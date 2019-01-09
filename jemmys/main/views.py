from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, ProductPhoto, ProductCategory
from django_ajax.decorators import ajax

# Create your views here.

def home(request):
    context = dict()
    context['products'] = list()
    if request.GET.get('category'):
        all_products = Product.objects.filter(category__category=request.GET['category'])
    elif request.GET.get('name'):
        all_products = Product.objects.filter(name=request.GET['name'])
    else:
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
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        product = self.get_object()
        context['photos'] = ProductPhoto.objects.filter(product=product)
        # Other products of the same category
        others = Product.objects.exclude(id__exact=context['product'].id).filter(category__exact=context['product'].category)
        context['others'] = list()
        for other in others:
            photos = ProductPhoto.objects.filter(product=other)[:2]
            product = {'details':other, 'photos':list()}
            product['photos'] = [*photos]
            context['others'].append(product)
        print(others)
        return context


def about(request):
    return render(request, "main/about.html")


@ajax
def categories(request):
    cats = ProductCategory.objects.filter(products__quantity__gt=0)
    cats = list(set(cats))
    return {'categories': cats}
