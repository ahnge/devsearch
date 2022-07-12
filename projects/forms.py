from django.forms import ModelForm
from django import forms
from .models import Project, Review
from users.forms import BaseForm


class ProjectForm(BaseForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image',
                  'demo_link', 'source_link']

        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self,  *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update(
                {'class': 'input', 'placeholder': f"{name.capitalize()}"})

        # self.fields['title'].widget.attrs.update(
        #     {'class': 'input', 'placeholder': 'Add title'})

        # self.fields['description'].widget.attrs.update(
        #     {'class': 'input'})


class ReviewForm(BaseForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

    def __init__(self,  *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
