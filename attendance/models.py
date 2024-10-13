import bcrypt
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

class Semester(models.Model):
    name = models.CharField(max_length=255, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_code = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    instructor = models.ForeignKey('Teacher', on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return self.course_name


class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=10, choices=[
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday')
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='timetables')
    classroom = models.CharField(max_length=255)

    def clean(self):
        # Ensure start time is before end time
        if self.start_time >= self.end_time:
            raise ValidationError('End time must be after start time.')

    def __str__(self):
        return f"{self.course.course_name} ({self.get_day_of_week_display()})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    name = models.CharField(max_length=255)
    student_id = models.CharField(max_length=255, unique=True)
    face_encoding = models.BinaryField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    academic_year = models.CharField(max_length=9)
    department = models.CharField(max_length=255)
    enrollment_date = models.DateField()
    enrollment_status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    parent_name = models.CharField(max_length=255)
    parent_email = models.EmailField(max_length=255)
    parent_phone = models.CharField(max_length=20)
    emergency_contact_name = models.CharField(max_length=255)
    emergency_contact_phone = models.CharField(max_length=20)
    profile_picture = models.URLField(blank=True, null=True)
    timetables = models.ManyToManyField(Timetable, blank=True)

    def set_face_encoding(self, encoding):
        self.face_encoding = bcrypt.hashpw(encoding.encode('utf-8'), bcrypt.gensalt())

    def check_face_encoding(self, encoding):
        return bcrypt.checkpw(encoding.encode('utf-8'), self.face_encoding)

    def attendance_percentage(self, course, semester):
        logs = Log.objects.filter(student=self, course=course, semester=semester)
        total_classes = logs.count()
        present_classes = logs.filter(attendance_status='Present').count()
        return (present_classes / total_classes * 100) if total_classes > 0 else 0

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    name = models.CharField(max_length=255)
    teacher_id = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    hire_date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    subject = models.CharField(max_length=255)
    qualifications = models.TextField()
    profile_picture = models.URLField(blank=True, null=True)
    department = models.CharField(max_length=255)
    professional_development = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Log(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='captured_faces/')
    status = models.CharField(max_length=15, choices=[('Identified', 'Identified'), ('Unidentified', 'Unidentified')])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')])
    attendance_date = models.DateField()
    attendance_time = models.TimeField()
    reason_for_absence = models.CharField(max_length=255, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    system_status = models.CharField(max_length=15, choices=[('Operational', 'Operational'), ('Error', 'Error')])
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name} - {self.status}"


class ReportedFace(models.Model):
    face_image = models.ImageField(upload_to='reported_faces/')
    report_reason = models.TextField()
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reported by {self.reporter.username} at {self.reported_at}"


class AttendanceReport(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    attendance_percentage = models.FloatField()

    def __str__(self):
        return f"{self.student.name} - {self.course.course_name} - {self.semester.name} - {self.attendance_percentage}%"
