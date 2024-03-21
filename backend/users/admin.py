from django.contrib import admin
from .models import User, organization, Drone

class DroneAdmin(admin.ModelAdmin):
    # List of fields to be displayed in the change form
    list_display = ( 'name', 'description','organization'  ,'image')

    # List of fields to be displayed in the change form, but as read-only
    readonly_fields = ('secret','joinning_url','id')


admin.site.register(User)
admin.site.register(organization)
admin.site.register(Drone,DroneAdmin)

# Register your models here.
