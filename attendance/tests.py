from django.test import TestCase
from django.contrib.auth.models import User
from .models import Semester, Course, Timetable, Student, Teacher, Log, ReportedFace, AttendanceReport

class SemesterModelTest(TestCase):
    def setUp(self):
        self.semester = Semester.objects.create(name="Fall 2024", start_date="2024-09-01", end_date="2024-12-15")

    def test_semester_str(self):
        self.assertEqual(str(self.semester), "Fall 2024")

class CourseModelTest(TestCase):
    def setUp(self):
        self.teacher = Teacher.objects.create(
            user=User.objects.create(username='teacher1', password='password'),
            name='John Doe', teacher_id='T001', email='john.doe@example.com', phone_number='1234567890',
            gender='Male', hire_date='2020-01-01', status='Active', subject='Mathematics',
            qualifications='PhD in Mathematics', department='Mathematics'
        )
        self.course = Course.objects.create(course_code="MATH101", course_name="Calculus I", description="Basic Calculus", instructor=self.teacher)

    def test_course_str(self):
        self.assertEqual(str(self.course), "Calculus I")

class TimetableModelTest(TestCase):
    def setUp(self):
        self.semester = Semester.objects.create(name="Fall 2024", start_date="2024-09-01", end_date="2024-12-15")
        self.course = Course.objects.create(course_code="MATH101", course_name="Calculus I", instructor=Teacher.objects.create(
            user=User.objects.create(username='teacher1', password='password'),
            name='John Doe', teacher_id='T001', email='john.doe@example.com', phone_number='1234567890',
            gender='Male', hire_date='2020-01-01', status='Active', subject='Mathematics',
            qualifications='PhD in Mathematics', department='Mathematics'
        ))
        self.timetable = Timetable.objects.create(course=self.course, day_of_week='Mon', start_time='10:00:00', end_time='11:00:00', semester=self.semester, classroom='Room 101')

    def test_timetable_str(self):
        self.assertEqual(str(self.timetable), "Calculus I (Monday)")

class StudentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='student1', password='password')
        self.student = Student.objects.create(
            user=self.user,
            name='Jane Smith',
            student_id='S001',
            gender='Female',
            academic_year='2024-2025',
            department='Computer Science',
            enrollment_date='2024-01-15',
            enrollment_status='Active',
            parent_name='John Smith',
            parent_email='john.smith@example.com',
            parent_phone='9876543210',
            emergency_contact_name='Mary Smith',
            emergency_contact_phone='9876543210'
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), "Jane Smith")

class TeacherModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='teacher2', password='password')
        self.teacher = Teacher.objects.create(
            user=self.user,
            name='Alice Johnson',
            teacher_id='T002',
            email='alice.johnson@example.com',
            phone_number='1234567890',
            gender='Female',
            hire_date='2021-05-01',
            status='Active',
            subject='Physics',
            qualifications='MSc in Physics',
            department='Physics'
        )

    def test_teacher_str(self):
        self.assertEqual(str(self.teacher), "Alice Johnson")

class LogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='student2', password='password')
        self.student = Student.objects.create(
            user=self.user,
            name='Bob Brown',
            student_id='S002',
            gender='Male',
            academic_year='2024-2025',
            department='Mathematics',
            enrollment_date='2024-01-15',
            enrollment_status='Active',
            parent_name='John Brown',
            parent_email='john.brown@example.com',
            parent_phone='9876543210',
            emergency_contact_name='Mary Brown',
            emergency_contact_phone='9876543210'
        )
        self.semester = Semester.objects.create(name="Fall 2024", start_date="2024-09-01", end_date="2024-12-15")
        self.course = Course.objects.create(course_code="MATH101", course_name="Calculus I", instructor=Teacher.objects.create(
            user=User.objects.create(username='teacher1', password='password'),
            name='John Doe', teacher_id='T001', email='john.doe@example.com', phone_number='1234567890',
            gender='Male', hire_date='2020-01-01', status='Active', subject='Mathematics',
            qualifications='PhD in Mathematics', department='Mathematics'
        ))
        self.log = Log.objects.create(
            student=self.student,
            course=self.course,
            semester=self.semester,
            status='Identified',
            attendance_status='Present',
            attendance_date='2024-10-01',
            attendance_time='10:00:00',
            system_status='Operational'
        )

    def test_log_str(self):
        self.assertEqual(str(self.log), "Bob Brown - Calculus I - Identified")

class ReportedFaceModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='reporter', password='password')
        self.reported_face = ReportedFace.objects.create(
            face_image='path/to/image.jpg',  # Note: This is just a placeholder; you'll need to handle media files correctly in tests
            report_reason='Suspicious activity',
            reporter=self.user
        )

    def test_reported_face_str(self):
        self.assertIn("Reported by", str(self.reported_face))

class AttendanceReportModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='student3', password='password')
        self.student = Student.objects.create(
            user=self.user,
            name='Charlie Green',
            student_id='S003',
            gender='Male',
            academic_year='2024-2025',
            department='Computer Science',
            enrollment_date='2024-01-15',
            enrollment_status='Active',
            parent_name='John Green',
            parent_email='john.green@example.com',
            parent_phone='9876543210',
            emergency_contact_name='Mary Green',
            emergency_contact_phone='9876543210'
        )
        self.semester = Semester.objects.create(name="Fall 2024", start_date="2024-09-01", end_date="2024-12-15")
        self.course = Course.objects.create(course_code="CS101", course_name="Introduction to Programming", instructor=Teacher.objects.create(
            user=User.objects.create(username='teacher3', password='password'),
            name='Alice Johnson', teacher_id='T002', email='alice.johnson@example.com', phone_number='1234567890',
            gender='Female', hire_date='2021-05-01', status='Active', subject='Computer Science',
            qualifications='MSc in Computer Science', department='Computer Science'
        ))
        self.attendance_report = AttendanceReport.objects.create(student=self.student, course=self.course, semester=self.semester, attendance_percentage=95.0)

    def test_attendance_report_str(self):
        self.assertEqual(str(self.attendance_report), "Charlie Green - Introduction to Programming - Fall 2024 - 95.0%")
