from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductPhoto

# Create your views here.

def home(request):
    context = dict()
    context['products'] = list()
    all_products = Product.objects.all()
    for prod in all_products:
        photos = ProductPhoto.objects.filter(product=prod)[:2]
        product = {'details':prod, 'photos':list()}
        product['photos'] = [*photos]
        context['products'].append(product)
    return render(request, "main/home.html", context=context)



class ProductDetailView(DetailView):
    model = Product
    template_name = "main/product.html"



def about(request):
    return render(request, "main/about.html")

