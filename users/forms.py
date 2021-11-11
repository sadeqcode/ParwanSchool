from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import re
from users.models import *
from courses.models import course, Class, topics
from phonenumber_field.formfields import PhoneNumberField


class AddUser(forms.ModelForm):
    class Meta:
        model = profile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['user_name', 'password', 'email', 'is_teacher', 'is_staff']


class EditUser(forms.ModelForm):
    class Meta:
        model = profile
        widgets = {
            'password': forms.PasswordInput(),
        }
        fields = ['user_name', 'password', 'email', 'is_teacher', 'is_staff']

    # Don't want to modify blank setting inside models (doing so will break normal validation in admin site)
    # The redefined constructor won't harm any functionality.
    def __init__(self, *args, **kwargs):
        super(EditUser, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class Contact(forms.Form):
    sender = forms.CharField(label='Name', max_length=30)
    subject = forms.CharField(label='Subject', max_length=30)
    email = forms.EmailField(label='Email', max_length=30)
    message = forms.CharField(widget=forms.Textarea)


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = course
        fields = ['course_name', 'is_general_course']

    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')

        regexp = re.compile(r'[0-9a-zA-Z ]')
        if not regexp.match(course_name):
            raise forms.ValidationError("Please make sure course name contains (a-z, A-Z, 0-9, space) characters")

        return course_name


class CreateUserForm(UserCreationForm):
    class Meta:
        model = profile
        fields = ['user_name', 'email', 'first_name', 'last_name', 'birth_date', 'phone_number', 'password1',
                  'password2']


class update_profile_form(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['user_name', 'email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'profile_pic', 'about']



