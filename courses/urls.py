from django.conf.urls import url
from django.urls import path, re_path
from . import views as course_views
from users import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  re_path(r'^$', course_views.courses, name='courses'),

                  re_path(r'^(?P<course_name>[\w ]+)/$', user_views.course_homepage, name='course_homepage'),


                  re_path(r'^professor/(?P<course_name>[\w ]+)/$', course_views.teacher_courses, name='professor_course'),
                  re_path(r'^professor/(?P<course_name>[\w ]+)/delete/$', course_views.delete_course, name='delete'),
                  re_path(r'^professor/(?P<course_name>[\w ]+)/edit/$', course_views.update_course, name='edit'),

                  re_path(r'^professor/(?P<course_name>[\w ]+)/students/$', course_views.list_students,
                          name='list_students'),
                  re_path(r'^professor/(?P<course_name>[\w ]+)/students/(?P<student_id>[\d ]+)/remove/$',
                          course_views.remove_students, name='remove_students'),
                  re_path(r'^professor/(?P<course_name>[\w ]+)/students/(?P<student_id>[\d ]+)/add/$',
                          course_views.add_students, name='add_students'),

                  re_path(r'^professor/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/$', course_views.chapter,
                          name='chapter'),
                  re_path(r'^professor/edit/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/$',
                          course_views.update_chapter, name='edit_chapter'),
                  re_path(r'^professor/delete/(?P<course_name>[\w ]+)/(?P<slug>[\w-]+)/$',
                          course_views.delete_chapter, name='delete_chapter'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
