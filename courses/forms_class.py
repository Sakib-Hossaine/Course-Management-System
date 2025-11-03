from django import forms
from .models_class import SchoolClass, ClassCategory


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = ["category", "description", "student_limit"]


class JoinClassForm(forms.Form):
    class_id = forms.IntegerField(widget=forms.HiddenInput())
