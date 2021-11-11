from __future__ import unicode_literals

from django.db import models
import os
from users.models import profile
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.dispatch import receiver


# Create your models here.


class course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)
    course_pic_URL = models.URLField(
        default="https://online.stanford.edu/sites/default/files/styles/figure_default/public/2018-03/education"
                "-creating-effective-online-blended-courses_gse-yo.p.e.n.jpg?itok=QUn6gWp5")
    description = models.TextField(max_length=500, blank=True)
    is_general_course = models.BooleanField(default=True)
    course_created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.course_name

    def __str__(self):
        return self.course_name


class topics(models.Model):
    topic_name = models.CharField(max_length=100)
    is_Specialized = models.BooleanField(default=False)
    topic_created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.topic_name


class Class(models.Model):
    class_name = models.CharField(max_length=20, unique=True)
    link = models.URLField()
    class_created_date = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(topics, on_delete=models.CASCADE)
    capacity = models.PositiveIntegerField(default=7)
    course = models.ForeignKey(course, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(unique=True)
    class_pic_URL = models.URLField(default="https://media.istockphoto.com/vectors/communication-elearning-internet"
                                            "-network-as-knowledge-base-vector-id1059510610?k=20&m=1059510610&s"
                                            "=612x612&w=0&h=E3wbE9HsFSxUh6PcsCobIti-wfFrOD05jYHJl_a3yXQ=")
    saturday = models.BooleanField(default=False)
    satTime = models.TimeField(default='00:00')
    sunday = models.BooleanField(default=False)
    sunTime = models.TimeField(default='00:00')
    monday = models.BooleanField(default=False)
    monTime = models.TimeField(default='00:00')
    tuesday = models.BooleanField(default=False)
    tueTime = models.TimeField(default='00:00')
    wednesday = models.BooleanField(default=False)
    wedTime = models.TimeField(default='00:00')
    thursday = models.BooleanField(default=False)
    thuTime = models.TimeField(default='00:00')
    friday = models.BooleanField(default=False)
    friTime = models.TimeField(default='00:00')
    description = models.TextField(max_length=500, blank=True)
    class_participants = models.ManyToManyField(profile)

    def __unicode__(self):
        return self.class_name

    def __str__(self):
        return self.class_name

    def get_absolute_url(self):
        return reverse("chapter", kwargs={"course_name": self.course,
                                          "slug": self.slug})

    def slug_default(self):
        slug = create_slug(new_slug=self.class_name)
        return slug


def create_slug(instance=None, new_slug=None):
    slug = slugify(instance.class_name)

    if new_slug is not None:
        slug = new_slug

    qs = Class.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()

    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)

    return slug
