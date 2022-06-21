from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import UserCreateForm, ProfileForm, SkillForm

# Create your views here.


class LoginView(View):
    template_name = "registration/login_register.html"

    def get(self, req):
        if req.user.is_authenticated:
            return redirect('users:all')

        ctx = {}
        if req.GET:
            next = req.GET['next']
            ctx = {'next': next}
        return render(req, self.template_name, ctx)

    def post(self, req):
        username = req.POST['username'].lower()
        password = req.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(req, 'Username does not exist')

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect(req.GET['next'] if 'next' in req.GET else 'users:all')

        else:
            messages.error(req, 'Username OR password is incorrect')
            return render(req, self.template_name)


class LogoutView(View):
    def get(self, req):
        if req.user.is_authenticated:
            logout(req)
            messages.info(req, 'Successfully logout!')

        return redirect('users:all')


class RegisterUserView(View):
    template_name = "registration/login_register.html"

    def get(self, req):
        form = UserCreateForm()
        ctx = {'form': form, 'page': 'register'}
        return render(req, self.template_name, ctx)

    def post(self, req):
        form = UserCreateForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(req, 'User account was created!')
            if user is not None:
                login(req, user)
            return redirect('users:edit_account')
        else:
            messages.error(req, 'An error has occurred during registration.')
            ctx = {'form': form, 'page': 'register'}

        return render(req, self.template_name, ctx)


class Profiles(View):
    template_name = "users/profiles.html"
    profiles = Profile.objects.all()
    ctx = {'profiles': profiles}

    def get(self, req):
        return render(req, self.template_name, self.ctx)


class UserProfile(View):
    template_name = 'users/user-profile.html'

    def get(self, req, pk):
        profile = Profile.objects.get(pk=pk)
        top_skills = profile.skill_set.exclude(description__exact="")
        other_skills = profile.skill_set.filter(description="")
        ctx = {'profile': profile, 'top_skills': top_skills,
               'other_skills': other_skills}

        return render(req, self.template_name, ctx)


class UserAccount(LoginRequiredMixin, View):
    template_name = 'users/account.html'
    login_url = '/login/'

    def get(self, req):
        profile = req.user.profile
        skills = profile.skill_set.all()
        projects = profile.project_set.all()
        ctx = {'profile': profile, 'skills': skills, 'projects': projects}
        return render(req, self.template_name, ctx)


class EditAccount(LoginRequiredMixin, View):
    template_name = 'users/profile_form.html'
    login_url = '/login/'

    def get(self, req):
        f = ProfileForm(instance=req.user.profile)
        ctx = {'form': f}
        return render(req, self.template_name, ctx)

    def post(self, req):
        profile = req.user.profile
        f = ProfileForm(req.POST, req.FILES, instance=profile)
        if not f.is_valid:
            ctx = {'form': f}
            return render(req, self.template_name, ctx)

        f.save()
        messages.success(req, 'Account edited successfully')
        return redirect('users:user_account')


class CreateSkill(LoginRequiredMixin, View):
    template_name = 'users/skill_form.html'
    login_url = '/login/'

    def get(self, req):
        f = SkillForm()
        ctx = {'form': f}
        return render(req, self.template_name, ctx)

    def post(self, req):
        profile = req.user.profile
        f = SkillForm(req.POST)
        if f.is_valid():
            skill = f.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(req, "Skill was created successfully")
        else:
            ctx = {'form': f}
            messages.error(req, "Something went wrong")
            return render(req, self.template_name, ctx)
        return redirect('users:user_account')


class UpdateSkill(LoginRequiredMixin, View):
    template_name = 'users/skill_form.html'
    login_url = '/login/'

    def get(self, req, pk):
        profile = req.user.profile
        skill = profile.skill_set.get(pk=pk)
        form = SkillForm(instance=skill)
        ctx = {'form': form}
        return render(req, self.template_name, ctx)

    def post(self, req, pk):
        profile = req.user.profile
        skill = profile.skill_set.get(pk=pk)
        form = SkillForm(req.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(req, "Skill was updated successfully")
        return redirect('users:user_account')


class DeleteSkill(LoginRequiredMixin, View):
    template_name = 'delete_form.html'
    login_url = '/login/'

    def get(self, req, pk):
        profile = req.user.profile
        skill = profile.skill_set.get(pk=pk)
        ctx = {'object': skill}
        return render(req, self.template_name, ctx)

    def post(self, req, pk):
        profile = req.user.profile
        skill = profile.skill_set.get(pk=pk)
        skill.delete()
        messages.success(req, "Skill was deleted successfully")
        return redirect('users:user_account')
