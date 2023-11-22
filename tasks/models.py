from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from projects.models import Project
import jdatetime
from django_jalali.db.models import jDateTimeField


class User(AbstractUser):
    mcom = 'Commercial Manage'
    com = 'expert'
    POSITION_CHOICES = [
        (mcom, 'مدیر بازرگانی'),
        (com, 'کارشناس'),
    ]

    is_organisor = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    mobile_number = models.IntegerField(blank=True, null=True)
    position = models.CharField(max_length=100, choices=POSITION_CHOICES)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class TaskManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()


class Task(models.Model):
    task_name = models.CharField(max_length=15)
    info = models.TextField(max_length=150)
    agent = models.ForeignKey(
        'Agent', on_delete=models.SET_NULL, null=True)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = jDateTimeField(auto_now_add=True)
    date_start = jDateTimeField(null=True, blank=True)
    date_end = jDateTimeField(null=True, blank=True)
    category = models.ForeignKey(
        "Category", related_name="tasks", null=True, blank=True, on_delete=models.SET_NULL)
    converted_date = models.DateTimeField(null=True, blank=True)
    project = models.ForeignKey(
        Project, on_delete=models.SET_NULL, null=True)
    objects = TaskManager()

    def __str__(self):
        return f"{self.task_name}"

    #  to set the date_start to the date_created value if date_start is not provided.
    def save(self, *args, **kwargs):
        if not self.date_start:
            self.date_start = self.created_at
        super(Task, self).save(*args, **kwargs)


class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


def post_user_created_signal(sender, instance, created, **kwargs):
    print(instance, created)
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(post_user_created_signal, sender=User)

# Add follow up for Task


def handle_upload_follow_ups(instance, filename):
    return f"task_followups/task_{instance.task.pk}/{filename}"


class FollowUp(models.Model):
    task = models.ForeignKey(
        Task, related_name="followups", on_delete=models.CASCADE)
    date_added = jDateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    file = models.FileField(null=True, blank=True,
                            upload_to=handle_upload_follow_ups)

    def __str__(self):
        return f"{self.task.task_name} "


class Category(models.Model):
    # New, Contacted, Converted, Unconverted
    name = models.CharField(max_length=30)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
