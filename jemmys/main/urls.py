from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home, about, contact, ProductDetailView, categories, cart_manager, cart, variants

urlpatterns = [
    path('', home, name='home'),
    path('view/<slug:slug>', ProductDetailView.as_view(), name='view_product'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('cats', categories, name='cats'),
    path('cart', cart, name='cart'),
    path('cart-manager', cart_manager, name='cart-manager'),
    path('variant-info', variants, name='variant-info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
