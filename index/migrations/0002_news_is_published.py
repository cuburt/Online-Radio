# Generated by Django 2.2.4 on 2019-10-08 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(default=True),
        ),
    ]