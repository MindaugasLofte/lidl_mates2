from django.urls import path

from . import views
from .views import SearchResultsView

urlpatterns = [
    path('search/', SearchResultsView.as_view(), name='search'),
    path('', views.index, name='index'),
    path('working_zones/', views.working_zones, name='working_zones'),
    path('working_machines_list/', views.working_machines_list, name='working_machines_list'),
    path('workers/', views.workers, name='workers'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('work_records/', views.work_records, name='work_records'),



    
]
