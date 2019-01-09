from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField

class ProductCategory(models.Model):
    """Model definition for a Product's Category."""

    category = models.CharField(max_length=50)

    class Meta:
        """Meta definition for Product Category."""

        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'

    def __str__(self):
        """Unicode representation of Product Category."""
        return self.category

class Product(models.Model):
    """Model definition for a Product."""

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1500)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='KES')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    slug = models.SlugField(blank=True)

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
