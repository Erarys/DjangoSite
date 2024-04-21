from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView
)
from cart.forms import CartAddProductForm
from shop.forms import OrderCreateForm, ProductCreateForm
from shop.models import Product, Order, Basket


# View для отображения домашней страницы
class HomePageView(View):
    def get(self, request: HttpRequest):
        return render(request, 'shop/home-page.html')


# View для отображения списка продуктов
class ProductsListView(ListView):
    template_name = "shop/products-list.html"
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False, category="goods")

    def get_queryset(self):
        query = self.request.GET.get('category')
        if query:
            memo_list = Product.objects.filter(archived=False, category=query)
        else:
            memo_list = Product.objects.filter(archived=False)

        # ordering = self.get_ordering()
        # memo_list = memo_list.order_by(ordering)
        # The following checks are not needed since your get_ordering() will always only return ONE string
        # if ordering and isinstance(ordering, str):
        # ordering = (ordering,)
        # memo_list = memo_list.order_by(*ordering)
        return memo_list


# View для отображения деталей продукта
class ProductDetailsView(DetailView):
    template_name = "shop/product-details.html"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        # Добавляем форму для добавления продукта в корзину в контекст
        cart_product_form = CartAddProductForm()
        kwargs['cart_product_form'] = cart_product_form
        return super(ProductDetailsView, self).get_context_data(**kwargs)


# View для создания нового продукта
class ProductCreateView(PermissionRequiredMixin, View):
    permission_required = "shop:superuser"

    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": ProductCreateForm()
        }
        return render(request, "shop/product-create.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        form = ProductCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # После успешного создания продукта, перенаправляем на список продуктов
            url = reverse('shop:products_list')
            return redirect(url)

        context = {
            'form': form
        }
        return render(request, 'shop/product-create.html', context)


# View для обновления продукта
class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "shop:superuser"
    template_name = "shop/product-update.html"
    model = Product
    fields = ["name", "category", "price", "description", "discount"]
    success_url = reverse_lazy("shop:products_list")

    def get_success_url(self):
        # После успешного обновления продукта, перенаправляем на страницу деталей обновленного продукта
        return reverse("shop:product_details", kwargs={"pk": self.object.pk})


# View для удаления продукта
class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shop:superuser"
    template_name = "shop/product-delete.html"
    model = Product
    success_url = reverse_lazy("shop:products_list")

    def form_valid(self, form):
        # Помечаем продукт как "архивный" при удалении (вместо реального удаления из базы данных)
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# View для создания заказа
class CreateOrderView(View):
    def get(self, request: HttpRequest):
        user = request.user
        form = OrderCreateForm(user=user)
        return render(request, 'shop/order-create.html', {'form': form})

    def post(self, request):
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Order created successfully!")
        return render(request, 'shop/order-create.html', {'form': form})
