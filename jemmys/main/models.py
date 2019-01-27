from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from djmoney.models.fields import MoneyField
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string


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
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)], default=0)
    variant_of = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name='variants', blank=True, null=True)
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
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images")

    class Meta:
        """Meta definition for ProductPhotos."""

        verbose_name = 'Product Photo'
        verbose_name_plural = 'Product Photos'

    def __str__(self):
        """Unicode representation of ProductPhotos."""
        return f"{self.product.name}'s photo"


class BuyerAddress(models.Model):
    """Model definition for a Buyer's Address."""

    name = models.CharField(max_length=70)
    street = models.CharField(max_length=70)
    house = models.CharField(max_length=70, blank=True, null=True)
    city = models.CharField(max_length=30)
    region = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    country = models.CharField(max_length=30)

    class Meta:
        """Meta definition for BuyerAddress."""

        verbose_name = 'Buyer Address'
        verbose_name_plural = 'Buyer Addresses'

    def __str__(self):
        """Unicode representation of BuyerAddress."""
        return f"{self.name} of {self.street}"


def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator(instance):
    order_new_id = random_string_generator()

    Klass = instance.__class__

    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return id_generator(instance)
    return order_new_id


class Order(models.Model):
    """Model definition for an Order."""

    STATUSES = (
        ('P', 'Pending'),
        ('C', 'Canceled'),
        ('F', 'Fulfilled'),
    )

    order_id = models.CharField(max_length=7, unique=True, blank=True)
    total = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=0)
    shipping = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=200)
    status = models.CharField(max_length=1, choices=STATUSES, default='P')
    buyer = models.ForeignKey(
        BuyerAddress, on_delete=models.CASCADE, related_name='orders')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Order."""

        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        """Unicode representation of Order."""
        return self.order_id

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_id = id_generator(self)
        super(Order, self).save(*args, **kwargs)


class OrderItem(models.Model):
    """An item in an order."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    cost = MoneyField(max_digits=14, decimal_places=2, default_currency='KES', default=0)
     

    class Meta:
        """Meta definition for Order Item."""

        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        """Unicode representation of Order Item."""
        return f'[{self.order.order_id}] {self.item.name} - {self.cost}'

    def save(self, *args, **kwargs):
        self.cost = self.item.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)    


@receiver(post_save, sender=OrderItem)
def minus_usage(sender, instance, **kwargs):
    cost = instance.cost
    order = instance.order
    order.total = order.total + cost
    order.save()