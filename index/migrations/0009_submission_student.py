# Generated by Django 3.0.8 on 2020-07-28 02:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0008_submission_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
