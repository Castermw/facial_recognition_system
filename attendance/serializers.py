from rest_framework import serializers
from .models import Student, Log, Course, Timetable, AttendanceReport

# Serializer for Student model
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'user', 'email', 'face_encoding', 'date_of_birth', 'course']  # Modify based on the Student model


# Serializer for Log model
class LogSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    semester_name = serializers.CharField(source='semester.name', read_only=True)

    class Meta:
        model = Log
        fields = [
            'id', 'student', 'student_name', 'course', 'course_name', 'semester', 'semester_name', 
            'attendance_status', 'attendance_time', 'reason_for_absence', 'system_status', 
            'notes', 'image', 'status', 'attendance_date', 'attendance_time'
        ]


# Serializer for Course model
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'course_code', 'description', 'teacher']  # Modify fields based on Course model


# Serializer for Timetable model
class TimetableSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.course_name', read_only=True)

    class Meta:
        model = Timetable
        fields = ['id', 'course', 'course_name', 'start_time', 'end_time', 'location']  # Modify based on Timetable model


# Serializer for AttendanceReport model
class AttendanceReportSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    course_name = serializers.CharField(source='course.course_name', read_only=True)
    attendance_time = serializers.TimeField(source='log.attendance_time', read_only=True)
    attendance_date = serializers.DateField(source='log.attendance_date', read_only=True)

    class Meta:
        model = AttendanceReport
        fields = ['id', 'student', 'student_name', 'course', 'course_name', 'attendance_status', 'attendance_date', 'attendance_time']
