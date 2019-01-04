from django.db import models
from django.utils.text import slugify
from djmoney.models.fields import MoneyField

class Product(models.Model):
    """Model definition for a Product."""

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=800)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    category = models.CharField(max_length=30)
    slug = models.SlugField()

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return f"{self.name} - {self.price}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)


class ProductPhoto(models.Model):
    """Model definition for a Product's Photos."""

    photo = models.ImageField(upload_to='product_photos')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        """Meta definition for ProductPhotos."""

        verbose_name = 'Product Photo'
        verbose_name_plural = 'Product Photos'

    def __str__(self):
        """Unicode representation of ProductPhotos."""
        return f"{self.product.name}'s photo"
