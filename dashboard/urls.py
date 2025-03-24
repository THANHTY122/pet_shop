# dashboard/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Sản phẩm
    path('add-product/', views.add_product, name='add_product'),
    path('edit-product/<int:MaSP>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:MaSP>/', views.delete_product, name='delete_product'),
    # Nhà cung cấp
    path('add-ncc/', views.add_ncc, name='add_ncc'),
    path('edit-ncc/<int:MaNCC>/', views.edit_ncc, name='edit_ncc'),
    path('delete-ncc/<int:MaNCC>/', views.delete_ncc, name='delete_ncc'),
    # Loại sản phẩm
    path('add-loai/', views.add_loai, name='add_loai'),
    path('edit-loai/<int:MaLoai>/', views.edit_loai, name='edit_loai'),
    path('delete-loai/<int:MaLoai>/', views.delete_loai, name='delete_loai'),
]