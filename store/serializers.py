from rest_framework import serializers
from .models import LoaiSanPham, SanPham, NguoiDung, HoaDon, ChiTietHoaDon

class LoaiSanPhamSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoaiSanPham
        fields = ['MaLoai', 'TenLoai', 'slug', 'MoTa', 'TrangThai', 'NgayTao', 'NgayCapNhat']

class SanPhamSerializer(serializers.ModelSerializer):
    LoaiSP = LoaiSanPhamSerializer(read_only=True)  # Hiển thị thông tin loại sản phẩm
    NCC = serializers.StringRelatedField()  # Hiển thị tên nhà cung cấp
    gia_sau_khi_giam = serializers.ReadOnlyField()  # Thêm giá sau giảm

    class Meta:
        model = SanPham
        fields = ['MaSP', 'TenSP', 'DonGia', 'HinhAnh', 'MoTa', 'NCC', 'SoLuong', 'LoaiSP', 
                  'GiamGia', 'DonViTinh', 'TrangThai', 'NgayNhapKho', 'HanSuDung', 'gia_sau_khi_giam']

class NguoiDungSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Hiển thị username

    class Meta:
        model = NguoiDung
        fields = ['user', 'DiaChi', 'SoDienThoai', 'NgaySinh', 'Avatar', 'VaiTro', 'NgayDangKy', 'TrangThai']

class ChiTietHoaDonSerializer(serializers.ModelSerializer):
    MaSP = SanPhamSerializer(read_only=True)  # Hiển thị thông tin sản phẩm
    thanhtien = serializers.ReadOnlyField()  # Thêm thành tiền

    class Meta:
        model = ChiTietHoaDon
        fields = ['MaHD', 'MaSP', 'SoLuong', 'DonGia', 'thanhtien']

class HoaDonSerializer(serializers.ModelSerializer):
    NguoiDat = NguoiDungSerializer(read_only=True)  # Hiển thị thông tin người đặt
    chitiethoadon_set = ChiTietHoaDonSerializer(many=True, read_only=True)  # Danh sách chi tiết hóa đơn
    tong_tien = serializers.ReadOnlyField()  # Thêm tổng tiền

    class Meta:
        model = HoaDon
        fields = ['MaHD', 'NguoiDat', 'NgayDat', 'TrangThai', 'DiaChiGiao', 'SDTGiao', 
                  'PhuongThucThanhToan', 'GhiChu', 'tong_tien', 'chitiethoadon_set']