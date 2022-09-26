from django.db import migrations

def forwards_func(apps, schema_editor):
    Lessons = apps.get_model('mainapp', 'Lessons')

    Lessons.objects.create(
      course_id = 1,
      num = 1,
      title = 'Lesson 1',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 2,
      title = 'Lesson 2',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 3,
      title = 'Lesson 3',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 4,
      title = 'Lesson 4',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 5,
      title = 'Lesson 5',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 6,
      title = 'Lesson 6',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 7,
      title = 'Lesson 7',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 1,
      num = 8,
      title = 'Lesson 8',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 1,
      title = 'Lesson 1',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 2,
      title = 'Lesson 2',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 3,
      title = 'Lesson 3',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 4,
      title = 'Lesson 4',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 5,
      title = 'Lesson 5',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 6,
      title = 'Lesson 6',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 7,
      title = 'Lesson 7',
      description = 'Описание урока',
    )
    Lessons.objects.create(
      course_id = 2,
      num = 8,
      title = 'Lesson 8',
      description = 'Описание урока',
    )

def reverse_func(apps, schema_editor):
    Lessons = apps.get_model('mainapp', 'Lessons')
    Lessons.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0006_data_migration_courses'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
