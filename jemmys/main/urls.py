from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import home, about, ProductDetailView

urlpatterns = [
    path('', home, name='home'),
    path('view/<slug:slug>', ProductDetailView.as_view(), name='view_product'),
    path('about', about, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
