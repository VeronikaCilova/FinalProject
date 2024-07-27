from django.contrib import admin

from viewer.models import Profile, Position, Goal, Review

# Register your models here.
admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(Goal)
admin.site.register(Review)
