from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from user.models import Profile
from django.core.exceptions import ValidationError


def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')




class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  ]


    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'password']


class UpdateProfileFormNotVerified(forms.ModelForm):
    photo = forms.FileField(required=False, validators=[file_size])

    class Meta:
        model = Profile
        exclude = ['user', 'verified']


class UpdateProfileFormVerified(forms.ModelForm):
    photo = forms.FileField(required=False, validators=[file_size])

    class Meta:
        model = Profile
        exclude = ['user', 'verified', 'category', 'type', 'date_of_birth', 'gender']

