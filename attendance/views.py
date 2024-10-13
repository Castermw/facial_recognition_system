from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import (
    Student, Teacher, Log, ReportedFace,
    Course, AttendanceReport, Timetable, Semester
)
from .forms import StudentForm  # Assuming you create a form class for Student
from django.http import HttpResponse
import cv2
import face_recognition
from django.utils import timezone
import logging
import time
import csv
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage  # For image storage
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Attendance System</h1>")

# Configure logging
logger = logging.getLogger(__name__)

@login_required
@permission_required('attendance.add_student', raise_exception=True)
def register_student(request):
    """Register a new student with the provided details."""
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save(commit=False)
            student.user = request.user
            student.save()
            logger.info(f"Student registered: {student.name}")
            return redirect('student_list')
        else:
            logger.error(f"Form validation failed: {form.errors}")
    else:
        form = StudentForm()
    return render(request, 'register_student.html', {'form': form})

@login_required
@permission_required('attendance.view_log', raise_exception=True)
def live_feed(request):
    """Display a live video feed for face recognition."""
    video_capture = cv2.VideoCapture(0)
    
    # Check if the camera opened successfully
    if not video_capture.isOpened():
        logger.error("Camera could not be opened.")
        return HttpResponse("Camera not accessible.", status=500)

    known_face_encodings, known_face_names = fetch_known_faces()

    retry_attempts = 3
    retry_delay = 2
    for attempt in range(retry_attempts):
        if known_face_encodings:
            break
        logger.warning("Failed to fetch known faces, retrying...")
        time.sleep(retry_delay)
        retry_delay *= 2

    if not known_face_encodings:
        logger.warning("Using default face encodings due to failure to fetch known faces.")

    while True:
        ret, frame = video_capture.read()
        if not ret:
            logger.error("Error reading camera frame. Exiting live feed.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                log_attendance(name)
            else:
                log_entry = log_unidentified_face(frame)
                return redirect('report_face', log_id=log_entry.id)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()
    return HttpResponse("Live feed ended.")

def fetch_known_faces():
    """Fetch known face encodings and names from the database."""
    try:
        students = Student.objects.filter(face_encoding__isnull=False)
        known_face_encodings = [student.face_encoding for student in students]
        known_face_names = [student.name for student in students]
        return known_face_encodings, known_face_names
    except Exception as e:
        logger.error(f"Error fetching known faces: {e}")
        return [], []

def log_unidentified_face(frame):
    """Log an unidentified face by saving its image."""
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    image_filename = f"unidentified/{timestamp}.jpg"
    try:
        file_path = default_storage.save(image_filename, ContentFile(cv2.imencode('.jpg', frame)[1].tobytes()))
        log_entry = Log.objects.create(image=file_path, status='Unidentified')
        logger.info(f"Unidentified face logged: {file_path}")
        return log_entry
    except Exception as e:
        logger.error(f"Error saving unidentified face image: {e}")
        return None

def log_attendance(student_name):
    """Log attendance for a recognized student."""
    try:
        student = Student.objects.get(name=student_name)
        current_time = timezone.now()
        timetable_entry = Timetable.objects.filter(
            start_time__lte=current_time,
            end_time__gte=current_time
        ).first()

        if not timetable_entry:
            logger.warning(f"No timetable entry found for student: {student.name} at {current_time}.")
            return

        course = timetable_entry.course
        semester = Semester.objects.filter(
            start_date__lte=current_time,
            end_date__gte=current_time
        ).first()

        if not semester:
            logger.warning(f"No active semester found for student: {student.name} at {current_time}.")
            return

        attendance_status = 'Present'

        Log.objects.create(
            student=student,
            course=course,
            semester=semester,
            attendance_status=attendance_status,
            attendance_date=current_time.date(),
            attendance_time=current_time.time(),
            reason_for_absence=None,
            system_status='Operational',
            notes=''
        )
        logger.info(f"Attendance logged for {student.name}")
    except Student.DoesNotExist:
        logger.error(f"Student with name {student_name} does not exist.")
    except Exception as e:
        logger.error(f"Error logging attendance for {student_name}: {e}")

@login_required
@permission_required('attendance.report_face', raise_exception=True)
def report_face(request, log_id):
    """Report an unidentified face."""
    log_entry = get_object_or_404(Log, id=log_id)

    if request.method == 'POST':
        report_reason = request.POST.get('reason')
        if not report_reason:
            logger.error("Report reason is required.")
            return render(request, 'report_face.html', {'log_entry': log_entry, 'error': "Reason is required."})

        reported_face = ReportedFace(
            face_image=log_entry.image,
            report_reason=report_reason,
            reporter=request.user
        )
        reported_face.save()
        logger.info(f"Face reported: {log_entry.image} - Reason: {report_reason}")
        return redirect('live_feed')

    return render(request, 'report_face.html', {'log_entry': log_entry})

@login_required
@permission_required('attendance.view_attendance_report', raise_exception=True)
def view_attendance_report(request):
    """View attendance reports for students."""
    if request.user.groups.filter(name='Teachers').exists():
        reports = AttendanceReport.objects.all()
    else:
        reports = AttendanceReport.objects.filter(student__user=request.user)

    return render(request, 'attendance_report.html', {'reports': reports})

@login_required
@permission_required('attendance.export_attendance_report', raise_exception=True)
def export_attendance_report(request, format):
    """Export attendance report in specified format."""
    if format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="attendance_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Student Name', 'Course', 'Semester', 'Status', 'Date'])

        attendance_data = Log.objects.all().values_list(
            'student__name', 'course__course_name', 'semester__name', 
            'attendance_status', 'attendance_time'
        )

        for row in attendance_data:
            writer.writerow(row)

        logger.info("Attendance report exported as CSV.")
        return response
    else:
        logger.error("Unsupported export format requested.")
        return HttpResponse("Unsupported format", status=400)
