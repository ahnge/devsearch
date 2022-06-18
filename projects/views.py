from django.shortcuts import render, redirect
from .models import Project
from .forms import ProjectForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


def projects(req):
    msg = 'projects'
    projects = Project.objects.all()
    ctx = {'msg': msg, 'projects': projects}
    return render(req, "projects/projects.html", ctx)


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
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
        return redirect('projects:all_pjs')


class UpdateProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req, pk):
        pj = Project.objects.get(pk=pk)
        form = ProjectForm(instance=pj)
        ctx = {'form': form}
        return render(req, 'projects/project_form.html', ctx)

    def post(self, req, pk):
        pj = Project.objects.get(pk=pk)
        form = ProjectForm(req.POST, req.FILES, instance=pj)
        if form.is_valid():
            form.save()
        return redirect('projects:all_pjs')


class DeleteProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req, pk):
        pj = Project.objects.get(pk=pk)
        ctx = {'project': pj}
        return render(req, 'projects/delete_form.html', ctx)

    def post(self, req, pk):
        pj = Project.objects.get(pk=pk)
        pj.delete()
        return redirect('projects:all_pjs')
