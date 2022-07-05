from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .utils import search_projects, paginate_projects
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm


class ProjectsView(View):
    template_name = "projects/projects.html"

    def get(self, req):
        projects, search_query = search_projects(req)
        custom_range, projects = paginate_projects(req, projects)

        ctx = {'projects': projects, 'search_query': search_query,
               'custom_range': custom_range}
        return render(req, self.template_name, ctx)


class ProjectView(View):
    def get(self, req, pk):
        pj = Project.objects.get(pk=pk)
        f = ReviewForm()
        ctx = {'project': pj, 'form': f}
        return render(req, "projects/single-project.html", ctx)

    def post(self, req, pk):
        pj = Project.objects.get(pk=pk)
        f = ReviewForm(req.POST)
        if f.is_valid():
            review = f.save(commit=False)
            review.project = pj
            review.owner = req.user.profile
            review.save()
            pj.getVoteCount
            messages.success(req, 'Your review was successfully submitted!')
            return redirect('projects:sg_pj', pk=pk)
        else:
            print("form is not validated")
            ctx = {'form': f, 'project': pj}
            return render(req, "projects/single-project.html", ctx)


class CreateProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req):
        form = ProjectForm
        ctx = {'form': form}
        return render(req, 'projects/project_form.html', ctx)

    def post(self, req):
        new_tags = req.POST.get("new_tags").replace(',', '').split()
        profile = req.user.profile
        form = ProjectForm(req.POST, req.FILES)
        if form.is_valid():
            pj = form.save(commit=False)
            pj.owner = profile
            pj.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                pj.tags.add(tag)
            messages.success(req, "Project created successfully")
        return redirect('users:user_account')


class UpdateProject(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, req, pk):
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        form = ProjectForm(instance=pj)
        ctx = {'form': form, 'project': pj}
        return render(req, 'projects/project_form.html', ctx)

    def post(self, req, pk):
        new_tags = req.POST.get("new_tags").replace(',', '').split()
        profile = req.user.profile
        pj = profile.project_set.get(pk=pk)
        form = ProjectForm(req.POST, req.FILES, instance=pj)
        if form.is_valid():
            p = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                p.tags.add(tag)
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
