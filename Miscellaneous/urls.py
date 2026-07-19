from django.urls import path
from .import views

urlpatterns = [
    path('', views.MisecllaneousApiView.as_view(), name='misecllaneous-list-create'),
    path('culture/', views.CultureListCreateView.as_view(), name='culture-list-create'),
    path('culture/<uuid:id>/', views.CultureDetailView.as_view(), name='culture-detail'),
    path('travel/', views.TravelListCreateView.as_view(), name='travel-list-create'),
    path('travel/<uuid:id>/', views.TravelDetailView.as_view(), name='travel-detail'),
    path('history/', views.HistoryListCreateView.as_view(), name='history-list-create'),
    path('history/<uuid:id>/', views.HistoryDetailView.as_view(), name='history-detail'),
    path('politics/', views.PoliticsListCreateView.as_view(), name='politics-list-create'),
    path('politics/<uuid:id>/', views.PoliticsDetailView.as_view(), name='politics-detail'),
    path('worldview/', views.WorldviewListCreateView.as_view(), name='worldview-list-create'),
    path('worldview/<uuid:id>/', views.WorldviewDetailView.as_view(), name='worldview-detail'),
]
