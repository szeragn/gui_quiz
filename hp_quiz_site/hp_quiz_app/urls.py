from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("question/add/", views.add_question, name="add_question"),
    path("question/add/addrecord", views.add_question_record),
    path("question/update/<int:id>", views.update_question),
    path("question/update/updaterecord/<int:id>", views.update_question_record),
    path("question/delete/<int:id>", views.delete_question),
    path("options/add/", views.add_options, name="add_options"),
    path("options/add/addrecord", views.add_options_record, name="add_options_record"),
    path("options/update/<int:id>", views.update_options, name="update_options"),
    path(
        "options/update/updaterecord/<int:id>",
        views.update_options_record,
        name="update_options_record",
    ),
    path("options/delete/<int:id>", views.delete_options, name="delete_options"),
]
