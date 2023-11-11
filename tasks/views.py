from typing import Any
from django.db import models
from django.shortcuts import render, reverse
from tasks.models import Task, Agent
from django.views import generic
from django.db.models.query import QuerySet
from tasks.forms import TaskModelForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from agents.mixin import OrganisorAndLoginRequiredMixin


class HomeView(LoginView):
    template_name = "task_home.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        messages.error(
            self.request, 'Login failed. Please check your credentials.')
        return super().form_invalid(form)


class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queryset = Task.objects.filter(organisation=user.userprofile)
        else:
            queryset = Task.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)

        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'tasks/task_detail.html'
    model = Task
    context_object_name = 'task'

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            queyset = Task.objects.filter(organisation=user.userprofile)
        else:
            queyset = Task.objects.filter(organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queyset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'tasks/task_create.html'
    form_class = TaskModelForm
    model = Task

    def get_success_url(self):
        return reverse("tasks:task_list")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.organisation = self.request.user.userprofile
        task.save()
        messages.success(self.request, "You have successfully created a Task")
        return super(TaskCreateView, self).form_valid(form)


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'tasks/task_delete.html'
    queryset = Task.objects.all()
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse('tasks:task_list')


class TaskUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "tasks/task_update.html"
    form_class = TaskModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        return Task.objects.filter(organisation=user.userprofile)

    def get_success_url(self):
        return reverse("tasks:task_list")

    def form_valid(self, form):
        form.save()
        messages.info(self.request, "You have successfully updated this task")
        return super(TaskUpdateView, self).form_valid(form)
