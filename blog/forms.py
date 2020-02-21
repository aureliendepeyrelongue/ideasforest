from django import forms
from django.forms import ModelForm
from .models import Comment, ContactMessage

class CommentForm(ModelForm):
    class Meta :
        model = Comment
        fields = ['content']

class ContactMessageForm(ModelForm):
    class Meta :
        model = ContactMessage
        fields = ['name', 'email', 'content']