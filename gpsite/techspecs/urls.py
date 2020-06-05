from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:id>/', views.detail, name='detail'),
    path('allequipments/', views.all_equipment, name='all_equipments'),
    path('addequipments/', views.add_equipment, name='add_equipments'),
    path('addgeneralspecs/', views.add_general_specs, name='add_general_specs'),
    path('addtechnicalspecs/', views.add_tech_specs, name='add_tech_specs'),
    path('addreport/', views.add_report, name='add_report'),
    path('test/', views.test, name='test'),

]
