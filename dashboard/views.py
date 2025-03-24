# dashboard/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import SanPham, LoaiSanPham, NhaCungCap
from django.core.paginator import Paginator
from django import forms

# Form cho Sản phẩm
class SanPhamForm(forms.ModelForm):
    class Meta:
        model = SanPham
        fields = ['TenSP', 'DonGia', 'HinhAnh', 'MoTa', 'NCC', 'SoLuong', 'LoaiSP', 'GiamGia', 'DonViTinh', 'TrangThai', 'HanSuDung']
        widgets = {
            'MoTa': forms.Textarea(attrs={'rows': 3}),
            'HanSuDung': forms.DateInput(attrs={'type': 'date'}),
        }

# Form cho Nhà cung cấp
class NhaCungCapForm(forms.ModelForm):
    class Meta:
        model = NhaCungCap
        fields = ['TenNCC', 'DiaChi', 'SoDienThoai', 'Email', 'TrangThai']

# Form cho Loại sản phẩm
class LoaiSanPhamForm(forms.ModelForm):
    class Meta:
        model = LoaiSanPham
        fields = ['TenLoai', 'MoTa', 'TrangThai']

# Decorator kiểm tra admin
def admin_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'nguoidung') or request.user.nguoidung.VaiTro != '1':
            messages.error(request, 'Bạn không có quyền truy cập vào dashboard!')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

# Dashboard chính
@admin_required
def dashboard(request):
    sanpham_list = SanPham.objects.all().select_related('LoaiSP', 'NCC')
    ncc_list = NhaCungCap.objects.all()
    loai_list = LoaiSanPham.objects.all()
    
    paginator_sp = Paginator(sanpham_list, 10)
    paginator_ncc = Paginator(ncc_list, 10)
    paginator_loai = Paginator(loai_list, 10)
    
    page_number_sp = request.GET.get('page_sp')
    page_number_ncc = request.GET.get('page_ncc')
    page_number_loai = request.GET.get('page_loai')
    
    page_obj_sp = paginator_sp.get_page(page_number_sp)
    page_obj_ncc = paginator_ncc.get_page(page_number_ncc)
    page_obj_loai = paginator_loai.get_page(page_number_loai)
    
    context = {
        'sanpham_list': page_obj_sp,
        'ncc_list': page_obj_ncc,
        'loai_list': page_obj_loai,
        'page_obj_sp': page_obj_sp,
        'page_obj_ncc': page_obj_ncc,
        'page_obj_loai': page_obj_loai,
        'is_paginated_sp': page_obj_sp.has_other_pages(),
        'is_paginated_ncc': page_obj_ncc.has_other_pages(),
        'is_paginated_loai': page_obj_loai.has_other_pages(),
    }
    return render(request, 'pages/dashboard.html', context)

# Quản lý Nhà cung cấp
@admin_required
def add_ncc(request):
    if request.method == 'POST':
        form = NhaCungCapForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm nhà cung cấp thành công!')
            return redirect('dashboard')
    else:
        form = NhaCungCapForm()
    return render(request, 'pages/add_ncc.html', {'form': form})

@admin_required
def edit_ncc(request, MaNCC):
    ncc = get_object_or_404(NhaCungCap, MaNCC=MaNCC)
    if request.method == 'POST':
        form = NhaCungCapForm(request.POST, instance=ncc)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật nhà cung cấp thành công!')
            return redirect('dashboard')
    else:
        form = NhaCungCapForm(instance=ncc)
    return render(request, 'pages/edit_ncc.html', {'form': form, 'ncc': ncc})

@admin_required
def delete_ncc(request, MaNCC):
    ncc = get_object_or_404(NhaCungCap, MaNCC=MaNCC)
    if request.method == 'POST':
        ncc.delete()
        messages.success(request, 'Xóa nhà cung cấp thành công!')
        return redirect('dashboard')
    return render(request, 'pages/delete_ncc.html', {'ncc': ncc})

# Quản lý Loại sản phẩm
@admin_required
def add_loai(request):
    if request.method == 'POST':
        form = LoaiSanPhamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm loại sản phẩm thành công!')
            return redirect('dashboard')
    else:
        form = LoaiSanPhamForm()
    return render(request, 'pages/add_loai.html', {'form': form})

@admin_required
def edit_loai(request, MaLoai):
    loai = get_object_or_404(LoaiSanPham, MaLoai=MaLoai)
    if request.method == 'POST':
        form = LoaiSanPhamForm(request.POST, instance=loai)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật loại sản phẩm thành công!')
            return redirect('dashboard')
    else:
        form = LoaiSanPhamForm(instance=loai)
    return render(request, 'pages/edit_loai.html', {'form': form, 'loai': loai})

@admin_required
def delete_loai(request, MaLoai):
    loai = get_object_or_404(LoaiSanPham, MaLoai=MaLoai)
    if request.method == 'POST':
        loai.delete()
        messages.success(request, 'Xóa loại sản phẩm thành công!')
        return redirect('dashboard')
    return render(request, 'pages/delete_loai.html', {'loai': loai})

# Các view cũ cho Sản phẩm (giữ nguyên)
@admin_required
def add_product(request):
    if request.method == 'POST':
        form = SanPhamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thêm sản phẩm thành công!')
            return redirect('dashboard')
    else:
        form = SanPhamForm()
    return render(request, 'pages/add_product.html', {'form': form})

@admin_required
def edit_product(request, MaSP):
    product = get_object_or_404(SanPham, MaSP=MaSP)
    if request.method == 'POST':
        form = SanPhamForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cập nhật sản phẩm thành công!')
            return redirect('dashboard')
    else:
        form = SanPhamForm(instance=product)
    return render(request, 'pages/edit_product.html', {'form': form, 'product': product})

@admin_required
def delete_product(request, MaSP):
    product = get_object_or_404(SanPham, MaSP=MaSP)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Xóa sản phẩm thành công!')
        return redirect('dashboard')
    return render(request, 'pages/delete_product.html', {'product': product})