from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.courses, name="courses"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("courses/<int:pk>/buy/", views.start_payment, name="start_payment"),
    path("payment/success/", views.payment_success, name="payment_success"),
    path("payment/fail/", views.payment_fail, name="payment_fail"),
    path("payment/cancel/", views.payment_cancel, name="payment_cancel"),
    path("payment/ipn/", views.payment_ipn, name="payment_ipn"),
    path("courses/<int:pk>/update/", views.update_course, name="update_course"),
    path("courses/<int:pk>/delete/", views.delete_course, name="delete_course"),
    path("add/", views.add_course, name="add_course"),
    # My Courses: list the courses purchased by the logged-in user
    path("my-courses/", views.my_courses, name="my_courses"),
    # List all courses by a specific instructor (user)
    path("instructor/<int:user_id>/", views.instructor_courses, name="instructor_courses"),
]
