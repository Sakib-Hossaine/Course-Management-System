from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models_class import SchoolClass, ClassCategory
from .forms_class import SchoolClassForm, JoinClassForm


@login_required
def class_list(request):
    classes = SchoolClass.objects.select_related("category", "teacher").all()
    return render(request, "courses/class_list.html", {"classes": classes})


@login_required
def add_class(request):
    if request.user.user_type != "teacher":
        messages.error(request, "Only teachers can add classes.")
        return redirect("class_list")
    if request.method == "POST":
        form = SchoolClassForm(request.POST)
        if form.is_valid():
            school_class = form.save(commit=False)
            school_class.teacher = request.user
            school_class.save()
            messages.success(request, "Class created successfully!")
            return redirect("class_list")
    else:
        form = SchoolClassForm()
    return render(request, "courses/class_form.html", {"form": form, "action": "Add"})


@login_required
def edit_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.user != school_class.teacher:
        messages.error(request, "Only the class teacher can edit this class.")
        return redirect("class_list")
    if request.method == "POST":
        form = SchoolClassForm(request.POST, instance=school_class)
        if form.is_valid():
            form.save()
            messages.success(request, "Class updated successfully!")
            return redirect("class_list")
    else:
        form = SchoolClassForm(instance=school_class)
    return render(request, "courses/class_form.html", {"form": form, "action": "Edit"})


@login_required
def delete_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.user != school_class.teacher:
        messages.error(request, "Only the class teacher can delete this class.")
        return redirect("class_list")
    if request.method == "POST":
        school_class.delete()
        messages.success(request, "Class deleted successfully!")
        return redirect("class_list")
    return render(request, "courses/class_confirm_delete.html", {"school_class": school_class})


@login_required
def join_class(request, class_id):
    school_class = get_object_or_404(SchoolClass, id=class_id)
    if request.user.user_type != "student":
        messages.error(request, "Only students can join classes.")
        return redirect("class_list")
    if school_class.is_full():
        messages.error(request, "This class is already full.")
        return redirect("class_list")
    if request.user in school_class.students.all():
        messages.info(request, "You have already joined this class.")
        return redirect("class_list")
    school_class.students.add(request.user)
    messages.success(request, "You have joined the class!")
    return redirect("class_list")
