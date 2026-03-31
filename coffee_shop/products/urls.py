from django.urls import path

from .views import HomeView, ProductDetailView, ProductListView

app_name = 'products'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/category/<slug:category_slug>/', ProductListView.as_view(), name='product_by_category'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
]
