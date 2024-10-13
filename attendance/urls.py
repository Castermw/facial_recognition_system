from django.urls import path
from .views import (
    register_student,
    live_feed,
    report_face,
    view_attendance_report,
    export_attendance_report
)
from .api_views import (
    StudentListCreateAPIView,
    StudentDetailAPIView,
    LogListCreateAPIView,
    LogDetailAPIView,
    CourseListCreateAPIView,
    CourseDetailAPIView,
    TimetableListCreateAPIView,
    TimetableDetailAPIView,
    AttendanceReportListCreateAPIView,
    AttendanceReportDetailAPIView
)

urlpatterns = [
    path('register_student/', register_student, name='register_student'),
    path('live_feed/', live_feed, name='live_feed'),
    path('report_face/<int:log_id>/', report_face, name='report_face'),
    path('attendance_report/', view_attendance_report, name='attendance_report'),
    path('export_attendance_report/<str:format>/', export_attendance_report, name='export_attendance_report'),
    
    # API URLs
    path('api/students/', StudentListCreateAPIView.as_view(), name='student-list-create'),
    path('api/students/<int:pk>/', StudentDetailAPIView.as_view(), name='student-detail'),
    path('api/logs/', LogListCreateAPIView.as_view(), name='log-list-create'),
    path('api/logs/<int:pk>/', LogDetailAPIView.as_view(), name='log-detail'),
    path('api/courses/', CourseListCreateAPIView.as_view(), name='course-list-create'),
    path('api/courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),
    path('api/timetables/', TimetableListCreateAPIView.as_view(), name='timetable-list-create'),
    path('api/timetables/<int:pk>/', TimetableDetailAPIView.as_view(), name='timetable-detail'),
    path('api/attendance-reports/', AttendanceReportListCreateAPIView.as_view(), name='attendance-report-list-create'),
    path('api/attendance-reports/<int:pk>/', AttendanceReportDetailAPIView.as_view(), name='attendance-report-detail'),
]
