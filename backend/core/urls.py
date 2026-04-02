from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('vendors/', views.vendor_list, name='vendor_list'),
    path('vendors/create/', views.vendor_create, name='vendor_create'),
    path('vendors/<int:pk>/edit/', views.vendor_edit, name='vendor_edit'),
    path('vendors/<int:pk>/delete/', views.vendor_delete, name='vendor_delete'),
    path('purchaseorders/', views.purchaseorder_list, name='purchaseorder_list'),
    path('purchaseorders/create/', views.purchaseorder_create, name='purchaseorder_create'),
    path('purchaseorders/<int:pk>/edit/', views.purchaseorder_edit, name='purchaseorder_edit'),
    path('purchaseorders/<int:pk>/delete/', views.purchaseorder_delete, name='purchaseorder_delete'),
    path('requisitions/', views.requisition_list, name='requisition_list'),
    path('requisitions/create/', views.requisition_create, name='requisition_create'),
    path('requisitions/<int:pk>/edit/', views.requisition_edit, name='requisition_edit'),
    path('requisitions/<int:pk>/delete/', views.requisition_delete, name='requisition_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
