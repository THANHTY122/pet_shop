from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import LoaiSanPham, SanPham, NguoiDung, HoaDon, ChiTietHoaDon
from .serializers import (LoaiSanPhamSerializer, SanPhamSerializer, NguoiDungSerializer, 
                         HoaDonSerializer, ChiTietHoaDonSerializer)
import re
from django.core.paginator import Paginator


# View thông thường
def home(request):
    """Trang chính của Pet Shop (kết hợp index và home)"""
    products = SanPham.objects.filter(TrangThai=1)
    return render(request, 'pages/home.html', {
        'message': 'Chào mừng đến với Pet Shop!',
        'products': products
    })

def Sign_In(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('home')
            else:
                messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng.')
        else:
            messages.error(request, 'Dữ liệu không hợp lệ. Vui lòng kiểm tra lại.')
    else:
        form = AuthenticationForm()
    return render(request, 'pages/signin.html', {'form': form})


def SignUp(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            so_dien_thoai = request.POST.get('SoDienThoai', '')
            if so_dien_thoai and not re.match(r'^0\d{9,10}$', so_dien_thoai):
                messages.error(request, 'Số điện thoại phải bắt đầu bằng 0 và có 10-11 số.')
                return render(request, 'pages/signup.html', {'form': form})
            
            user = form.save()
            nguoi_dung = NguoiDung.objects.create(
                user=user,
                DiaChi=request.POST.get('DiaChi', ''),
                SoDienThoai=so_dien_thoai,
                NgaySinh=request.POST.get('NgaySinh', None) or None,
                Avatar=request.FILES.get('Avatar', None),
                VaiTro='3'  # Khách hàng
            )
            login(request, user)
            messages.success(request, 'Đăng ký thành công! Chào mừng bạn đến với Pet Shop.')
            return redirect('home')
        else:
            messages.error(request, 'Đăng ký thất bại. Vui lòng kiểm tra lại thông tin.')
    else:
        form = UserCreationForm()
    return render(request, 'pages/signup.html', {'form': form})

def product(request):
    """Danh sách sản phẩm với phân trang, lọc theo loại và tìm kiếm"""
    # Lấy tất cả loại sản phẩm để hiển thị trong bộ lọc
    loaisanpham = LoaiSanPham.objects.filter(TrangThai=1)

    # Truy vấn sản phẩm với tối ưu hóa
    sanpham_list = SanPham.objects.filter(TrangThai=1).select_related('LoaiSP', 'NCC')

    # Lọc theo loại sản phẩm (nếu có)
    loai_filter = request.GET.get('loai')
    if loai_filter:
        sanpham_list = sanpham_list.filter(LoaiSP__MaLoai=loai_filter)

    # Tìm kiếm sản phẩm (nếu có)
    query = request.GET.get('q')
    if query:
        sanpham_list = sanpham_list.filter(TenSP__icontains=query)

    # Phân trang (9 sản phẩm mỗi trang)
    paginator = Paginator(sanpham_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Truyền dữ liệu vào context
    context = {
        'sanpham_list': page_obj,  # Danh sách sản phẩm đã phân trang
        'loaisanpham': loaisanpham,  # Danh sách loại sản phẩm cho bộ lọc
        'page_obj': page_obj,  # Đối tượng phân trang
        'is_paginated': page_obj.has_other_pages(),  # Kiểm tra có phân trang hay không
        'query': query,  # Giữ giá trị tìm kiếm (nếu có)
    }
    return render(request, 'pages/product.html', context)

def DSSPTheoLoai(request, ml):
    loai = get_object_or_404(LoaiSanPham, MaLoai=ml)
    loaisanpham = LoaiSanPham.objects.filter(TrangThai=1)
    sanpham_list = SanPham.objects.filter(LoaiSP=loai, TrangThai=1).select_related('LoaiSP', 'NCC')
    paginator = Paginator(sanpham_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'sanpham_list': page_obj,
        'loaisanpham': loaisanpham,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'loai': loai,
    }
    return render(request, 'pages/product.html', context)

def product_detail(request, ml):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(SanPham, MaSP=ml)
    return render(request, 'pages/product_detail.html', {'product': product})

def search_products(request):
    """Tìm kiếm sản phẩm"""
    query = request.GET.get('q', '')
    products = SanPham.objects.filter(TenSP__icontains=query, TrangThai=1)
    return render(request, 'pages/product.html', {'products': products, 'query': query})

@login_required
def cart(request):
    """Giỏ hàng (dùng session)"""
    cart = request.session.get('cart', {})
    products = SanPham.objects.filter(MaSP__in=cart.keys())
    cart_items = [{'product': p, 'quantity': cart[str(p.MaSP)]} for p in products]
    return render(request, 'pages/cart.html', {'cart_items': cart_items})

@login_required
def AddToCart(request, MaSP):
    product = get_object_or_404(SanPham, MaSP=MaSP)
    if product.SoLuong <= 0:
        messages.error(request, 'Sản phẩm này đã hết hàng!')
        return redirect('product')
    cart = request.session.get('cart', {})
    current_quantity = cart.get(str(MaSP), 0)
    if current_quantity + 1 > product.SoLuong:
        messages.error(request, 'Số lượng trong kho không đủ!')
        return redirect('product')
    cart[str(MaSP)] = current_quantity + 1
    request.session['cart'] = cart
    messages.success(request, 'Đã thêm vào giỏ hàng!')
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    """Xóa khỏi giỏ hàng"""
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

@login_required
def AddToInvoice(request):
    """Tạo hóa đơn từ giỏ hàng"""
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('cart')
    hoa_don = HoaDon.objects.create(NguoiDat=request.user.nguoidung)
    for MaSP, quantity in cart.items():
        product = SanPham.objects.get(MaSP=MaSP)
        ChiTietHoaDon.objects.create(MaHD=hoa_don, MaSP=product, SoLuong=quantity, DonGia=product.gia_sau_khi_giam)
    request.session['cart'] = {}  # Xóa giỏ hàng sau khi tạo hóa đơn
    return redirect('hoa_don')

@login_required
def DeleteAllCart(request):
    """Xóa toàn bộ giỏ hàng"""
    request.session['cart'] = {}
    return redirect('cart')

@login_required
def hoa_don(request):
    """Danh sách hóa đơn"""
    invoices = HoaDon.objects.filter(NguoiDat__user=request.user)
    return render(request, 'pages/hoa_don.html', {'invoices': invoices})

@login_required
def detail_invoice(request, MaHD):
    """Chi tiết hóa đơn"""
    invoice = get_object_or_404(HoaDon, MaHD=MaHD, NguoiDat__user=request.user)
    return render(request, 'pages/detail_invoice.html', {'invoice': invoice})

# API ViewSets
class LoaiSanPhamViewSet(viewsets.ModelViewSet):
    queryset = LoaiSanPham.objects.all()
    serializer_class = LoaiSanPhamSerializer
    permission_classes = [AllowAny]

class SanPhamViewSet(viewsets.ModelViewSet):
    queryset = SanPham.objects.filter(TrangThai=1)
    serializer_class = SanPhamSerializer
    permission_classes = [AllowAny]

class KhachHangViewSet(viewsets.ModelViewSet):
    queryset = NguoiDung.objects.filter(VaiTro='3')
    serializer_class = NguoiDungSerializer
    permission_classes = [IsAuthenticated]

class HoaDonViewSet(viewsets.ModelViewSet):
    queryset = HoaDon.objects.all()
    serializer_class = HoaDonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return HoaDon.objects.filter(NguoiDat__user=self.request.user)

class CTHoaDonViewSet(viewsets.ModelViewSet):
    queryset = ChiTietHoaDon.objects.all()
    serializer_class = ChiTietHoaDonSerializer
    permission_classes = [IsAuthenticated]

class ListLoaiSanPham(generics.ListAPIView):
    queryset = LoaiSanPham.objects.all()
    serializer_class = LoaiSanPhamSerializer
    permission_classes = [AllowAny]

class ListSanPham(generics.ListAPIView):
    queryset = SanPham.objects.filter(TrangThai=1)
    serializer_class = SanPhamSerializer
    permission_classes = [AllowAny]