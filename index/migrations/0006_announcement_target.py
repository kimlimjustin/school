# Generated by Django 3.0.8 on 2020-07-25 12:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_auto_20200725_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='target',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='target', to='index.Class'),
            preserve_default=False,
        ),
    ]