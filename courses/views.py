from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import *
from users.models import profile
from .models import course, topics, Class


# Create your views here.


def courses(request):
    queryset_grade = course.objects.filter(is_general_course=False)
    queryset_general = course.objects.filter(is_general_course=True)

    context = {
        "title": "Courses",
        "queryset_grade": queryset_grade,
        "queryset_general": queryset_general,
    }

    return render(request, "users/course.html", context)


@user_passes_test(lambda user: profile.is_teacher)
def teacher_courses(request, course_name=None):
    add_chapter_form = AddChapterForm(request.POST or None)
    queryset_chapter = Class.objects.filter(course__course_name=course_name)

    context = {
        "title": course_name,
        "add_chapter_form": add_chapter_form,
        "queryset_chapter": queryset_chapter,
        "course_name": course_name,
        "path": "Profile",
        "redirect_path": "profile",
    }

    if add_chapter_form.is_valid():
        instance = add_chapter_form.save(commit=False)
        instance.teacher_courses = teacher_courses.objects.get(course_name=course_name)
        instance.save()
        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

    return render(request, "courses/course.html", context)


@user_passes_test(lambda user: profile.is_teacher)
def chapter(request, course_name=None, slug=None):
    place = Class.objects.get(course__course_name=course_name, slug=slug)

    context = {
        "title": place.class_name,
        "time": str(place.time),
        "course_name": course_name,
        "slug": slug,
        "path": "Profile",
        "redirect_path": "profile",

    }

    return render(request, "courses/chapter.html", context)


@login_required
def class_register(request, course_name, class_name):
    user = profile.objects.get(user_name=request.user)
    class_info = Class.objects.get(class_name=class_name)
    course_info = course.objects.get(course_name=course_name)
    all_professors = profile.objects.filter(is_teacher=True)
    form = update_class_participants_form(instance=class_info)

    if request.method == 'POST':
        class_info.class_participants.add(user)

    context = {
        'user': user,
        'class': class_info,
        'course': course_info,
        'allteachers': all_professors,
        'class_students': class_info.class_participants,
        'form': form,
    }
    return render(request, 'users/classRegister.html', context)


@login_required
def your_classes(request):
    user = profile.objects.get(user_name=request.user)
    classes = Class.objects.filter(class_participants=request.user)
    professors = profile.objects.filter(is_teacher=True)
    students = profile.objects.filter(is_teacher=False).filter(is_staff=False)
    context = {
        'user': user,
        'class': classes,
        "professors": professors,
        "students": students,
    }
    return render(request, 'users/student_dashboard.html', context)





@user_passes_test(lambda user: profile.is_teacher)
def delete_course(request, course_name=None):
    instance = teacher_courses.objects.get(course_name=course_name)
    instance.delete()
    return HttpResponseRedirect(reverse('profile'))


@user_passes_test(lambda user: profile.is_teacher)
def delete_chapter(request, course_name=None, slug=None):
    instance = Class.objects.get(slug=slug)
    instance.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: profile.is_teacher)
def update_course(request, course_name=None):
    instance = teacher_courses.objects.get(course_name=course_name)
    update_course_form = EditCourseForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "form": update_course_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_course_form.is_valid():
        update_course_form.save()
        return redirect(reverse('profile'))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: profile.is_teacher)
def update_chapter(request, course_name=None, slug=None):
    instance = Class.objects.get(slug=slug)
    update_chapter_form = EditChapterForm(request.POST or None, instance=instance)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit",
        "course_name": course_name,
        "form": update_chapter_form,
        "path": path,
        "redirect_path": redirect_path,
    }

    if update_chapter_form.is_valid():
        update_chapter_form.save()
        return redirect(reverse('professor_course', kwargs={'course_name': course_name}))

    return render(request, "courses/edit.html", context)


@user_passes_test(lambda user: profile.is_teacher)
def list_students(request, course_name=None):
    courss = teacher_courses.objects.get(course_name=course_name)
    added_students = profile.objects.filter(students_to_course=courss)
    excluded_students = profile.objects.exclude(students_to_course=courss).filter(is_teacher=False).filter(
        is_staff=False)

    query_first = request.GET.get("q1")
    if query_first:
        excluded_students = excluded_students.filter(username__icontains=query_first)

    query_second = request.GET.get("q2")
    if query_second:
        added_students = added_students.filter(username__icontains=query_second)

    path = request.path.split('/')[1]
    redirect_path = path
    path = path.title()

    context = {
        "title": "Edit students in course " + course_name,
        "excluded_students": excluded_students,
        "added_students": added_students,
        "course_name": course_name,
        "path": path,
        "redirect_path": redirect_path,
        "startTime": "Start Time",
    }

    return render(request, "courses/add_students.html", context)


def add_students(request, student_id, course_name=None):
    student = profile.objects.get(id=student_id)
    clas = Class.objects.get(course__course_name=course_name)
    clas.class_participants.add(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@user_passes_test(lambda user: user.is_professor)
def remove_students(request, student_id, course_name=None):
    student = profile.objects.get(id=student_id)
    courss = teacher_courses.objects.get(course_name=course_name)
    courss.teachers.remove(student)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
