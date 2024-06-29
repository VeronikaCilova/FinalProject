from django.contrib.auth.models import User

from django.db.models import Model, CharField, EmailField, ForeignKey, DO_NOTHING, ImageField, SET_NULL
from django.forms import DateTimeField
from pip._vendor.distlib.markers import Evaluator


# Create your models here.
class Profile(Model):
    user = ForeignKey(User, on_delete=DO_NOTHING)
    position = ForeignKey(Position, null=True, blank=True, on_delete=DO_NOTHING)
    picture = ImageField(upload_to="images/", default=None, null=False, blank=False)
    supervisor = ForeignKey('Profile', null=True, blank=True, on_delete=SET_NULL)

    class Meta:
        ordering = ['surname', 'name']

    def __str__(self):
        return f'{self.user.first_name} ({self.user.last_name})'


class Review(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = CharField(max_length=500, null=True, blank=True)
    evaluator = ForeignKey(Profile, on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, on_delete=DO_NOTHING)
    goal = CharField(max_length=500, null=True, blank=True)
    training = CharField(max_length=250, null=True, blank=True)


class Task(Model):
    creation_date = DateTimeField(auto_now_add=True)
    note = CharField(max_length=500, null=True, blank=True)
    to_do_list = CharField(max_length=500, null=True, blank=True)
    creator = ForeignKey(Profile, on_delete=DO_NOTHING)


class Feedback(Model):
    creation_date = DateTimeField(auto_now_add=True)
    description = CharField(max_length=500, null=True, blank=True)
    evaluator = ForeignKey(Profile, on_delete=DO_NOTHING)
    subject_of_review = ForeignKey(Profile, on_delete=DO_NOTHING)




