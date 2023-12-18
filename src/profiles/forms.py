from django import forms
from .models import Profile

from django.utils.translation import ugettext_lazy

class ProfileModelForm(forms.ModelForm):
    first_name = forms.CharField(label=ugettext_lazy("first-name"), widget=forms.TextInput())
    last_name = forms.CharField(label=ugettext_lazy("last-name"), widget=forms.TextInput())
    bio = forms.CharField(label=ugettext_lazy("my-profile-biography"), widget=forms.Textarea(), required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')

