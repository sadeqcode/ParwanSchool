import http.client

from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from itertools import chain
from django.http import Http404
from django.core.mail import send_mail

from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

import users.models
from courses.models import Class, course, topics
from users.forms import Contact, AddUser, EditUser, CreateUserForm, update_profile_form
from courses.forms import AddClassForm, AddCourseForm, AddTopicForm
from users.models import profile as userprofile
from users.models import profile


# Create your views here.


def home(request):
    teachers_count = userprofile.objects.filter(is_teacher=True).count
    students_count = userprofile.objects.filter(is_teacher=False).filter(is_staff=False).count()
    class_count = Class.objects.all().count()
    topics_count = topics.objects.all().count()
    context = {
        "title": "eLearning",
        "teachers_count": teachers_count,
        "students_count": students_count,
        "class_count": class_count,
        "topics_count": topics_count,
    }

    return render(request, "home.html", context)


def about(request):
    teachers_count = userprofile.objects.filter(is_teacher=True).count
    students_count = userprofile.objects.filter(is_teacher=False).filter(is_staff=False).count()
    class_count = Class.objects.all().count()
    topics_count = topics.objects.all().count()
    context = {
        "title": "About",
        "teachers_count": teachers_count,
        "students_count": students_count,
        "class_count": class_count,
        "topics_count": topics_count,
    }

    return render(request, "about.html", context)


def contact(request):
    user = userprofile.objects.filter(user_name=request.user)
    if request.method == 'POST':
        sender_name = request.POST['name']
        sender_email = request.POST['mail']
        sender_message = request.POST['message']
        send_mail(
            sender_name,  # subject
            sender_message,  # massage
            sender_email,  # from email
            ['sadeqnameh@gmail.com'],  # to email
        )
        context = {
            "title": "Contact",
            "sender": user
        }
        return render(request, "users/contact.html", context)

    else:
        context = {
            "title": "Contact",
        }

        return render(request, "users/contact.html", context)


@login_required
def profile(request):
    user = request.user
    userinfo = userprofile.objects.get(user_name=user)

    user_class = Class.objects.filter(class_participants=userinfo)
    user_classes_count = Class.objects.filter(class_participants=userinfo).count()

    user_topics_count = 0
    user_topics_all = []
    for topic in user_class:
        if topic.topic not in user_topics_all:
            user_topics_all.append(topic.topic)
            user_topics_count += 1

    context = {
        'user': user,
        'profile': userinfo,
        'user_class': user_class,
        'user_class_count': user_classes_count,
        'user_topics': user_topics_all,
        'user_topic_count': user_topics_count,

    }

    return render(request, "users/profile.html", context)


@login_required
def update_profile(request):
    user = userprofile.objects.get(user_name=request.user)
    if request.method == 'POST':
        form = update_profile_form(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت آپدیت شد')
            return redirect('profile')
    else:
        form = update_profile_form(instance=user)
    context = {
        'user': user,
        'form': form,
    }

    return render(request, 'users/profile_update.html', context)


@user_passes_test(lambda user: user.is_site_admin)
def admin(request):
    add_user_form = AddUser(request.POST or None)
    queryset = profile.objects.all()

    search = request.GET.get("search")
    if search:
        queryset = queryset.filter(username__icontains=search)

    context = {
        "title": "Admin",
        "add_user_form": add_user_form,
        "queryset": queryset,

    }

    if add_user_form.is_valid():
        instance = add_user_form.save(commit=False)
        passwd = add_user_form.cleaned_data.get("password")
        instance.password = make_password(password=passwd,
                                          salt='salt', )
        instance.save()
        reverse('profile')

    return render(request, "users/sysadmin_dashboard.html", context)


# def professor(request):
#    add_course_form = AddCourseForm(request.POST or None)
#    queryset_course = course.objects.filter(user__username=request.user)

#    context = {
#        "title": "Professor",
#        "add_course_form": add_course_form,
#        "queryset_course": queryset_course,
#    }

#    if add_course_form.is_valid():
#        course_name = add_course_form.cleaned_data.get("course_name")
#        instance = add_course_form.save(commit=False)
#        instance.user = request.user
#        instance.save()
#        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

#   return render(request, "users/professor_dashboard.html", context)


@login_required
def student(request):
    classes = Class.objects.filter(class_participants=request.user)
    professors = profile.objects.filter(is_teacher=True)
    students = profile.objects.filter(is_teacher=False).filter(is_staff=False)
    context = {
        "title": request.user,
        "professors": professors,
        "students": students,
        "class": classes,
    }

    return render(request, "users/student_dashboard.html", context)


@user_passes_test(lambda user: userprofile.is_teacher)
def add_course(request):
    form = AddCourseForm
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'courses/new_course.html', context)


@user_passes_test(lambda user: userprofile.is_teacher)
def add_topic(request):
    form = AddTopicForm
    if request.method == 'POST':
        form = AddTopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form': form
    }
    return render(request, 'courses/new_topic.html', context)


@user_passes_test(lambda user: userprofile.is_teacher)
def add_class(request):
    form = AddClassForm
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'courses/new_class.html', context)


@user_passes_test(lambda user: user.is_site_admin)
def update_user(request, username):
    user = profile.objects.get(userـname=username)
    data_dict = {'username': user.username, 'email': user.email}
    update_user_form = EditUser(initial=data_dict, instance=user)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "update_user_form": update_user_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if request.POST:
        user_form = EditUser(request.POST, instance=user)

        if user_form.is_valid():
            instance = user_form.save(commit=False)
            passwd = user_form.cleaned_data.get("password")

            if passwd:
                instance.password = make_password(password=passwd,
                                                  salt='salt', )
            instance.save()

            return redirect(reverse('profile'))

    return render(request, "users/edit_user.html", context)


@user_passes_test(lambda user: user.is_site_admin)
def delete_user(request, username):
    user = profile.objects.get(username=username)
    user.delete()
    return redirect(reverse('profile'))


def course_homepage(request, course_name):
    class_list = Class.objects.filter(course__course_name=course_name)

    if class_list:

        professors = userprofile.objects.filter(is_teacher=True)
        students = userprofile.objects.filter(is_teacher=False).filter(is_staff=False)
        user = request.user

        context = {
            "course_name": course_name,
            "class_list": class_list,

            "professors": professors,
            "students": students,
        }
        return render(request, "users/course_detaila.html", context)

    else:
        warning_message = "متاسفانه هنوز کلاسی برای این پایه یا کورس وجود ندارد "
        messages.warning(request, warning_message)
        return redirect(reverse('courses'))


# login and register pages
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('user_name')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'registration/registration_form.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')
