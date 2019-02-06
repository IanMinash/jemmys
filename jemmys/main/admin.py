from django.contrib import admin
from .models import Product, ProductPhoto, ProductCategory, Order, OrderItem, BuyerAddress, UserIssue

# Register your models here.
admin.site.register(ProductPhoto)
admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(BuyerAddress)
admin.site.register(OrderItem)
admin.site.register(UserIssue)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "variant_of":
            kwargs["queryset"] = Product.objects.filter(variant_of=None)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)