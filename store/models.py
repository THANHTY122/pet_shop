from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _  # Hỗ trợ đa ngôn ngữ
import re
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from decimal import Decimal

# Model Loại Sản Phẩm
class LoaiSanPham(models.Model):
    TRANG_THAI = (
        (1, _('Hiện')),  # Trạng thái hiển thị
        (0, _('Ẩn')),    # Trạng thái ẩn
    )
    MaLoai = models.AutoField(primary_key=True, verbose_name=_('Mã loại'))
    TenLoai = models.CharField(max_length=50, verbose_name=_('Tên loại'))
    slug = models.SlugField(max_length=50, unique=True, blank=True, verbose_name=_('Slug'))
    MoTa = models.TextField(blank=True, verbose_name=_('Mô tả'))
    TrangThai = models.SmallIntegerField(choices=TRANG_THAI, default=1, verbose_name=_('Trạng thái'))
    NgayTao = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày tạo'))
    NgayCapNhat = models.DateTimeField(auto_now=True, verbose_name=_('Ngày cập nhật'))

    def __str__(self):
        return self.TenLoai

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.TenLoai)
        super().save(*args, **kwargs)

# Model Nhà Cung Cấp
class NhaCungCap(models.Model):
    MaNCC = models.AutoField(primary_key=True, verbose_name=_('Mã NCC'))
    TenNCC = models.CharField(max_length=50, verbose_name=_('Tên NCC'))
    DiaChi = models.CharField(max_length=100, verbose_name=_('Địa chỉ'))
    SoDienThoai = models.CharField(max_length=15, verbose_name=_('Số điện thoại'))
    Email = models.EmailField(unique=True, verbose_name=_('Email'))
    TrangThai = models.SmallIntegerField(choices=LoaiSanPham.TRANG_THAI, default=1, verbose_name=_('Trạng thái'))

    def __str__(self):
        return self.TenNCC
    
    def clean(self):
        if not re.match(r'^0\d{9,10}$', self.SoDienThoai):
            raise ValidationError(_('Số điện thoại phải bắt đầu bằng 0 và có 10-11 số.'))

# Model Người Dùng
class NguoiDung(models.Model):
    VAI_TRO = (
        ('1', _('Admin')),
        ('2', _('Nhân viên')),
        ('3', _('Khách hàng')),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('Tài khoản'))
    DiaChi = models.CharField(max_length=100, verbose_name=_('Địa chỉ'))
    SoDienThoai = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name=_('Số điện thoại'))
    NgaySinh = models.DateField(blank=True, null=True, verbose_name=_('Ngày sinh'))
    Avatar = models.ImageField(upload_to='avatar/', blank=True, null=True, verbose_name=_('Ảnh đại diện'))
    VaiTro = models.CharField(max_length=1, choices=VAI_TRO, default='3', verbose_name=_('Vai trò'))
    NgayDangKy = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày đăng ký'))
    TrangThai = models.SmallIntegerField(choices=LoaiSanPham.TRANG_THAI, default=1, verbose_name=_('Trạng thái'))

    def __str__(self):
        return self.user.username
    
    def clean(self):
        if self.SoDienThoai and not re.match(r'^0\d{9,10}$', self.SoDienThoai):
            raise ValidationError(_('Số điện thoại phải bắt đầu bằng 0 và có 10-11 số.'))

# Model Sản Phẩm
class SanPham(models.Model):
    MaSP = models.AutoField(primary_key=True, verbose_name=_('Mã sản phẩm'))
    TenSP = models.CharField(max_length=50, verbose_name=_('Tên sản phẩm'))
    DonGia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Đơn giá'))
    HinhAnh = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name=_('Hình ảnh'))
    MoTa = models.TextField(blank=True, verbose_name=_('Mô tả'))
    NCC = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, verbose_name=_('Nhà cung cấp'))
    SoLuong = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name=_('Số lượng'))
    LoaiSP = models.ForeignKey(LoaiSanPham, on_delete=models.CASCADE, verbose_name=_('Loại sản phẩm'))
    GiamGia = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name=_('Giảm giá (%)'))
    DonViTinh = models.CharField(max_length=20, default='Cái', verbose_name=_('Đơn vị tính'))
    TrangThai = models.SmallIntegerField(choices=LoaiSanPham.TRANG_THAI, default=1, verbose_name=_('Trạng thái'))
    NgayNhapKho = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày nhập kho'))
    HanSuDung = models.DateField(blank=True, null=True, verbose_name=_('Hạn sử dụng'))

    def __str__(self):
        return self.TenSP
    
    def gia_sau_khi_giam(self):
        return self.DonGia * (1 - self.GiamGia * Decimal('0.01'))

# Model Hóa Đơn
class HoaDon(models.Model):
    TRANG_THAI = (
        ('1', _('Chờ xác nhận')),
        ('2', _('Đang giao')),
        ('3', _('Đã giao')),
        ('4', _('Hủy')),
    )
    PHUONG_THUC_THANH_TOAN = (
        ('1', _('Tiền mặt')),
        ('2', _('Chuyển khoản')),
        ('3', _('Ví điện tử')),
    )
    MaHD = models.AutoField(primary_key=True, verbose_name=_('Mã hóa đơn'))
    NguoiDat = models.ForeignKey(NguoiDung, on_delete=models.CASCADE, verbose_name=_('Người đặt'))
    NgayDat = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày đặt'))
    TrangThai = models.CharField(max_length=20, choices=TRANG_THAI, default='1', verbose_name=_('Trạng thái'))
    DiaChiGiao = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Địa chỉ giao'))
    SDTGiao = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('SĐT giao hàng'))
    PhuongThucThanhToan = models.CharField(max_length=1, choices=PHUONG_THUC_THANH_TOAN, default='1', verbose_name=_('Phương thức thanh toán'))
    GhiChu = models.TextField(blank=True, null=True, verbose_name=_('Ghi chú'))

    def __str__(self):
        return f"{_('Hóa đơn')} {self.MaHD} - {self.NguoiDat.user.username}"
    
    @property
    def tong_tien(self):
        return sum(ct.thanhtien for ct in self.chitiethoadon_set.all())

# Model Chi Tiết Hóa Đơn
class ChiTietHoaDon(models.Model):
    MaHD = models.ForeignKey(HoaDon, on_delete=models.CASCADE, verbose_name=_('Hóa đơn'))
    MaSP = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name=_('Sản phẩm'))
    SoLuong = models.IntegerField(verbose_name=_('Số lượng'))
    DonGia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Đơn giá'))

    def __str__(self):
        return f"{self.MaSP.TenSP} - {_('SL')}: {self.SoLuong}"
    
    @property
    def thanhtien(self):
        return self.SoLuong * self.DonGia
    
    def clean(self):
        if self.SoLuong > self.MaSP.SoLuong:
            raise ValidationError(_('Số lượng sản phẩm không đủ'))
    
    def save(self, *args, **kwargs):
        if not self.pk and not self.DonGia:
            self.DonGia = self.MaSP.gia_sau_khi_giam
        super().save(*args, **kwargs)

# Model Lịch Sử Kho
class LichSuKho(models.Model):
    LOAI_THAY_DOI = (
        ('1', _('Nhập')),
        ('2', _('Xuất')),
    )
    SanPham = models.ForeignKey(SanPham, on_delete=models.CASCADE, verbose_name=_('Sản phẩm'))
    NgayThayDoi = models.DateTimeField(auto_now_add=True, verbose_name=_('Ngày thay đổi'))
    SoLuong = models.IntegerField(verbose_name=_('Số lượng'))
    LoaiThayDoi = models.CharField(max_length=1, choices=LOAI_THAY_DOI, verbose_name=_('Loại thay đổi'))
    NguoiThucHien = models.ForeignKey(NguoiDung, on_delete=models.SET_NULL, null=True, verbose_name=_('Người thực hiện'))
    GhiChu = models.TextField(blank=True, null=True, verbose_name=_('Ghi chú'))

    def __str__(self):
        return f"{self.SanPham.TenSP} - {self.LoaiThayDoi} - {self.SoLuong}"

# Signal tự động cập nhật kho
@receiver(post_save, sender=ChiTietHoaDon)
def update_kho(sender, instance, created, **kwargs):
    if created:
        product = instance.MaSP
        product.SoLuong -= instance.SoLuong
        product.save()
        LichSuKho.objects.create(
            SanPham=product,
            SoLuong=instance.SoLuong,
            LoaiThayDoi='2',
            NguoiThucHien=instance.MaHD.NguoiDat,
            GhiChu=f"{_('Xuất')} {instance.SoLuong} {product.DonViTinh} {_('cho hóa đơn')} {instance.MaHD.MaHD}"
        )

# Signal tạo slug
@receiver(pre_save, sender=LoaiSanPham)
def pre_save_loai_san_pham(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.TenLoai)