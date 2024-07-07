from django.contrib.auth.models import User
from django.db.models import (Model, CharField, ForeignKey, DO_NOTHING, ImageField, SET_NULL, TextField, DateField,
                              TextChoices, DateTimeField, BooleanField, OneToOneField)


class Position(Model):
    position = CharField(max_length=128)
    department = CharField(max_length=128)

    #class Meta:
        #ordering = ['position_name']

    def __str__(self):
        return self.position


class Profile(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    position = ForeignKey(Position, null=True, blank=True, on_delete=DO_NOTHING)
    picture = ImageField(upload_to="images/", default=None, null=False, blank=False)
    supervisor = ForeignKey('Profile', null=True, blank=True, on_delete=SET_NULL)
    bio = TextField(null=True, blank=True)

    #class Meta:
        #ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Priority(TextChoices):
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'


class Status(TextChoices):
    TODO = 'todo'
    DOING = 'doing'
    DONE = 'done'


class Goal(Model):
    name = CharField(max_length=32)
    description = TextField(null=True, blank=True)
    deadline = DateField(null=True, blank=True)
    priority = CharField(max_length=64, choices=Priority.choices, null=True, blank=True)
    status = CharField(max_length=10, choices=Status.choices, null=True, blank=True)

    #class Meta:
        #ordering = ['name', 'deadline']

    def __str__(self):
        return f"{self.name} ({self.deadline})"


class Review(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = CharField(max_length=500, null=True, blank=True)
    evaluator = ForeignKey(Profile, related_name='evaluations', on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, related_name='reviews', on_delete=DO_NOTHING)
    goal = CharField(max_length=500, null=True, blank=True)
    training = CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.subject_of_review} ({self.creation_date})"


class Task(Model):
    title=CharField(max_length=120)
    description = TextField(null=True, blank=True)
    creation_date = DateTimeField(auto_now_add=True)
    due_date = DateTimeField(default=None, null=True, blank=True)
    to_do_list = CharField(max_length=500, null=True, blank=True)
    creator = ForeignKey(Profile, on_delete=DO_NOTHING)
    completed = BooleanField(default=False)

    def __str__(self):
        return self.title


class Feedback(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = CharField(max_length=500, null=True, blank=True)
    evaluator = ForeignKey(Profile, related_name='given_feedback', on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, related_name='received_feedback', on_delete=DO_NOTHING)

    def __str__(self):
        return f"{self.subject_of_review} ({self.creation_date})"


