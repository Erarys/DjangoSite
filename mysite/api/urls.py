from django.urls import path

from api.views import ProductApiView

app_name = "api"

urlpatterns = [
    path('request/', ProductApiView.as_view(), name="product_request"),
]