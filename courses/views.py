from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from .forms import CourseDeleteForm
from .forms import CourseUpdateForm
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from .models import Payment
import requests

try:
    from sslcommerz_python.payment import SSLCSession
except Exception:
    SSLCSession = None


# Courses Page View
def courses(request):
    courses = Course.objects.all()
    print(courses)
    return render(request, "courses/courses.html", {"courses": courses})


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, "courses/course details.html", {"course": course})


# In your courses/views.py
def add_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("courses")  # or wherever you want to redirect
    else:
        form = CourseForm()
    return render(request, "courses/addcourses.html", {"form": form})


def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseUpdateForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect("course_detail", course.id)
    else:
        form = CourseUpdateForm(instance=course)
    return render(request, "courses/updatecourse.html", {"form": form, "course": course})


def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course.delete()
        return redirect("courses")
    form = CourseDeleteForm(instance=course)
    return render(request, "courses/coursedelete.html", {"form": form, "course": course})


def start_payment(request, pk):
    """Create a payment record and initialize SSLCOMMERZ payment session."""
    course = get_object_or_404(Course, pk=pk)
    if not request.user.is_authenticated:
        # settings.LOGIN_URL may be a named URL (e.g. 'users:login') or a path.
        from django.urls import reverse, NoReverseMatch

        login_setting = settings.LOGIN_URL
        try:
            login_path = reverse(login_setting)
        except NoReverseMatch:
            # LOGIN_URL is probably a path already
            login_path = login_setting

        return redirect(f"{login_path}?next={request.path}")

    # create payment record
    email = request.user.email if hasattr(request.user, "email") else request.POST.get("email", "")
    amount = course.current_price
    payment = Payment.objects.create(course=course, user_email=email, amount=amount, currency="BDT")

    if SSLCSession is None:
        # Library not installed - show instructions
        return render(
            request,
            "courses/payment_fail.html",
            {"message": "SSLCOMMERZ library not installed. Please pip install sslcommerz-python."},
        )

    sslc = SSLCSession(
        sslc_is_sandbox=settings.SSLCOMMERZ.get("IS_SANDBOX", True),
        sslc_store_id=settings.SSLCOMMERZ.get("STORE_ID"),
        sslc_store_pass=settings.SSLCOMMERZ.get("STORE_PASS"),
    )

    # set urls
    host = request.get_host()
    scheme = "https" if request.is_secure() else "http"
    success_url = scheme + "://" + host + redirect_url_path(request, "payment_success")
    fail_url = scheme + "://" + host + redirect_url_path(request, "payment_fail")
    cancel_url = scheme + "://" + host + redirect_url_path(request, "payment_cancel")
    ipn_url = scheme + "://" + host + redirect_url_path(request, "payment_ipn")

    sslc.set_urls(
        success_url=success_url, fail_url=fail_url, cancel_url=cancel_url, ipn_url=ipn_url
    )

    sslc.set_product_integration(
        total_amount=Decimal(str(amount)),
        currency="BDT",
        product_category=str(course.category),
        product_name=course.title,
        num_of_item=1,
        shipping_method="NO",
        product_profile="general",
    )

    display_name = getattr(request.user, "get_full_name", None)
    if callable(display_name):
        display_name = request.user.get_full_name() or request.user.username
    else:
        display_name = getattr(request.user, "username", getattr(request.user, "email", ""))

    # determine phone: prefer user profile, else use sandbox test phone fallback
    user_phone = getattr(request.user, "phone_number", None) or getattr(
        request.user, "parent_phone", None
    )
    if not user_phone:
        # fallback to configured test phone for sandbox environments
        user_phone = settings.SSLCOMMERZ.get("TEST_CUSTOMER_PHONE", "")

    if not user_phone:
        # inform frontend that phone is required for payment initiation
        payment.status = "FAILED"
        payment.save()
        return render(
            request,
            "courses/payment_fail.html",
            {
                "message": "Customer phone number is required to start payment. Please add a phone number to your profile."
            },
        )

    sslc.set_customer_info(
        name=display_name,
        email=email,
        phone=user_phone,
        address1="",
        address2="",
        city="",
        postcode="",
        country="",
    )

    response_data = sslc.init_payment()

    status = response_data.get("status") if isinstance(response_data, dict) else None
    if status == "SUCCESS":
        payment.session_key = response_data.get("sessionkey")
        payment.save()
        gateway_url = response_data.get("GatewayPageURL")
        return redirect(gateway_url)
    else:
        payment.status = "FAILED"
        payment.save()
        reason = (
            response_data.get("failedreason")
            if isinstance(response_data, dict)
            else "Unknown error"
        )
        return render(request, "courses/payment_fail.html", {"message": reason})


def redirect_url_path(request, name):
    """Helper to reverse named url path to path portion only."""
    from django.urls import reverse

    path = reverse(name)
    return path


@csrf_exempt
def payment_success(request):
    # SSLCOMMERZ will POST back with transaction details
    data = request.POST.dict() if request.method == "POST" else request.GET.dict()
    sessionkey = data.get("sessionkey")
    tran_id = data.get("tran_id")
    # Server-side verification before accepting
    verified = False
    try:
        store_id = settings.SSLCOMMERZ.get("STORE_ID")
        store_pass = settings.SSLCOMMERZ.get("STORE_PASS")
        base = settings.SSLCOMMERZ.get("VALIDATION_API")
        if tran_id and store_id and store_pass:
            r = requests.get(
                base,
                params={"tran_id": tran_id, "store_id": store_id, "store_passwd": store_pass},
                timeout=10,
            )
            if r.status_code == 200:
                # response may be JSON or URL-encoded; try JSON first
                try:
                    resp = r.json()
                except Exception:
                    resp = None
                if resp and resp.get("status") in ("VALID", "VALIDATED", "SUCCESS"):
                    verified = True
    except Exception:
        verified = False

    # find payment by sessionkey
    payment = Payment.objects.filter(session_key=sessionkey).first()
    if payment:
        if verified:
            payment.status = "SUCCESS"
        else:
            payment.status = "PENDING"
        payment.transaction_id = tran_id
        payment.save()
    return render(request, "courses/payment_success.html", {"data": data})


@csrf_exempt
def payment_fail(request):
    data = request.POST.dict() if request.method == "POST" else request.GET.dict()
    sessionkey = data.get("sessionkey")
    payment = Payment.objects.filter(session_key=sessionkey).first()
    if payment:
        payment.status = "FAILED"
        payment.save()
    return render(
        request,
        "courses/payment_fail.html",
        {"data": data, "message": "Payment failed or canceled."},
    )


@csrf_exempt
def payment_cancel(request):
    data = request.POST.dict() if request.method == "POST" else request.GET.dict()
    sessionkey = data.get("sessionkey")
    payment = Payment.objects.filter(session_key=sessionkey).first()
    if payment:
        payment.status = "CANCEL"
        payment.save()
    return render(
        request, "courses/payment_fail.html", {"data": data, "message": "Payment canceled by user."}
    )


@csrf_exempt
def payment_ipn(request):
    # Instant Payment Notification - SSLCOMMERZ will POST here
    data = request.POST.dict()
    # log or process IPN; match by sessionkey or tran_id
    sessionkey = data.get("sessionkey")
    tran_id = data.get("tran_id")
    payment = Payment.objects.filter(session_key=sessionkey).first()
    if payment:
        payment.status = data.get("status", payment.status)
        payment.transaction_id = tran_id or payment.transaction_id
        payment.save()
    # respond 200
    from django.http import HttpResponse

    return HttpResponse("IPN received")
