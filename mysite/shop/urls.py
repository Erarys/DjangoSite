from django.urls import path

from shop.views import (
    HomePageView,
    ProductsListView,
    ProductDetailsView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    CreateOrderView,
    questionlist,
)

app_name = "shop"

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("products/", ProductsListView.as_view(), name="products_list"),
    path("products/create/", ProductCreateView.as_view(), name="product_create"),
    path("products/<int:pk>", ProductDetailsView.as_view(), name="product_details"),
    path("products/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("products/<int:pk>/delete", ProductDeleteView.as_view(), name="product_delete"),
    path("order/", CreateOrderView.as_view(), name="order_create"),
    path('question-list/', questionlist, name='question-list'),
]
