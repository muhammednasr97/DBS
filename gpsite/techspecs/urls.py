from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/<str:id>/', views.detail, name='detail'),
    path('allequipments/', views.all_equipments, name='all_equipments'),
    path('addequipments/', views.add_equipment, name='add_equipments'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('about/', views.about, name='about'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('update/<str:id>/', views.data_to_update, name='data_to_update'),
    path('edit/<str:id>/', views.edit, name='edit'),

]
