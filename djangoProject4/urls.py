"""djangoProject4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from courses import views as course_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('about/', user_views.about, name='about'),
    path('courses/', include('courses.urls')),
    re_path(r'courses/(?P<course_name>[\w ]+)/(?P<class_name>[\w ]+)/$', course_views.class_register,
            name='class-register'),
    path('profile/', include('users.urls')),
    path("update-profile/", user_views.update_profile, name="update_profile"),
    path("your-classes/", course_views.your_classes, name="your-classes"),
    path('contact/', user_views.contact, name='contact'),
    path(r'login/', user_views.loginPage, name='login'),
    path(r'register/', user_views.registerPage, name='register'),
    path(r'logout/', user_views.logoutUser, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Remove this in project deployment
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
