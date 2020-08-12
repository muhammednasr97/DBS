from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('search/<str:id>/', views.search_detail, name='detail'),
    path('allequipments/', views.all_equipments, name='all_equipments'),
    path('allequipments/<str:id>/', views.admin_detail, name='details'),
    path('addequipments/', views.add_equipment, name='add_equipments'),
    path('searchequipment/', views.search_allequipment, name='search_equipment'),
    path('search/', views.search_page, name='search'),
    path('about/', views.about, name='about'),
    path('delete/<str:id>/', views.delete, name='delete'),
    path('update/<str:id>/', views.data_to_update, name='data_to_update'),
    path('edit/<str:id>/<int:version>', views.edit, name='edit'),
    path('archive/<str:id>/', views.archive, name='archive'),
    path('compare/<str:id>/', views.archive_view, name='compare'),
    path('pdf/<str:id>/', views.gen_pdf, name='pdf'),
    path('test/', views.test, name='test'),
    path('radiology/', views.radiology, name='specialty')
]
