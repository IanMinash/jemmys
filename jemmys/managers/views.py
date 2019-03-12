from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect, get_object_or_404
from django.conf import settings
from jemmys.main.models import Product, ProductPhoto, ProductCategory, Order, BuyerAddress, UserIssue
from django_ajax.decorators import ajax
from .forms import LoginForm, NewProductForm, NewVariantForm

# Create your views here.


class Login(LoginView):
    template_name = "managers/login.html"
    authentication_form = LoginForm

    def get(self, *args, **kwargs):
        # Redirect if user is already logged in.
        if self.request.user.is_authenticated:
            return redirect("managers:dashboard")
        else:
            return super().get(self.request, args, kwargs)


class Logout(LogoutView):
    template_name = "managers/logout.html"


@login_required
def dash(request):
    return render(request, "managers/dashboard.html", context={})


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = "managers/products.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        queryset = queryset.filter(variant_of=None)
        return queryset


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "managers/product.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        context['variant_of_products'] = Product.objects.filter(
            variant_of=None)
        return context


@login_required
def update_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = NewProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            if product.variant_of:
                return redirect("managers:product", product.variant_of.slug)
            else:
                return redirect("managers:product", product.slug)
        return render(request, 'managers/update_product.html', {'form': form})


@login_required
def new_product(request):
    context = {}
    if request.method == 'POST':
        form = NewProductForm(data=request.POST)
        if form.is_valid():
            product = form.save()
            images = request.FILES.getlist('images')
            for image in images:
                ProductPhoto.objects.create(photo=image, product=product)
            return redirect("managers:products")
        else:
            context['form'] = form
    else:
        context['form'] = NewProductForm
        context['categories'] = ProductCategory.objects.all()
    return render(request, "managers/new_product.html", context=context)


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "managers/orders.html"
    context_object_name = "orders"


@login_required
def view_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    items = order.items.all()
    item_total = 0
    for item in items:
        item_total += item.cost
    context={'order': order, 'items': items, 'item_total': item_total}
    if request.method == "POST":
        order.status = request.POST.get("order_status")
        order.save(update_fields=["status"])
        context['success'] = True
    return render(request, "managers/order.html", context=context)


@login_required
def variant_manager(request):
    if request.method == "POST":
        action = request.POST.get("action", None)
        if action == "add":
            form = NewVariantForm(request.POST)
            if form.is_valid():
                variant = form.save()
                images = request.FILES.getlist('images')
                for image in images:
                    ProductPhoto.objects.create(photo=image, product=variant)
                return redirect("managers:product", Product.objects.get(id=request.POST.get("variant_of")).slug)
    else:
        pass


class CustomerListView(LoginRequiredMixin, ListView):
    model = BuyerAddress
    template_name = "managers/customers.html"
    context_object_name = "customers"


class CustomerDetailView(LoginRequiredMixin, DetailView):
    model = BuyerAddress
    template_name = "managers/customer.html"
    context_object_name = "customer"

    
    def get_context_data(self, **kwargs):
        context = super(CustomerDetailView, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(buyer=self.get_object())
        context['api_key'] = settings.GCLOUD_API_KEY
        return context
    

class IssueListView(LoginRequiredMixin, ListView):
    model = UserIssue
    template_name = "managers/issues.html"
    context_object_name = "issues"



class IssueDetailView(LoginRequiredMixin, DetailView):
    model = UserIssue
    template_name = "managers/issue.html"
    context_object_name = "issue"


@login_required
@ajax
def issue_manager(request, pk):
    if request.method == 'POST':
        issue = UserIssue.objects.get(pk=pk)
        issue.status = request.POST.get("status")
        issue.save(update_fields=["status"])
        return {'text':"SUCCESS"}