from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    # Topic and sub-topic inputs are handled separately in the template as dynamic fields.

    class Meta:
        model = Course
        # rating and review_count removed per requirements; topics/subtopics are collected separately
        fields = [
            "title",
            "instructor",
            "enrollment_year",
            "current_price",
            "original_price",
            "category",
            "image",
        ]


class CourseUpdateForm(forms.ModelForm):
    # Topics/subtopics are provided using the dynamic topic UI in the template and
    # handled in the view (Topic/SubTopic models).

    class Meta:
        model = Course
        fields = [
            "title",
            "enrollment_year",
            "current_price",
            "original_price",
            "image",
            "category",
            "instructor",
        ]


class CourseDeleteForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = []  # No fields needed, just for confirmation
