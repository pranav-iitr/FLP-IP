from django.contrib import admin
from .models import User, organization, Drone

admin.site.register(User)
admin.site.register(organization)
admin.site.register(Drone)

# Register your models here.
