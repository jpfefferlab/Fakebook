from django import forms
from .models import Post, Comment

from django.utils.translation import ugettext_lazy

class PostModelForm(forms.ModelForm):
    #image = forms.ImageField(label='Upload Image', widget=forms.ClearableFileInput(attrs={'id':'itest'}))
    content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':3,'placeholder': ugettext_lazy("post_creation_prompt"), 'style':'background-color : #F0F2F5;'}))
    image = forms.ImageField(label='', required=False, widget=forms.ClearableFileInput(attrs={'style':'background-color : transparent; border-color: transparent; text-color=red'}))
    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': ugettext_lazy("comment_creation_prompt")}))
    class Meta:
        model = Comment
        fields = ('body',)
