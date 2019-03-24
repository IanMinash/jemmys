from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from jemmys.main.models import Product


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['home', 'contact', 'shipping', 'cart', 'search-order', 'make-order', 'managers:dashboard']

    def location(self, obj):
        return reverse(obj)


class ProductSitemap(Sitemap):
    change_freq = "weekly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(quantity__gt=0)

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return reverse('view-product', kwargs={'slug':obj.slug})
