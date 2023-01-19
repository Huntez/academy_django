from django.db import models
from django.core.validators import  MinValueValidator 
from decimal import Decimal

class User(models.Model):
    user_chat_id = models.PositiveBigIntegerField()
    on_workout = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user_chat_id)

    # Can be added name, surname, etc..

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
    user_chat_id = models.ForeignKey('User', on_delete=models.CASCADE)
    balance = models.DecimalField(
        default=0,
        max_digits=100,
        decimal_places=3,
    )
    
    def __str__(self):
        return str(self.user_chat_id)

class Users_Cart(models.Model):
    user_chat_id = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.product)

class Subscription(models.Model):
    user_chat_id = models.ForeignKey('User', on_delete=models.CASCADE)
    exercises = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return str(self.user_chat_id)

class Sub_product(models.Model):
    name = models.CharField(max_length=50)
    exercises = models.PositiveIntegerField()
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return str(self.name)

class Trainer(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    free = models.BooleanField()
    # start_work = models.TimeField() TODO
    # end_work = models.TimeField()

    def __str__(self):
        return str(self.name)

class TrainingTime(models.Model):
    user_chat_id = models.ForeignKey('User', on_delete=models.CASCADE)
    trainer = models.ForeignKey(
            'Trainer', 
            on_delete=models.CASCADE, 
            blank=True, 
            null=True
    )
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.user_chat_id)
