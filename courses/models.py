from django.db import models
from django.conf import settings


class Instructor(models.Model):
    name = models.CharField(max_length=100)
    credentials = models.CharField(max_length=200)
    # optional link to a user account (teacher). Not all instructors must be linked.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="instructor_profile",
    )

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    # The user who created / teaches this course. Use AUTH_USER_MODEL so
    # the 'instructor' is directly the teacher user account.
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="courses"
    )
    # rating and review_count removed — topics and subtopics moved to dedicated models
    enrollment_year = models.PositiveIntegerField()
    current_price = models.DecimalField(max_digits=6, decimal_places=2)
    original_price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(
        upload_to="course_images/", default="course_images/default.png", verbose_name="Course Image"
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ("python", "Python"),
            ("web-development", "Web Development"),
            ("sql", "SQL"),
            ("php", "PHP"),
        ],
        default="python",
    )

    def __str__(self):
        return self.title

    # legacy rating/review helpers removed

    def get_discount_percentage(self):
        if self.original_price > 0:
            discount = ((self.original_price - self.current_price) / self.original_price) * 100
            return f"{int(discount)}%"
        return "0%"


class Topic(models.Model):
    """A top-level topic within a Course."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class SubTopic(models.Model):
    """A sub-topic that belongs to a Topic."""

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subtopics")
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.name


class Payment(models.Model):
    """Simple payment record for SSLCOMMERZ transactions."""

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_email = models.EmailField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    currency = models.CharField(max_length=10, default="BDT")
    status = models.CharField(max_length=32, default="INIT")
    transaction_id = models.CharField(max_length=128, blank=True, null=True)
    session_key = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment({self.course.title} - {self.amount} {self.currency} - {self.status})"
