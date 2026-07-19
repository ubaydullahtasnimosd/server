from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuranLifeLessonsListCreateView.as_view(), name='quran-life-lessons-list-create'),
    path('<uuid:id>/', views.QuranLifeLessonsRetrieveUpdateDestroyView.as_view(), name='quran-life-lessons-retrieve-update-destroy')
]
