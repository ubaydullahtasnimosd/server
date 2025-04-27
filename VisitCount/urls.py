from django.urls import path
from .views import VisitorCountAPIView

urlpatterns = [
    path('', VisitorCountAPIView.as_view(), name='visitor-count'),
]