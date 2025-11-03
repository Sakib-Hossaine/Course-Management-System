from django.urls import path
from . import views_class

urlpatterns = [
    path("class/", views_class.class_list, name="class_list"),
    path("class/add/", views_class.add_class, name="add_class"),
    path("class/edit/<int:class_id>/", views_class.edit_class, name="edit_class"),
    path("class/delete/<int:class_id>/", views_class.delete_class, name="delete_class"),
    path("class/join/<int:class_id>/", views_class.join_class, name="join_class"),
]
