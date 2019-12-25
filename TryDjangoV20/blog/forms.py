from django import forms
from .models import UserBlog



class CreateNewBlog(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserBlog
        fields=[
            "title",
            "content",
            "image"
        ]