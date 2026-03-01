from django.urls import path

from . import views

app_name = 'scheduler'

urlpatterns = [
    path('', views.schedule_home, name='home'),
    path('schedule/add/', views.schedule_add, name='schedule_add'),
    path('schedule/edit/<int:pk>/', views.schedule_edit, name='schedule_edit'),

    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/add/', views.teacher_add, name='teacher_add'),

    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.subject_add, name='subject_add'),

    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_add, name='group_add'),
]
