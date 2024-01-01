from django.contrib import admin
from .models import User, organization, team_member, drone

admin.site.register(User)
admin.site.register(organization)
admin.site.register(team_member)
admin.site.register(drone)

# Register your models here.
