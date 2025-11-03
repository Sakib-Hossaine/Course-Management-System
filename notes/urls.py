from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.notes, name="notes"),
    path("notes/add/", views.add_note, name="add_note"),
    path("notes/edit/<int:note_id>/", views.edit_note, name="edit_note"),
    path("notes/delete/<int:note_id>/", views.delete_note, name="delete_note"),
    path("notes/download/<int:note_id>/", views.download_note, name="download_note"),
    path("notes/report/<int:note_id>/", views.report_note, name="report_note"),
]
