from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'name',
            'student_id',
            'gender',
            'academic_year',
            'department',
            'enrollment_date',
            'enrollment_status',
            'parent_name',
            'parent_email',
            'parent_phone',
            'emergency_contact_name',
            'emergency_contact_phone',
            'profile_picture',
            'timetables',
        ]
        # Exclude 'face_encoding' as it is non-editable
        exclude = ['face_encoding']

    def clean_parent_email(self):
        email = self.cleaned_data.get('parent_email')
        if Student.objects.filter(parent_email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_face_encoding(self):
        # Keep the validation logic but do not render the field
        face_encoding = self.cleaned_data.get('face_encoding')
        if not face_encoding:
            raise forms.ValidationError("Face encoding is required.")
        return face_encoding
