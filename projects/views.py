from typing import Any
from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Project, Document
from django.views import generic
from projects.forms import ProjectModelForm, DocumentForm
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
    template_name = 'projects/project_delete.html'

    def get_success_url(self):
        return reverse('project_list')


class ProjectDocumentCreat(generic.CreateView):
    form_class = DocumentForm
    template_name = 'projects/document_create.html'

    def get_success_url(self):
        return reverse('projects:project_detail', kwargs={"pk": self.kwargs["pk"]})

    def get_context_data(self, **kwargs):
        context = super(ProjectDocumentCreat, self).get_context_data(**kwargs)
        context.update({
            "project": Project.objects.get(pk=self.kwargs["pk"])
        })
        return context

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs["pk"])
        document = form.save(commit=False)
        document.project = project
        document.save()
        return super().form_valid(form)


class ProjectDocumentDelete(generic.DeleteView):
    template_name = 'projects/document_delete.html'

    def get_object(self, queryset=None):
        """ Hook to ensure object is fetched from your custom queryset. """
        # You can also add additional filters here if needed
        return get_object_or_404(Document, pk=self.kwargs['pk'])

    def get_success_url(self):
        document = Document.objects.get(id=self.kwargs["pk"])
        return reverse("projects:project_detail", kwargs={"pk": document.project.pk})
