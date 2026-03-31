from django.urls import path

from .views import (
    CartAddView,
    CartDetailView,
    CartRemoveView,
    CartUpdateView,
    CheckoutView,
    OrderHistoryView,
)

app_name = 'orders'

urlpatterns = [
    path('', CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', CartAddView.as_view(), name='cart_add'),
    path('update/<int:product_id>/', CartUpdateView.as_view(), name='cart_update'),
    path('remove/<int:product_id>/', CartRemoveView.as_view(), name='cart_remove'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('history/', OrderHistoryView.as_view(), name='order_history'),
]
