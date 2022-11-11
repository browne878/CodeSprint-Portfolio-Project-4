import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    company_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, null=True)
    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True)
    created_at = models.DateField(auto_now_add=True, null=True)


class UserProfile(models.Model):
    class Role(models.TextChoices):
        CLIENT = 'client', _('CLIENT')
        DEVELOPER = 'developer', _('DEVELOPER')
        ADMIN = 'admin', _('ADMIN')

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(
        max_length=9,
        choices=Role.choices,
        default=Role.CLIENT,
        null=True,
        blank=True)
    company_id = models.ForeignKey(
        Company,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True)
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True)


class Project(models.Model):
    project_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Sprint(models.Model):
    sprint_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    starts_at = models.DateField(null=True)
    ends_at = models.DateField(null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Case(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('PENDING')
        PLANNING = 'planning', _('PLANNING')
        IN_FE_DEVELOPMENT = 'in fe development', _('IN_FE_DEVELOPMENT')
        IN_BE_DEVELOPMENT = 'in be development', _('IN_BE_DEVELOPMENT')
        TESTING = 'testing', _('TESTING')
        COMPLETED = 'completed', _('COMPLETED')

    class Category(models.TextChoices):
        BUG = 'bug', _('BUG')
        FEATURE = 'feature', _('FEATURE')
        CHANGE = 'change', _('CHANGE')

    class Task_Size(models.TextChoices):
        VSMALL = 'very small', _('VSMALL')
        SMALL = 'small', _('SMALL')
        MEDIUM = 'medium', _('MEDIUM')
        LARGE = 'large', _('LARGE')
        VLARGE = 'very large', _('VLARGE')

    case_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=255, null=True)
    created_at = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(
        choices=Status.choices,
        max_length=30,
        default=Status.PENDING
    )
    category = models.CharField(
        choices=Category.choices,
        max_length=30,
        default=Category.FEATURE
    )
    due_date = models.DateField(null=True)
    task_size = models.CharField(
        choices=Task_Size.choices,
        max_length=30,
        default=Task_Size.MEDIUM)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True)
