# Generated by Django 5.0.3 on 2024-10-10 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_alter_semester_name_alter_student_face_encoding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='timetables',
            field=models.ManyToManyField(blank=True, to='attendance.timetable'),
        ),
    ]