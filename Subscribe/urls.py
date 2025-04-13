from django.urls import path
from .import views

urlpatterns = [
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('subscribe/verify/<str:token>/', views.VerifySubscriptionView.as_view(), name='verify-subscription'),
    path('subscribers/', views.SubscriberListView.as_view(), name='subscriber-list')
]
