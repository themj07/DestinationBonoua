# Generated by Django 5.1.6 on 2025-02-18 17:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0013_remove_commentairetourisme_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='commentairetourisme',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='commentaires', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='commentairetourisme',
            name='nom',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
