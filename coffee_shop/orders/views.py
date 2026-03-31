from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import FormView, ListView, TemplateView

from products.models import Product

from .cart import Cart
from .forms import AddToCartForm, CheckoutForm
from .models import Order, OrderItem


class CartDetailView(TemplateView):
    template_name = 'orders/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = Cart(self.request)
        return context


class CartAddView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id, is_available=True)
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart.add(product=product, quantity=form.cleaned_data['quantity'])
            messages.success(request, 'Đã thêm sản phẩm vào giỏ hàng.')
        return redirect('orders:cart_detail')


class CartUpdateView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        quantity = max(1, quantity)
        cart.add(product=product, quantity=quantity, override_quantity=True)
        messages.success(request, 'Đã cập nhật số lượng.')
        return redirect('orders:cart_detail')


class CartRemoveView(View):
    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        cart.remove(product)
        messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
        return redirect('orders:cart_detail')


class CheckoutView(LoginRequiredMixin, FormView):
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm

    def dispatch(self, request, *args, **kwargs):
        self.cart = Cart(request)
        if len(self.cart) == 0:
            messages.warning(request, 'Giỏ hàng đang trống.')
            return redirect('products:product_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        order = Order.objects.create(
            user=self.request.user,
            full_name=form.cleaned_data['full_name'],
            email=form.cleaned_data['email'],
            phone=form.cleaned_data['phone'],
            address=form.cleaned_data['address'],
            note=form.cleaned_data['note'],
        )

        for item in self.cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['price'],
            )

        order.total_price = order.calculate_total()
        order.status = 'paid'  # Mô phỏng thanh toán thành công
        order.save(update_fields=['total_price', 'status'])
        self.cart.clear()
        messages.success(self.request, f'Đặt hàng thành công! Mã đơn hàng: #{order.pk}')
        return redirect('orders:order_history')


class OrderHistoryView(LoginRequiredMixin, ListView):
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')
