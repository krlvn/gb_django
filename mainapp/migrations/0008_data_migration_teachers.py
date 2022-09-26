from django.db import migrations

def forwards_func(apps, schema_editor):
    Teachers = apps.get_model('mainapp', 'Teachers')

    Teachers.objects.create(
      name = 'Альфред',
      surname = 'Нуцубидзе',
      birth_date = '1990-07-10',
    ).course.set([1, 3])
    Teachers.objects.create(
      name = 'Роман',
      surname = 'Доржинов',
      birth_date = '1988-02-04',
    ).course.set([2, 4])
    Teachers.objects.create(
      name = 'Ярослав',
      surname = 'Конягин',
      birth_date = '1981-12-08',
    ).course.set([3, 5])
    Teachers.objects.create(
      name = 'Автандил',
      surname = 'Наварский',
      birth_date = '1983-05-16',
    ).course.set([4, 6])
    Teachers.objects.create(
      name = 'Роза',
      surname = 'Уланова',
      birth_date = '1986-05-09',
    ).course.set([5, 7])
    Teachers.objects.create(
      name = 'Бронислава',
      surname = 'Алиева',
      birth_date = '1971-01-07',
    ).course.set([6, 8])
    Teachers.objects.create(
      name = 'Диана',
      surname = 'Попова',
      birth_date = '1990-08-25',
    ).course.set([1, 8])

def reverse_func(apps, schema_editor):
    Teachers = apps.get_model('mainapp', 'Teachers')
    Teachers.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_data_migration_lessons'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
