from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.HadithLifeLessonsListCreateView.as_view(),
        name="hadith-life-lessons-list-create",
    ),
    path(
        "<uuid:id>/",
        views.HadithLifeLessonsRetrieveUpdateDestroyView.as_view(),
        name="hadith-life-lessons-retrieve-update-destroy",
    ),
]

