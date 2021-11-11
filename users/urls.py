from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from . import views as user_views

urlpatterns = [
    url(r'', user_views.profile, name='profile'),
    path("update-profile/", user_views.update_profile, name="update_profile"),
    url("student/", user_views.student, name='student'),
    path("teacher/", user_views.professor, name='teacher'),

    path('sys-admin/', user_views.admin, name='admin'),
    path(r'edit/(?P<username>[\w ]+)/', user_views.update_user, name='update_user'),
    path(r'delete/(?P<username>[\w ]+)/', user_views.delete_user, name='delete_user'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
