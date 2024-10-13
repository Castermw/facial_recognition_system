from django.contrib import admin
from .models import Semester, Course, Timetable, Student, Teacher, Log, ReportedFace, AttendanceReport

# Optionally, define custom admin classes
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'academic_year', 'enrollment_status')
    search_fields = ('name', 'student_id', 'parent_name', 'parent_email')
    
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher_id', 'email', 'department', 'status')
    search_fields = ('name', 'teacher_id', 'email')

class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'instructor')
    search_fields = ('course_code', 'course_name')

class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'day_of_week', 'start_time', 'end_time', 'semester', 'classroom')
    search_fields = ('course__course_name', 'day_of_week', 'semester__name')

class LogAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'attendance_status', 'attendance_date', 'attendance_time')
    search_fields = ('student__name', 'course__course_name', 'semester__name')

# Register your models with the admin site
admin.site.register(Semester)
admin.site.register(Course, CourseAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(ReportedFace)
admin.site.register(AttendanceReport)
