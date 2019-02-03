from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home, contact, ProductDetailView, categories, cart_manager, cart, variants, make_order, view_order, order_search, shipping

urlpatterns = [
    path('', home, name='home'),
    path('view/<slug:slug>', ProductDetailView.as_view(), name='view-product'),
    path('contact', contact, name='contact'),
    path('shipping', shipping, name='shipping'),
    path('cats', categories, name='cats'),
    path('cart', cart, name='cart'),
    path('order/', include([
        path('', make_order, name='make-order'),
        path('search', order_search, name='search-order'),
        path('<order_id>', view_order, name='view-order'),
    ])),
    path('cart-manager', cart_manager, name='cart-manager'),
    path('variant-info', variants, name='variant-info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
