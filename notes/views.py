import os
from django.urls import reverse
from django.contrib import messages
from django.http import FileResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note, Report

from .forms import NoteForm


def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or getattr(request.user, "user_type", None) != "teacher"
        ):
            return HttpResponseRedirect(reverse("notes"))
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def notes(request):
    notes = Note.objects.all().order_by("-upload_date")
    return render(request, "notes/notes.html", {"notes": notes})


@login_required
@teacher_required
def add_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, "Note added successfully.")
            return HttpResponseRedirect(reverse("notes"))
    else:
        form = NoteForm()
    return render(request, "notes/note_form.html", {"form": form, "action": "Add"})


@login_required
@teacher_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return HttpResponseRedirect(reverse("notes"))
    else:
        form = NoteForm(instance=note)
    return render(request, "notes/note_form.html", {"form": form, "action": "Edit"})


@login_required
@teacher_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return HttpResponseRedirect(reverse("notes"))
    return render(request, "notes/note_confirm_delete.html", {"note": note})


@login_required
def download_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    try:
        file_path = note.file.path
    except ValueError:
        raise Http404("File path is invalid.")

    if os.path.exists(file_path):
        note.download_count = note.download_count + 1
        note.save(update_fields=["download_count"])
        return FileResponse(
            open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path)
        )
    else:
        raise Http404("File not found.")


@login_required
def report_note(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, id=note_id)
        reason = request.POST.get("reason", "")
        Report.objects.create(note=note, reported_by=request.user, reason=reason)
        messages.success(request, "Thank you for your report. We will review it shortly.")
        return HttpResponseRedirect(reverse("notes_list"))
    return HttpResponseRedirect(reverse("notes_list"))
