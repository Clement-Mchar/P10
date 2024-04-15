from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Project(models.Model):
    TYPE_CHOICES = (
        ('front-end', "front-end"),
        ('Back-end', "back-end"),
        ('iOs', "iOs"),
        ('android', "android"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=128, verbose_name="name", null=False, blank=False
    )
    description = models.TextField(
        max_length=2048, blank=True, verbose_name="description", null=False
    )
    contributors = models.ManyToManyField(settings.AUTH_USER_MODEL, through="authentication.Contributor")
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default="")
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name="author", on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

class Issue(models.Model):
    PRIORITY_CHOICES= (
        ('LOW', 'low'),
        ('MEDIUM', 'medium'),
        ('HIGH', 'high'),

    )
    TAG_CHOICES= (
        ('To Do', 'to do'),
        ('In Progress', 'in progress'),
        ('Finished', 'finished'),

    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=128, verbose_name="title", null=False, blank=False
    )
    description = models.TextField(blank=True, verbose_name="description", null=False)
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default="")
    tag = models.CharField(max_length=15, choices=TAG_CHOICES, default="")
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    comment = models.TextField(blank=True, verbose_name="comment", null=False)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
