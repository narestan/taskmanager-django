from django.shortcuts import render, redirect, reverse
from .models import Project
from django.views import generic
from projects.forms import ProjectModelForm
from agents.mixin import OrganisorAndLoginRequiredMixin

# CRUD Projects


class ProjectListView(generic.ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/project_list.html'


class ProjectDetailView(generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'


class ProjectCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    form_class = ProjectModelForm
    template_name = 'projects/project_create.html'

    def get_success_url(self):
        return reverse('projects:project_list')


class ProjectUpdateView(generic.UpdateView):
    model = Project
    form_class = ProjectModelForm
    template_name = 'projects/project_update.html'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


class ProjectDeleteView(generic.DeleteView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_confirm_delete.html'

    def get_success_url(self):
        return reverse('project_list')
