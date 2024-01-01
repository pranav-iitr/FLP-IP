# Generated by Django 5.0 on 2024-01-01 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_organization_drone_team_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='team_member',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('removed', 'Removed'), ('blocked', 'Blocked')], default='pending', max_length=50),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_no',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
