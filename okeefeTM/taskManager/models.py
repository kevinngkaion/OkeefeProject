from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def get_admin_user():
    return User.objects.get(username='admin')

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
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    ANNUAL = "Annual"
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
    INTERVAL_CHOICES = [
        ('', 'Interval'),
        (DAILY, "Day(s)"),
        (WEEKLY, "Week(s)"),
        (MONTHLY, "Month(s)"),
        (ANNUAL, "Year(s)"),
    ] 
    user = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True, default=get_admin_user)
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
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES, null=True, blank=True)
    intervalLength = models.IntegerField(null=True, blank=True)


    def __str__(self):
      return self.name


class Upload(models.Model):
    task = models.ForeignKey(Task, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    file_name = models.CharField(max_length=255)
    alt_txt = models.CharField(max_length=255)
    time = models.DateTimeField(default=timezone.now())


class UserDepartment(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, unique=True)
    department = models.ForeignKey(Department, on_delete=models.RESTRICT)

    def __str__(self):
        return "User: " + self.user.get_username() + " | Deparment: " + self.department.name

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.token}"
