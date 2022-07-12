from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import Profile, Message
from .forms import UserCreateForm, ProfileForm, SkillForm, MessageForm
from .utils import search_profiles, paginate_profiles, account_activation_token

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
            user.is_active = False
            user.save()
            current_site = get_current_site(req)
            mail_subject = 'Activate your devsearch account.'
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(req, 'users/check_email.html')
        else:
            messages.error(req, 'An error has occurred during registration.')
            ctx = {'form': form, 'page': 'register'}

        return render(req, self.template_name, ctx)


class UserAccountActivateView(View):
    template_name = 'users/invalid_link.html'

    def get(self, req, uidb64, token):
        if req.user.is_authenticated:
            return redirect('users:all')

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(req, user)
            subject = 'Welcome to Devsearch'
            msg = "We are glad you are here!"
            email = EmailMessage(
                subject=subject,
                body=msg,
                from_email=settings.EMAIL_HOST_USER,
                to=[user.email],
                headers={'Content-Type': 'text/plain'},
            )
            email.send()
            messages.success(req, 'User account was created!')
            return redirect(req.GET['next'] if 'next' in req.GET else 'users:edit_account')
        else:
            return render(req, self.template_name)


class Profiles(View):
    template_name = "users/profiles.html"

    def get(self, req):
        profiles, search_query = search_profiles(req)
        custom_range, profiles = paginate_profiles(req, profiles)

        ctx = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
        return render(req, self.template_name, ctx)


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


class InboxView(LoginRequiredMixin, View):
    template_name = 'users/inbox.html'
    login_url = '/login/'

    def get(self, req):
        profile = req.user.profile
        m = profile.messages.all()
        umc = m.filter(is_read=False).count()
        ctx = {'ms': m, 'unread_msgs': umc}
        return render(req, self.template_name, ctx)


class MsgDetailView(LoginRequiredMixin, View):
    template_name = 'users/message.html'
    login_url = '/login/'

    def get(self, req, pk):
        p = req.user.profile
        m = p.messages.get(id=pk)
        if not m.is_read:
            m.is_read = True
            m.save()
        ctx = {'msg': m}
        return render(req, self.template_name, ctx)


class CreateMsg(View):
    template_name = "users/message_form.html"

    def get(self, req, pk):
        p = Profile.objects.get(pk=pk)
        if req.user.is_authenticated and req.user.profile == p:
            messages.warning(req, "Wow Wow, just wow!")
            return redirect('users:user_profile', pk=pk)
        f = MessageForm()
        ctx = {'profile_id': pk, 'form': f}
        return render(req, self.template_name, ctx)

    def post(self, req, pk):
        recipient_p = Profile.objects.get(pk=pk)
        f = MessageForm(req.POST)
        if f.is_valid():
            if req.user.is_authenticated:
                m = f.save(commit=False)
                m.sender = req.user.profile
                m.recipient = recipient_p
                m.name = req.user.profile.name
                m.email = req.user.profile.email
                m.save()
            else:
                m = f.save(commit=False)
                m.recipient = recipient_p
                m.save()
            messages.success(req, "Message sent successfully")
            return redirect('users:user_profile', pk=pk)

        ctx = {'profile_id': pk, 'form': f}
        messages.error(req, "Message not sent")
        return render(req, self.template_name, ctx)


class DeleteMsgView(LoginRequiredMixin, View):
    template_name = 'delete_form.html'
    login_url = '/login/'

    def get(self, req, pk):
        msg = Message.objects.get(pk=pk)
        ctx = {'object': msg}
        return render(req, self.template_name, ctx)

    def post(self, req, pk):
        msg = Message.objects.get(pk=pk)
        msg.delete()
        messages.success(req, "Message was deleted successfully")
        return redirect('users:inbox')
