from django import forms
from .models import *
import re


class AddChapterForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name']

    def clean_chapter_name(self) -> object:
        class_name = self.cleaned_data.get('class_name')
        regexp = re.compile(r'[0-9a-zA-Z ]')

        if not regexp.match(class_name):
            raise forms.ValidationError("Please make sure chapter name contains (a-z, A-Z, 0-9, space) characters")

        return class_name


class EditCourseForm(forms.ModelForm):
    class Meta:
        model = course
        fields = ['course_name', 'is_general_course']


class EditChapterForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name']

class update_class_participants_form(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_participants']