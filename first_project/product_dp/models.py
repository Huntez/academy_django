from django.db import models
from django.core.validators import  MinValueValidator 
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    Name = models.CharField(
        max_length=10,
    )
    Info = models.CharField(
        max_length=100
    )

    def __str__(self):
        return str(self.Name)

class Product(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    Category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.Name)

class Users_Cart(models.Model):
    user_chat_id = models.PositiveBigIntegerField()
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.product)
