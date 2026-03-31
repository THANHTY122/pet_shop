# Coffee Shop Django Project

Website bán cà phê xây dựng bằng Django theo mô hình MVT, tách app `products`, `orders`, `users`.

## Công nghệ
- Django (khuyến nghị bản mới nhất trong dải `>=5.1,<6.0`)
- SQLite mặc định (có thể đổi sang PostgreSQL trong `settings.py`)
- Bootstrap 5 + Django Templates

## Cấu trúc thư mục

```text
coffee_shop/
├── manage.py
├── requirements.txt
├── coffee_shop/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── products/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── fixtures/sample_data.json
│   └── templates/products/
├── orders/
│   ├── models.py
│   ├── cart.py
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── context_processors.py
│   └── templates/orders/
├── users/
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/users/
├── templates/
│   ├── base.html
│   ├── includes/
│   └── registration/login.html
└── static/
    ├── css/styles.css
    └── js/main.js
```

## Cài đặt và chạy

```bash
cd coffee_shop
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata products/fixtures/sample_data.json
python manage.py runserver
```

Truy cập:
- Trang chủ: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## Chức năng đã có
- Trang chủ + sản phẩm nổi bật.
- Danh sách sản phẩm có lọc theo danh mục, tìm kiếm.
- Chi tiết sản phẩm.
- Giỏ hàng session-based: thêm / xóa / cập nhật số lượng.
- Checkout mô phỏng thanh toán thành công.
- Đăng ký / đăng nhập / đăng xuất.
- Lịch sử đơn hàng theo người dùng đăng nhập.
- Admin quản lý danh mục, sản phẩm, đơn hàng.

## Nâng cấp Stripe/PayPal (gợi ý)
- Tạo app thanh toán riêng (`payments`).
- Ở `CheckoutView.form_valid`, gọi API Stripe Checkout Session hoặc PayPal Orders API.
- Lưu transaction id + webhook để đối soát trạng thái đơn hàng.

## Lưu ý bảo mật cơ bản
- Đã bật CSRF middleware, session auth, form validation.
- Trước production cần:
  - Đổi `SECRET_KEY` và tắt `DEBUG=False`
  - Cấu hình `ALLOWED_HOSTS`
  - Bật HTTPS, secure cookies.
