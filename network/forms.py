from django import forms
from .models import Post
from django.forms import ModelForm

class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        labels = {'content': ""}
        widgets = {
        "content": forms.Textarea(attrs={'class':'form-control',  "placeholder":"What's on your mind?", "rows":3})
        }

