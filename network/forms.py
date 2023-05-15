from django import forms
from .models import *
from django.forms import ModelForm

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {'content': ""}
        widgets = {
        "content": forms.Textarea(attrs={'class':'form-control',  "placeholder":"What's on your mind?", "rows":3})
        }

# class NewPostForm(forms.Form):
#     content = forms.CharField(label="Content", widget=forms.Textarea(attrs={
#                                     'placeholder': "What's on your mind?",
#                                     'aria-label': "content",
#                                     'rows': 10,
#                                     "class": "form-control"
#                                     }))