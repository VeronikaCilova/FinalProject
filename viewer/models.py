from django.contrib.auth.models import User

from django.db.models import Model, CharField, EmailField, ForeignKey, DO_NOTHING, ImageField, SET_NULL


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
