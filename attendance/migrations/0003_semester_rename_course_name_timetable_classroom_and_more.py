# Generated by Django 5.0.3 on 2024-10-08 08:42

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0002_remove_student_date_of_birth_remove_student_semester_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.RenameField(
            model_name='timetable',
            old_name='course_name',
            new_name='classroom',
        ),
        migrations.RemoveField(
            model_name='log',
            name='camera_id',
        ),
        migrations.RemoveField(
            model_name='log',
            name='image_path',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='teacher',
        ),
        migrations.AddField(
            model_name='log',
            name='attendance_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='log',
            name='image',
            field=models.ImageField(default='C:\\Users\\Admin\\Desktop\\finalproject\\facial_recognition_system\\imgs\\default.png', upload_to='captured_faces/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teacher',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='teacher_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='log',
            name='attendance_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='reportedface',
            name='face_image',
            field=models.ImageField(upload_to='reported_faces/'),
        ),
        migrations.AlterField(
            model_name='student',
            name='timetables',
            field=models.ManyToManyField(to='attendance.timetable'),
        ),
        migrations.AlterField(
            model_name='timetable',
            name='day_of_week',
            field=models.CharField(choices=[('Mon', 'Monday'), ('Tue', 'Tuesday'), ('Wed', 'Wednesday'), ('Thu', 'Thursday'), ('Fri', 'Friday')], max_length=10),
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=10, unique=True)),
                ('course_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('instructor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.teacher')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timetable',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.course'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='AttendanceReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendance_percentage', models.FloatField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.student')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.course')),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attendance.semester')),
            ],
        ),
        migrations.AddField(
            model_name='log',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.semester'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timetable',
            name='semester',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.semester'),
            preserve_default=False,
        ),
    ]