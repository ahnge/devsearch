from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
