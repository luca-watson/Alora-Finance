# Generated by Django 5.0.1 on 2024-04-01 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classroom', '0016_alter_lesson_assignment_lesson_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessons_completed',
            name='lesson_completed',
            field=models.BooleanField(default=False),
        ),
    ]
