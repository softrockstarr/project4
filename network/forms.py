from django import forms
from .models import *
from django.forms import ModelForm

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]

# class NewPostForm(forms.Form):
#     content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
#                                     'placeholder': "What's on your mind?",
#                                     'aria-label': "content",
#                                     'rows': 10,
#                                     "class": "form-control"
#                                     }))