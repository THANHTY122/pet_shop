from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from . import views

# Khai báo API router
router = DefaultRouter()
router.register(r'loaisanpham', views.LoaiSanPhamViewSet, basename='loaisanpham')
router.register(r'sanpham', views.SanPhamViewSet, basename='sanpham')
router.register(r'khachhang', views.KhachHangViewSet, basename='khachhang')
router.register(r'hoadon', views.HoaDonViewSet, basename='hoadon')
router.register(r'cthoadon', views.CTHoaDonViewSet, basename='cthoadon')

urlpatterns = [
    # Trang chính
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),  # Giữ nguyên để tương thích

    # Xác thực người dùng
    path('signin/', views.Sign_In, name='signin'),
    path('signup/', views.SignUp, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Sửa 'index' thành 'home'

    # API Routes
    path('api/', include(router.urls)),  # Bao gồm tất cả API từ ViewSet
    path('api/loaisanpham/', views.ListLoaiSanPham.as_view(), name='loaisanpham-list'),
    path('api/sanpham/', views.ListSanPham.as_view(), name='list_sanpham'),

    # Quản lý sản phẩm
    path('products/', views.product, name='product'),
    path('products/category/<int:ml>/', views.DSSPTheoLoai, name='DSSPTheoLoai'),
    path('products/<int:ml>/', views.product_detail, name='product_detail'),
    # path('products/search/', views.search_products, name='search_products'),

    # Giỏ hàng
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:MaSP>/', views.AddToCart, name='add_to_cart'),  
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/invoice/', views.AddToInvoice, name='AddToInvoice'),
    path('cart/clear/', views.DeleteAllCart, name='DeleteAllCart'),

    # Hóa đơn
    path('invoices/', views.hoa_don, name='hoa_don'),
    path('invoices/<int:MaHD>/', views.detail_invoice, name='detail-invoice'),
]