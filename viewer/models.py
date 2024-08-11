from django.contrib.auth.models import User
from django.db.models import (Model, CharField, ForeignKey, DO_NOTHING, ImageField, SET_NULL, TextField, DateField,
                              TextChoices, DateTimeField, BooleanField, CASCADE, OneToOneField)

from django.db import models
from django.utils import timezone


class Position(Model):
    position = CharField(max_length=128)
    department = CharField(max_length=128)

    # class Meta:
    #     ordering = ['position_name']

    def __str__(self):
        return self.position


class Profile(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    position = ForeignKey(Position, null=True, blank=True, on_delete=DO_NOTHING)
    picture = ImageField(upload_to="images/", default=None, null=False, blank=False)
    supervisor = ForeignKey('Profile', null=True, blank=True, on_delete=SET_NULL, related_name='subordinate')
    bio = TextField(null=True, blank=True)

    # class Meta:
    #     ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_all_goals(self):
        return Goal.objects.filter(profile=self).order_by('-deadline')

    def get_all_reviews(self):
        return Review.objects.filter(subject_of_review=self).order_by('-creation_date')

    def get_picture(self):
        return self.picture


class Priority(TextChoices):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Status(TextChoices):
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'


class Goal(Model):
    profile = ForeignKey(Profile, on_delete=CASCADE)
    name = CharField(max_length=160)
    description = TextField(null=True, blank=True)
    deadline = DateField(null=True, blank=True)
    priority = CharField(max_length=64, choices=Priority.choices, null=True, blank=True)
    status = CharField(max_length=10, choices=Status.choices, null=True, blank=True)

    # class Meta:
    #     ordering = ['name', 'deadline']

    def __str__(self):
        return f"{self.name} ({self.deadline})"


class Review(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = TextField(null=True, blank=True)
    evaluator = ForeignKey(Profile, related_name='evaluations', on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, related_name='reviews', on_delete=DO_NOTHING)
    goal = CharField(max_length=500, null=True, blank=True)
    training = CharField(max_length=250, null=True, blank=True)

    # class Meta:
    #     ordering = ['-creation_date']

    def __str__(self):
        return f"{self.subject_of_review} ({self.creation_date})"


class Todo(Model):
    title = models.CharField(max_length=100)
    details = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return self.title


class Feedback(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = CharField(max_length=500, null=True, blank=True)
    evaluator = ForeignKey(Profile, related_name='given_feedback', on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, related_name='received_feedback', on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.subject_of_review} ({self.creation_date})"
