from typing import Any
from django.db import models
from django.shortcuts import render, reverse
from tasks.models import Task, Agent, Category, FollowUp
from django.views import generic
from django.db.models.query import QuerySet
from tasks.forms import TaskModelForm, FollowUpModelForm, AssignAgentForm, TaskCategoryUpdateForm, CategoryModelForm, FollowUpModelForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from agents.mixin import OrganisorAndLoginRequiredMixin
import datetime
from django.utils import timezone


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
            queryset = Task.objects.filter(organisation=user.userprofile)
        else:
            queryset = Task.objects.filter(
                organisation=user.agent.organisation)
            queryset = queryset.filter(agent__user=user)
        return queryset


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


class TaskCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tasks/task_category_update.html"
    form_class = TaskCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of Tasks for the entire organisation
        if user.is_organisor:
            queryset = Task.objects.filter(organisation=user.userprofile)
        else:
            queryset = Task.objects.filter(
                organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.get_object().id})

    def form_valid(self, form):
        task_before_update = self.get_object()
        instance = form.save(commit=False)

        organisation = task_before_update.organisation if hasattr(
            task_before_update, 'organisation') else self.request.user.userprofile

        # Ensure the "Converted" category exists
        converted_category, created = Category.objects.get_or_create(
            name="Converted", defaults={'organisation': organisation})

        if form.cleaned_data["category"] == converted_category:
            # update the date at which this task was converted
            if task_before_update.category != converted_category:
                # this task has now been converted
                instance.converted_date = timezone.now()
        instance.save()
        return super(TaskCategoryUpdateView, self).form_valid(form)


class FollowUpCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "tasks/followup_create.html"
    form_class = FollowUpModelForm

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(FollowUpCreateView, self).get_context_data(**kwargs)
        context.update({
            "task": Task.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        task = Task.objects.get(pk=self.kwargs["pk"])
        followup = form.save(commit=False)
        followup.task = task
        followup.save()
        return super(FollowUpCreateView, self).form_valid(form)


class FollowUpUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "tasks/followup_update.html"
    form_class = FollowUpModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(
                task__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(
                task__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(task__agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.get_object().task.id})


class FollowUpDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "tasks/followup_delete.html"

    def get_success_url(self):
        followup = FollowUp.objects.get(id=self.kwargs["pk"])
        return reverse("tasks:task_detail", kwargs={"pk": followup.task.pk})

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        if user.is_organisor:
            queryset = FollowUp.objects.filter(
                task__organisation=user.userprofile)
        else:
            queryset = FollowUp.objects.filter(
                task__organisation=user.agent.organisation)
            # filter for the agent that is logged in
            queryset = queryset.filter(task__agent__user=user)
        return queryset


class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "tasks/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("tasks:task-list")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        task = Task.objects.get(id=self.kwargs["pk"])
        task.agent = agent
        task.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "tasks/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get the original queryset of categories
        categories = context['category_list']

        # Update context with categories and their task counts
        categories_with_task_count = []
        for category in categories:
            category.task_count = Task.objects.filter(
                category=category).count()
            categories_with_task_count.append(category)

        context['category_list'] = categories_with_task_count

        if user.is_organisor:
            queryset = Task.objects.filter(organisation=user.userprofile)
        else:
            queryset = Task.objects.filter(
                organisation=user.agent.organisation)

        context['unassigned_task_count'] = queryset.filter(
            category__isnull=True).count()

        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            return Category.objects.filter(organisation=user.userprofile)
        else:
            return Category.objects.filter(organisation=user.agent.organisation)


class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "tasks/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        # Get the current category from the context
        category = context['category']
        # Retrieve tasks related to the category
        context['tasks'] = Task.objects.filter(category=category)
        return context


class CategoryCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "tasks/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("tasks:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organisation = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "tasks/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("tasks:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset


class CategoryDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "tasks/category_delete.html"

    def get_success_url(self):
        return reverse("tasks:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of tasks for the entire organisation
        if user.is_organisor:
            queryset = Category.objects.filter(
                organisation=user.userprofile
            )
        else:
            queryset = Category.objects.filter(
                organisation=user.agent.organisation
            )
        return queryset
