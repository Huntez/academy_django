import decimal
from django.db import models
from django.core.validators import  MinValueValidator 
from decimal import Decimal

# Create your models here.
class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(
        max_length=100,
    )
    info = models.CharField(
        max_length=100
    )

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(
        unique=True,
        max_length=100
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)

class Wallet(models.Model):
    user_chat_id = models.PositiveBigIntegerField()
    balance = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=3,
    )
    
    def __str__(self):
        return str(self.user_chat_id)

class Users_Cart(models.Model):
    user_chat_id = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.product)

class Subscription(models.Model):
    user_chat_id = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    exercises = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return str(self.user_chat_id)

class Sub_product(models.Model):
    name = models.CharField(max_length=50)
    days = models.PositiveIntegerField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return str(self.name)

class TrainingTime(models.Model):
    user_chat_id = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    star_time = models.TimeField()
    end_time = models.TimeField()

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    start_work = models.TimeField()
    end_work = models.TimeField()

class TrainerSignUp(models.Model):
    user_chat_id = models.ForeignKey('Subscription', on_delete=models.CASCADE)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
