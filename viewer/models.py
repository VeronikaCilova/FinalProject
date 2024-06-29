from django.contrib.auth.models import User

from django.db.models import Model, CharField, EmailField, ForeignKey, DO_NOTHING, ImageField


# Create your models here.
class User(Model):
    name = CharField(max_length=64)
    surname = CharField(max_length=64)
    email = EmailField(max_length=254, unique=True)
    position = ForeignKey(Position, null=True, blank=True, on_delete=DO_NOTHING)
    picture = ImageField(upload_to="images/", default=None, null=False, blank=False)
    supervisor = ForeignKey(User, null=True, blank=False, on_delete=DO_NOTHING)
#   password = CharField(max_length=64)

    class Meta:
        ordering = ['surname', 'name']

    def __str__(self):
        return f'{self.name} ({self.surname})'
