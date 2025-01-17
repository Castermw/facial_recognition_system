# Generated by Django 5.0.3 on 2024-10-10 10:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0005_alter_student_timetables'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='instructor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='attendance.teacher'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='attendance.course'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timetables', to='attendance.semester'),
        ),
    ]
