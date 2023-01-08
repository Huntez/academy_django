from django.db import models

# Create your models here.

class Product(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Cost = models.DecimalField(
        
    )
    
