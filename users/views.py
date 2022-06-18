from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from .forms import UserCreateForm

# Create your views here.


class LoginView(View):
    template_name = "registration/login_register.html"

    def get(self, req):
        if req.user.is_authenticated:
            return redirect('users:all')
        return render(req, self.template_name)

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
            return redirect('users:all')
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
