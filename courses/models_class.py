from django.db import models
from django.conf import settings


class ClassCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    category = models.ForeignKey(ClassCategory, on_delete=models.CASCADE, related_name="classes")
    description = models.TextField(blank=True)
    student_limit = models.PositiveIntegerField(default=30)
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="joined_classes", blank=True
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="taught_classes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category.name} ({self.teacher.username})"

    @property
    def current_student_count(self):
        return self.students.count()

    def is_full(self):
        return self.current_student_count >= self.student_limit
