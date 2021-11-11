from django.contrib import admin
from .models import course, topics, Class
# Register your models here.


admin.site.register(course)
admin.site.register(topics)
admin.site.register(Class)