from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student, Log, Course, Timetable, AttendanceReport
from .serializers import StudentSerializer, LogSerializer, CourseSerializer, TimetableSerializer, AttendanceReportSerializer

# Student APIs
class StudentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

# Log APIs
class LogListCreateAPIView(generics.ListCreateAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

class LogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

# Course APIs
class CourseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

# Timetable APIsHere’s the complete implementation for the API views section that follows the structure of your original code, providing all necessary functionality:

### API Views (`api_views.py`)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Student, Log, Course, Timetable, AttendanceReport
from .serializers import StudentSerializer, LogSerializer, CourseSerializer, TimetableSerializer, AttendanceReportSerializer

# Student APIs
class StudentListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create students."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

class StudentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a student."""
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]

# Log APIs
class LogListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create logs."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

class LogDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a log."""
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [IsAuthenticated]

# Course APIs
class CourseListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create courses."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class CourseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a course."""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

# Timetable APIs
class TimetableListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create timetables."""
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]

class TimetableDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete a timetable."""
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]

# Attendance Report APIs
class AttendanceReportListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create attendance reports."""
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    permission_classes = [IsAuthenticated]

class AttendanceReportDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, or delete an attendance report."""
    queryset = AttendanceReport.objects.all()
    serializer_class = AttendanceReportSerializer
    permission_classes = [IsAuthenticated]
