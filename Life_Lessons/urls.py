from django.urls import path

from . import views


urlpatterns = [
    path(
        "",
        views.LifeLessonsListCreateView.as_view(),
        name="life-lessons-list-create",
    ),
    path(
        "<uuid:id>/",
        views.LifeLessonsRetrieveUpdateDestroyView.as_view(),
        name="life-lessons-retrieve-update-destroy",
    ),
]

