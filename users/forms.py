from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.models import ModelForm
from .models import Profile, Skill, Message


class BaseForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        for bound_field in self:
            if hasattr(bound_field, "field") and bound_field.field.required:
                bound_field.field.widget.attrs["required"] = "required"


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input', 'placeholder': f"{name.capitalize()}"})

        self.fields['first_name'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Full name'}
        )
        self.fields['password1'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Password'}
        )
        self.fields['password2'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Confirm your password'}
        )


class ProfileForm(BaseForm):
    class Meta:
        model = Profile
        exclude = ['user']

    def __init__(self,  *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input', 'placeholder': f"{name.capitalize()}"})


class SkillForm(BaseForm):
    class Meta:
        model = Skill
        exclude = ['owner']

    def __init__(self,  *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input', 'placeholder': f"{name.capitalize()}"})


class MessageForm(BaseForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self,  *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input', 'placeholder': f"{name.capitalize()}"})
