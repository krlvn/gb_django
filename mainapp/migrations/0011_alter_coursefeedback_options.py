# Generated by Django 4.1.1 on 2022-10-03 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0010_coursefeedback'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursefeedback',
            options={'ordering': ('course', 'rating'), 'verbose_name': 'CourseFeedback', 'verbose_name_plural': 'CourseFeedbacks'},
        ),
    ]