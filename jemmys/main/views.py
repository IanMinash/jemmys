from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from .models import Product, ProductPhoto, ProductCategory, Order, OrderItem
from .forms import AddressForm, UserIssueForm
from django_ajax.decorators import ajax

# Create your views here.

def home(request):
    context = dict()
    context['products'] = list()
    if request.GET.get('category'):
        all_products = Product.objects.filter(category__category=request.GET['category'], variant_of=None)
    elif request.GET.get('name'):
        all_products = Product.objects.filter(name=request.GET['name'])
    else:
        all_products = Product.objects.filter(variant_of=None)
    for prod in all_products:
        photos = ProductPhoto.objects.filter(product=prod)[:2]
        product = {'details':prod, 'photos':list()}
        product['photos'] = [*photos]
        context['products'].append(product)
    return render(request, "main/home.html", context=context)


class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product.html"
    context_object_name = "product"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.variant_of:
            return redirect('view-product', slug=self.object.variant_of.slug)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        context['photos'] = ProductPhoto.objects.filter(product=product)
        # Other products of the same category
        others = Product.objects.exclude(id__exact=context['product'].id).filter(category__exact=context['product'].category, variant_of=None)
        context['others'] = list()
        context['variants'] = Product.objects.filter(variant_of=product)
        context['quantity'] = range(1,product.quantity+1)
        for other in others:
            photos = ProductPhoto.objects.filter(product=other)[:2]
            product = {'details':other, 'photos':list()}
            product['photos'] = [*photos]
            context['others'].append(product)
        return context


@ajax
def variants(request):
    if request.method == 'POST':
        p_id = request.POST.get('id')
        product = Product.objects.get(id=p_id)
        photo_urls = list()
        photos = ProductPhoto.objects.filter(product=product)
        for photo in photos:
            photo_urls.append(str(photo.photo.url))
        return {'quantity': product.quantity, 'photos':photo_urls}

def order_search(request):
    context = dict()
    if request.method == 'POST':
        order_id = request.POST.get('ordersearch', None)
        order_id = order_id.upper()
        if order_id:
            try:
                order = Order.objects.get(order_id=order_id)
                return redirect('view-order', order_id=order.order_id)
            except ObjectDoesNotExist:
                context['not_found'] = True
    return render(request, "main/order-search.html", context=context)


def contact(request):
    success = errors = False
    if request.method == 'POST':
        success = False
        form = UserIssueForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
        else:
            errors = True
    return render(request, "main/contact.html", {'success':success, 'errors':errors})


def shipping(request):
    return render(request, "main/shipping.html")

def cart(request):
    cart_items = list()
    num_items = 0
    total = 0
    for i in request.session['cart']:
        product = Product.objects.get(id=i['id'])
        photo = ProductPhoto.objects.filter(product=product)[0]
        qty = i['quantity']
        num_items += qty
        price = product.price * qty
        cart_items.append({'product':product, 'quantity':qty, 'price':price, 'photo':photo})
        total += price
    return render(request, "main/cart.html", context={'cart':cart_items, 'total':total, 'num_items':num_items})


def make_order(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save()
            order = Order.objects.create(buyer=address)
            for item in request.session['cart']:
                product = Product.objects.get(id=item['id'])
                quantity = item['quantity']
                OrderItem.objects.create(order=order, item=product, quantity=quantity, cost=product.price*quantity)
            request.session['cart'] = None
            request.session.save()
            return redirect('view-order', order_id=order.order_id)
        else:
            return render(request, "main/make-order.html", context={'cart':cart_items, 'total':total, 'num_items':num_items, 'errors':True})
    
    else:
        cart_items = list()
        num_items = 0
        total = 0
        for i in request.session['cart']:
            product = Product.objects.get(id=i['id'])
            photo = ProductPhoto.objects.filter(product=product)[0]
            qty = i['quantity']
            num_items += qty
            price = product.price * qty
            cart_items.append({'product':product, 'quantity':qty, 'price':price, 'photo':photo})
            total += price
        return render(request, "main/make-order.html", context={'cart':cart_items, 'total':total, 'num_items':num_items})


def view_order(request, order_id):
    order = Order.objects.get(order_id=order_id)
    items = order.items.all()
    item_total = 0
    for item in items:
        item_total += item.cost
    return render(request, "main/view-order.html", context={'order':order, 'items':items, 'item_total':item_total})

@ajax
def categories(request):
    cats = ProductCategory.objects.filter(products__quantity__gt=0)
    cats = list(set(cats))
    return {'categories': cats}


@ajax
def cart_manager(request):
    request.session.set_expiry = 604800
    if not request.session.get('cart', None):
        request.session['cart'] = list()
    if request.method == 'POST':
        cart = request.session['cart']
        total = 0
        items = 0
        p_id, p_qty, action = request.POST.get('id'), request.POST.get('quantity'), request.POST.get('action')
        if p_qty:
            p_qty = int(p_qty)
        
        if action == 'update':
            for item in cart:
                if item['id'] == p_id:
                    item['quantity'] = p_qty
                    items += p_qty
                    product = Product.objects.get(id=p_id)
                    item_price = product.price * p_qty
                    total += item_price
                    status = 'updated!'
                else:
                    items += item['quantity']
                    this_product = Product.objects.get(id=item['id'])
                    this_product_price = this_product.price * item['quantity']
                    total += this_product_price
            request.session['cart'] = cart
            request.session.save()
            return {'text':status, 'total':str(total), 'items':items, 'itemPrice': str(item_price)}
        
        elif action == 'add':
            found = False
            product = Product.objects.get(id=p_id)
            for item in cart:
                if item['id'] == p_id:
                    found = True
                    product = Product.objects.get(id=p_id)
                    if (item['quantity'] + p_qty) <= product.quantity:
                        item['quantity'] += p_qty
                    else:
                        item['quantity'] = product.quantity
                    status = 'ADDED!'
                items += item['quantity']
                total += product.price * item['quantity']
            if not found:
                cart.append({'id':p_id,'quantity':p_qty})
                items += p_qty
                total += product.price * p_qty
                status = 'ADDED!'
            request.session['cart'] = cart
            request.session.save()
            return {'text':status, 'total':str(total), 'items':items}
        
        elif action == 'delete':
            for item in cart:
                if item['id'] == p_id:
                    cart.remove(item)
                    status = f'{Product.objects.get(id=p_id).name} has been removed from your cart.'
                else:
                    items += item['quantity']
                    product = Product.objects.get(id=item['id'])
                    item_price = product.price * item['quantity']
                    total += item_price
            request.session['cart'] = cart
            request.session.save()
            return {'text':status, 'total':str(total), 'items':items}
    else:
        num = 0
        for item in request.session['cart']:
                num += item['quantity']
        return {'num_items':num}
