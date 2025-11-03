from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser



def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/signup.html', {'form': form})

def teacher_class_call(request):
    return render(request, 'users/teacherclasscall.html')

def edit_student_profile(request):
    student = request.user
    if request.method == 'POST':
        # Update fields from POST data
        student.class_name = request.POST.get('class_name', student.class_name)
        student.school_name = request.POST.get('school_name', student.school_name)
        student.address = request.POST.get('address', student.address)
        student.parent_phone = request.POST.get('parent_phone', student.parent_phone)
        email = request.POST.get('email', student.email)
        if email:
            student.email = email
            if hasattr(student, 'user'):
                student.user.email = email
                student.user.save()
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            student.profile_picture = request.FILES['profile_picture']
        student.save()
        return redirect('users:student_profile')
    return render(request, 'users/edit_student_profile.html', {'student': student})

@login_required
def edit_teacher_profile(request):
    teacher = request.user
    if request.method == 'POST':
        teacher.qualification = request.POST.get('qualification', teacher.qualification)
        teacher.subjects_taught = request.POST.get('subjects_taught', teacher.subjects_taught)
        teacher.address = request.POST.get('address', teacher.address)
        teacher.phone_number = request.POST.get('phone_number', teacher.phone_number)
        email = request.POST.get('email', teacher.email)
        if email:
            teacher.email = email
        if 'profile_picture' in request.FILES:
            teacher.profile_picture = request.FILES['profile_picture']
        teacher.save()
        return redirect('users:teacher_profile')
    return render(request, 'users/edit_teacher_profile.html', {'teacher': teacher})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = request.POST.get('username')  # This is the email field
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)  # <-- FIXED HERE
            if user is not None:
                login(request, user)
                # Redirect based on user_type
                if user.user_type == 'student':
                    return redirect('users:student_profile')
                elif user.user_type == 'teacher':
                    return redirect('users:teacher_profile')
        else:
            print(form.errors)  # Add this for debugging
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')

@login_required
def student_profile(request):
    student = request.user
    return render(request, 'users/studentProfile.html', {'student': student})

@login_required
def teacher_profile(request):
    teacher = request.user
    return render(request, 'users/teacherProfile.html', {'teacher': teacher})

def student_marks(request):
    return render(request, 'users/student_marks.html')

# Create your views here.
def learner(request):
    return render(request, "users/learner.html")


def teacher(request):
    return render(request, "users/teacher.html")





# Contact Page View
def contact(request):
    return render(request, "users/contact.html")









