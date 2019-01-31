from django.contrib import admin
from .models import Product, ProductPhoto, ProductCategory, Order, OrderItem, BuyerAddress, UserIssue

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductPhoto)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(BuyerAddress)
admin.site.register(OrderItem)
admin.site.register(UserIssue)