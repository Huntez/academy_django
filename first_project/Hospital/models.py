from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.db import models

# Create your models here.

class Department(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    building = models.PositiveIntegerField(
        null=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Financing = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    def __str__(self):
        return self.Name

class Disease(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Severity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )

    def __str__(self):
        return self.Name

class Doctor(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )   
    Surname = models.CharField(
        unique=True,
        max_length=100
    )
    Phone = models.CharField(
        max_length=10,
    )
    Salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return self.Name

class Examination(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    ) 
    DayOfWeek = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)]
    )
    StartTime = models.TimeField()
    EndTime = models.TimeField()

    def save(self, *args, **kwargs):
        if self.EndTime < self.StartTime:
            self.EndTime = self.StartTime
        else:
            pass
        super(Examination, self).save(*args, **kwargs)

    def __str__(self):
        return self.Name

class Ward(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=20
    )
    Floor = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    Building = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return self.Name
