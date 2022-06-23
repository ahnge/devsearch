from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .utils import search_projects


class ProjectsView(View):
    template_name = "projects/projects.html"

    def get(self, req):
        ctx = search_projects(req)
        return render(req, self.template_name, ctx)


def project(req, pk):
    pj = Project.objects.get(pk=pk)
    ctx = {'project': pj}

    return render(req, "projects/single-project.html", ctx)


class CreateProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req):
        form = ProjectForm
        ctx = {'form': form}
        return render(req, 'projects/project_form.html', ctx)

    def post(self, req):
        profile = req.user.profile
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            pj = form.save(commit=False)
            pj.owner = profile
            pj.save()
            messages.success(req, "Project created successfully")
        return redirect('users:user_account')


class UpdateProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req, pk):
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        form = ProjectForm(instance=pj)
        ctx = {'form': form}
        return render(req, 'projects/project_form.html', ctx)

    def post(self, req, pk):
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        form = ProjectForm(req.POST, req.FILES, instance=pj)
        if form.is_valid():
            form.save()
            messages.success(req, "Project updated successfully")
        return redirect('users:user_account')


class DeleteProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req, pk):
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        ctx = {'object': pj}
        return render(req, 'delete_form.html', ctx)

    def post(self, req, pk):
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        pj.delete()
        messages.success(req, "Project deleted successfully")
        return redirect('users:user_account')
