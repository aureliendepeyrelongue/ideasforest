from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from PIL import Image
from django.core.files import File

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    class Meta :
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta :
        model = User
        fields = [ 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta :
        model = Profile
        fields = ['about','image','x', 'y', 'width', 'height']

    def save(self):
        profile = super(ProfileUpdateForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(profile.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((300, 300), Image.ANTIALIAS)
        resized_image.save(profile.image.path)

        return profile
