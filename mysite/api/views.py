from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Product


class ProductApiView(APIView):
    def get(self, request):
        allProducts = Product.objects.all().values()
        return Response({"message": "List of Product", "Product List": allProducts})

    def post(self, request):
        product, created = Product.objects.get_or_create(
            name=request.data["name"],
            category=request.data.get("category", "coffee_category"),
            image=request.data.get("image", "coffee_image.img"),
            description=request.data.get("description", "coffee_description"),
            price=request.data.get("price", 0),
            discount=request.data.get("discount", 0),
            archived=request.data.get("archived", False)
        )

        return Response({
            "message": f"Product Create {created}",
            "Product ": f"{product}",
        })

    def delete(self, request):
        obj = Product.objects.get(id=request.data["id"])
        obj.delete()

        return Response({
            "message": f"Product Delete",
            "Product ": f"{obj}",
        })

    def put(self, request):
        product, created = Product.objects.update_or_create(
            id=request.data["id"],
            defaults=request.data
        )

        return Response({
            "message": f"Product Update {created}",
            "Product ": f"{product}",
        })
