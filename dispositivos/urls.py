from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='inicio'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/', views.panel, name='panel'),  # <--- Agregado
    path('devices/', views.device_list, name='device_list'),
    path('devices/create/', views.device_create, name='device_create'),
    path('devices/<int:pk>/update/', views.device_update, name='device_update'),
    path('devices/<int:pk>/delete/', views.device_delete, name='device_delete'),
    path('devices/<int:pk>/', views.device_detail, name='device_detail'),
    path('measurements/', views.measurement_list, name='measurement_list'),
    path('measurements/create/', views.measurement_create, name='measurement_create'),
    path('measurements/<int:pk>/update/', views.measurement_update, name='measurement_update'),
    path('measurements/<int:pk>/delete/', views.measurement_delete, name='measurement_delete'),
    path('export/measurements/', views.export_measurements_excel, name='export_measurements'),
    path('export/devices/', views.export_devices_excel, name='export_devices'),
]
