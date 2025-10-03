from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest, HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView
from cart.forms import CartAddProductForm

from shop.ai import ai_helper
from shop.forms import OrderCreateForm, ProductCreateForm, SupportForm
from shop.models import Product, Order, Basket

from render_block import render_block_to_string


def questionlist(request):
    session = request.session

    if "chat_history" not in session:
        session["chat_history"] = []
    context = {
        'chat_history': session["chat_history"]
    }
    html = render_block_to_string('shop/home-page.html', 'messages-block', context)
    return HttpResponse(html)
class HomePageView(View):
    def get(self, request: HttpRequest):
        session = request.session
        session["chat_history"] = []
        if "chat_history" not in session:
            session["chat_history"] = []

        form = SupportForm()
        context = {
            'form': form,
            'chat_history': session["chat_history"]
        }
        return render(request, 'shop/home-page.html', context)

    def post(self, request: HttpRequest):
        form = SupportForm(request.POST)
        session = request.session

        if form.is_valid():
            question = form.cleaned_data['question']
            chat_history = session["chat_history"]
            answer = ai_helper(question, chat_history)

            # добавляем в историю
            session["chat_history"].append({"role": "user", "content": question})
            session["chat_history"].append({"role": "assistant", "content": answer})
            session.modified = True

            context = {
                'form': SupportForm(),
            }

            html = render_block_to_string('shop/home-page.html', 'ask-question-block', context)

            response = HttpResponse(html)

            if form.is_valid():
                response['HX-Trigger'] = 'question_valid'
            return response

        return render(request, 'shop/home-page.html', {
            'form': form,
            'chat_history': session.get("chat_history", [])
        })


class ProductsListView(ListView):
    template_name = "shop/products-list.html"
    # model = Product
    context_object_name = "products"
    queryset = Product.objects.filter(archived=False)


class ProductDetailsView(DetailView):
    template_name = "shop/product-details.html"
    model = Product
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context


class ProductCreateView(PermissionRequiredMixin, View):
    permission_required = "shop:superuser"
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": ProductCreateForm()
        }
        return render(request, "shop/product-create.html", context)

    def post(self, request: HttpRequest) -> HttpResponse:
        if self.request.user.is_superuser:
            form = ProductCreateForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                url = reverse('shop:products_list')
                return redirect(url)

            context = {
                'form': form
            }
            return render(request, 'shop/product-create.html', context)

        return redirect(reverse('shop:products_list'))


# class ProductCreateView(PermissionRequiredMixin, CreateView):
#     permission_required = "shop:superuser"
#     template_name = "shop/product-create.html"
#     model = Product
#     fields = "name", "description", "price", "discount", "image"
#     success_url = reverse_lazy("shop:products_list")


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = "shop:superuser"
    template_name = "shop/product-update.html"
    model = Product
    fields = "name", "price", "description", "discount", "image"
    success_url = reverse_lazy("shop:product_details")

    def get_success_url(self):
        return reverse(
            "shop:product_details",
            kwargs={"pk": self.object.pk},
        )


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "shop:superuser"
    template_name = "shop/product-delete.html"
    model = Product
    success_url = reverse_lazy("shop:products_list")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


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
