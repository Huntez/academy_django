from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.db import models
from django.utils import timezone

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

class Doctor(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )   
    Surname = models.CharField(
        unique=True,
        max_length=100
    )
    Premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    Salary = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )

    def __str__(self):
        return self.Name 

class DoctorsExamination(models.Model):
    StartTime = models.TimeField()
    EndTime = models.TimeField()
    DoctorId = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    ExaminationId = models.ForeignKey('Examination', on_delete=models.CASCADE)
    WardId = models.ForeignKey('Ward', on_delete=models.CASCADE)

    def clean(self):
        if self.EndTime <= self.StartTime:
            raise ValidationError("End time can't equal or lower than start time!")

class Donation(models.Model):
    Amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    Date = models.DateField()
    DepartmentId = models.ForeignKey('Department', on_delete=models.CASCADE)
    SponsorId = models.ForeignKey('Sponsor', on_delete=models.CASCADE)

    def clean(self):
        if self.Date > timezone.now():
            raise ValidationError('Date cant be greater than date now')

    def __str__(self):
        return self.Amount

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

    def clean(self):
        if self.Date > timezone.now():
            raise ValidationError('Date cant be greater than date now')

    def __str__(self):
        return self.Name

class Sponsor(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    ) 

class Ward(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=20
    )
    Places = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    DepartmentId = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
