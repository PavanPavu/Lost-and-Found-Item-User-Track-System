from django.urls import path
from . import views

urlpatterns = [
    # Admin URLs
    path('admin/items/', views.admin_items_list, name='admin_items_list'),
    path('admin/items/create/', views.item_create, name='item_create'),
    path('admin/items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('admin/items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('admin/items/<int:pk>/requests/', views.item_requests_list, name='item_requests_list'),
    path('admin/requests/<int:pk>/<str:action>/', views.request_action, name='request_action'),
    
    # User URLs
    path('items/', views.user_items_list, name='user_items_list'),
    path('items/<int:pk>/request/', views.item_request_create, name='item_request_create'),
    path('my-requests/', views.user_requests_list, name='user_requests_list'),
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)