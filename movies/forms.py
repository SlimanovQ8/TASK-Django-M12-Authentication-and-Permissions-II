from django import forms
from django.contrib.auth import get_user_model

from movies import models

User = get_user_model()


class MovieForm(forms.ModelForm):
    created_by = forms.ModelChoiceField(
        User.objects.all(),
        widget=forms.HiddenInput(),
    )

    class Meta:
        model = models.Movie
        fields = ["name", "plot", "created_by"]


class Registerform(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', "first_name", "last_name", "email"]
        widgets ={
            "password": forms.PasswordInput()
        }
class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
