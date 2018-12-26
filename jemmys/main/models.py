from django.db import models


class Product(models.Model):
    """Model definition for a Product."""

    name = models.CharField(max_length=65)
    description = models.CharField(max_length=800)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=30)

    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        """Unicode representation of Product."""
        return f"{self.name} - {self.price}"


class ProductPhoto(models.Model):
    """Model definition for a Product's Photos."""

    photo = models.ImageField(upload_to='product_photos')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for ProductPhotos."""

        verbose_name = 'Product Photo'
        verbose_name_plural = 'Product Photos'

    def __str__(self):
        """Unicode representation of ProductPhotos."""
        return f"{self.product.name}'s photo"
