from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'rating', 'review_count', 'enrollment_year', 'current_price', 'original_price', 'category', 'image']

class CourseUpdateForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title', 'rating', 'review_count', 'enrollment_year',
            'current_price', 'original_price', 'image', 'category', 'instructor'
        ]

class CourseDeleteForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = []  # No fields needed, just for confirmation