# Generated by Django 3.0.2 on 2020-09-12 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0002_auto_20200911_1816'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teacher',
            old_name='class_teachers',
            new_name='classroom',
        ),
        migrations.RenameField(
            model_name='teacher',
            old_name='subject_teachers',
            new_name='subject',
        ),
    ]