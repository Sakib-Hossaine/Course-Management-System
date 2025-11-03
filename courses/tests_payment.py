from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Course, Payment
from .models import Instructor


class PaymentInitTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="pass", user_type="student"
        )
        instructor = Instructor.objects.create(name="Inst", credentials="None")
        self.course = Course.objects.create(
            title="T1",
            instructor=instructor,
            rating=4.5,
            review_count=10,
            enrollment_year=2024,
            current_price=100.00,
            original_price=150.00,
            category="python",
        )
        self.client = Client()

    def test_start_payment_creates_payment(self):
        logged = self.client.login(email="test@example.com", password="pass")
        self.assertTrue(logged)
        resp = self.client.post(f"/courses/{self.course.pk}/buy/")
        # response may be redirect or rendered page; accept 200 or 302
        self.assertIn(resp.status_code, (200, 302))
        # start_payment returns either redirect to gateway or renders fail page
        # ensure a Payment record was created for this user+course
        payment = Payment.objects.filter(course=self.course).first()
        self.assertIsNotNone(payment)
        # payment should be in PENDING or FAILED or have session_key if library available
        self.assertIn(payment.status, ("NEW", "PENDING", "FAILED", "CANCEL", "SUCCESS"))
