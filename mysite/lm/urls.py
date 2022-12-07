from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.SearchResultsView.as_view(), name='search'),
    path('', views.index, name='index'),
    path('working_zones/', views.working_zones, name='working_zones'),
    path('working_machines_list/', views.working_machines_list, name='working_machines_list'),
    path('workers/', views.workers, name='workers'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('work_records/', views.work_records, name='work_records'),
    path('profile/', views.profilis, name='profile'),
    path('my_notes/', views.NotesListView.as_view(), name='my_notes'),
    path('my_working_records/', views.WorkersWorkingRecordsListView.as_view(), name='my_working_records'),
    path('my_used_machines/', views.WorkersUsedMachinesListView.as_view(), name='my_used_machines'),
    # path('my_machines/<int:pk>', views.KrautuvasByUserDetailView.as_view(), name='my_machine'),
    path('my_machine/new', views.KrautuvasByUserCreateView.as_view(), name='my_new_machine'),
    # path('my_used_machines/<int:pk>/update', views.KrautuvasByUserUpdateView.as_view(), name='my_machine_update'),
    # path('my_used_machines/<int:pk>/delete', views.KrautuvasByUserDeleteView.as_view(), name='my_machine_delete'),
    # path('my_notes/new', views.NotesByUserCreateView.as_view(), name='my_new_note'),
    # path('my_working_records/new', views.WorkingRecordByUserCreateView.as_view(), name='add_my_working_records'),

]
