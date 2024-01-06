from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission,BaseUserManager

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

class time_stamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True # This is an abstract class, so it will not be created in the database
    

# Create your models here.
class User(AbstractUser):
    # Some rules adding username
    status_choices = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("blocked", "Blocked"),          ]
    username_validator = UnicodeUsernameValidator()
    phone_no = models.CharField(max_length=10, blank=True)
    #Custom Field
    email = models.EmailField(_('email'), max_length=80, unique=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
        blank=True # Same code that has django as a default only added this to say can be an empty value
    )
  
    # Field for login
    USERNAME_FIELD = 'email'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)    
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    
    # Field for command createsuperuser
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return f"{self.email}"
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

class organization(time_stamp):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    capacity = models.IntegerField( default=20) # default capacity is 20
    
    class Meta:
        verbose_name_plural = "Organizations"

class team_member(time_stamp):
    statusOptions = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('removed', 'Removed'),
        ('blocked', 'Blocked')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE, related_name="organization")
    status = models.CharField(max_length=50, choices=statusOptions, default='pending')
    class Meta:
        verbose_name_plural = "Team Members"

class drone(time_stamp):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    organization = models.ForeignKey(organization, on_delete=models.CASCADE, related_name="organization_drone")
    joinning_url = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Drones"
    



