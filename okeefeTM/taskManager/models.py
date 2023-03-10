from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Task(models.Model):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    UNASSIGNED = 0
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETE = 3
    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]
    STATUS_CHOICES = [
        (UNASSIGNED, "Unassigned"),
        (NOT_STARTED, "Not Started"),
        (IN_PROGRESS, "In Progress"),
        (COMPLETE, "Complete"),
    ]
    BOOLEAN_CHOICES = [
      (True, "Yes"),
      (False, "No"),
    ]
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=150)
    desc = models.CharField(max_length=255)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=LOW)
    status = models.IntegerField(choices=STATUS_CHOICES, default=UNASSIGNED)
    date_created = models.DateField(default=timezone.now())
    date_due = models.DateField(null=True, blank=True, default=None)
    date_completed = models.DateField(null=True, blank=True, default=None)
    repeat = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)
    note = models.CharField(max_length=255, null=True, blank=True)
    isSeen = models.BooleanField(default=False, choices=BOOLEAN_CHOICES)

    def __str__(self):
      return self.name

class Repeating_Task(models.Model):
    DAILY = "Day"
    WEEKLY = "Week"
    BIWEEKLY = "BiWeek"
    MONTHLY = "Month"
    QUARTERLY = "Quart"
    SEMI_ANNUAL = "BiAnn"
    ANNUAL = "Ann"
    INTERVAL_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (BIWEEKLY, "Biweekly"),
        (MONTHLY, "Monthly"),
        (QUARTERLY, "Quarterly"),
        (SEMI_ANNUAL, "Semiannually"),
        (ANNUAL, "Annually"),
    ]
    task = models.ForeignKey(Task, on_delete=models.RESTRICT)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)
    length = models.IntegerField()

    def __str__(self):
        return self.task

class Upload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    file_name = models.CharField(max_length=255)
    alt_txt = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now())
