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


class AddCourseForm(forms.ModelForm):
    class Meta:
        model = course
        fields = ['course_name', 'course_pic_URL', 'description', 'is_general_course']


class AddClassForm(forms.ModelForm):
    class_name = forms.CharField(label="<br><hr>یک اسم برای کلاس انتخاب کنید", max_length=80, required=True)
    course = forms.ModelChoiceField(label="<br><hr>کورس یا پایه ی کلاس خود را مشخص کنید<br>توجه: اگر کورس یا پایه شما "
                                          "در لیست "
                                          "موجود نیست باید اول آن را بسارید", required=True,
                                    queryset=course.objects.all())
    topic = forms.ModelChoiceField(label="<br><hr>مضمون کلاس خود را مشخص کنید<br>توجه: اگر مضمون یا درس شما در لیست "
                                         "موجود نیست باید اول آن را بسارید", required=True,
                                   queryset=topics.objects.all())
    capacity = forms.IntegerField(label="<br><hr>ظرفیت کلاس", required=True)
    link = forms.URLField(label="<br><hr>لینک گروه برای کلاس<br>توجه: برای درست کردن کلاس باید اول یک گروه تلگرامی "
                                "یا واتس "
                                "اپ درست کنید", max_length=80, required=False)
    class_pic_URL = forms.URLField(label="<br><hr>برای انتخاب عکس باید یک عکس را از اینترنت اتخاب کرده <br>سپس لینک "
                                         "عکس را "
                                         "در اینجا کپی کنید<br>انتخاب عکس احباری نمیباشد. در صورت اتنخاب نکردن٬ این "
                                         "عکس به صورت پیش فرض قرار میگیرد: <a "
                                         "href='https://online.stanford.edu/sites/default/files/styles"
                                         "/figure_default/public/2018-03/education-creating-effective-online-blended"
                                         "-courses_gse-yo.p.e.n.jpg?itok=QUn6gWp5'>  <img "
                                         "src='https://online.stanford.edu/sites/default/files/styles/figure_default"
                                         "/public/2018-03/education-creating-effective-online-blended-courses_gse-yo"
                                         ".p.e.n.jpg?itok=QUn6gWp5' width= '100px' height='70px'></a><br>",
                                   max_length=80,
                                   required=False)
    description = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'somesdkl;jaslj dsf ...'})
    saturday = forms.BooleanField(label=" شنبه ",  required=False,)
    sunday = forms.BooleanField(label="یک شنبه ",  required=False)
    monday = forms.BooleanField(label="دو شنبه ",  required=False)
    tuesday = forms.BooleanField(label="سه شنبه ",  required=False)
    wednesday = forms.BooleanField(label="چهار شنبه ",  required=False)
    thursday = forms.BooleanField(label="پنج شنبه ",  required=False)
    friday = forms.BooleanField(label=" جمعه ",  required=False)

    class Meta:
        model = Class
        fields = ['class_name', 'course', 'topic', 'capacity', 'link', 'class_pic_URL', 'description',
                  'saturday', 'satTime', 'sunday', 'sunTime', 'monday', 'monTime', 'tuesday', 'tueTime',
                  'wednesday', 'wedTime', 'thursday', 'thuTime', 'friday', 'friTime']


class AddTopicForm(forms.ModelForm):
    class Meta:
        model = topics
        fields = ['topic_name', 'is_Specialized']
