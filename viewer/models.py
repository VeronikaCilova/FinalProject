from django.contrib.auth.models import User

from django.db.models import Model, CharField, EmailField, ForeignKey, DO_NOTHING, ImageField, SET_NULL, TextField, \
    DateField, TextChoices


class Position(Model):
    position_name = CharField(max_length=128)
    department = CharField(max_length=128)

    class Meta:
        ordering = ['position_name']

    def __str__(self):
        return self.position_name


class Profile(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    position = ForeignKey(Position, null=True, blank=True, on_delete=DO_NOTHING)
    picture = ImageField(upload_to="images/", default=None, null=False, blank=False)
    supervisor = ForeignKey('Profile', null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['surname', 'name']

    def __str__(self):
        return f'{self.user.first_name} ({self.user.last_name})'


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

    class Meta:
        ordering = ['name', 'deadline']

    def __str__(self):
        return f"{self.name} ({self.deadline})"
