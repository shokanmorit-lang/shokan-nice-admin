from django.db import models
from django.contrib.auth.models import User


class StoreModel(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    address = models.CharField(max_length=50, default="القيمة الافتراضية")
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    doc = models.FileField(upload_to='documents', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    gender_choice = [
        ('F', 'Female'),
        ('M', 'Male'),
        ('z', 'z')

    ]
    gender = models.CharField(max_length=1, choices=gender_choice)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store'


# =========================

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# =========================

class Product(models.Model):
    store = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


# =========================

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


# =========================

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}"
