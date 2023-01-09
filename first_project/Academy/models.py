from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

class Curator(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Surname = models.CharField(
        unique=True,
        max_length=100
    )

    def __str__(self):
        return str(self.Name)
class Department(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Building = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    Financing = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    FacultyId = models.ForeignKey('Facultie', on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
class Facultie(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Dean = models.CharField(
        max_length=255
    )
    Financing = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return self.Name

class Group(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=10
    )
    Rating = models.PositiveIntegerField(validators = [MaxValueValidator(5)])
    Year = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    DepartmentId = models.ForeignKey('Department', on_delete=models.CASCADE)

    def __str__(self):
        return self.Name
    
class GroupsCurator(models.Model):
    CuratorId = models.ForeignKey('Curator', on_delete=models.CASCADE)
    GroupId = models.ForeignKey('Group', on_delete=models.CASCADE)

class GroupsLecture(models.Model):
    LectureId = models.ForeignKey('Lecture', on_delete=models.CASCADE)
    GroupId = models.ForeignKey('Group', on_delete=models.CASCADE)

class GroupsStudents(models.Model):
    GroupId = models.ForeignKey('Group', on_delete=models.CASCADE)
    StundetId = models.ForeignKey('Student', on_delete=models.CASCADE)

class Lecture(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=255
    )
    SubjectId = models.ForeignKey('Subject', on_delete=models.CASCADE)
    # TeacherId = models.ForeignKey('Teacher', on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Student(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )
    Surname = models.CharField(
        unique=True,
        max_length=100
    )
    Rating = models.PositiveIntegerField(validators = [MaxValueValidator(5)])

class Subject(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )

    def __str__(self):
        return self.Name

class Teacher(models.Model):
    Name = models.CharField(
        unique=True,
        max_length=100
    )   
    Surname = models.CharField(
        unique=True,
        max_length=100
    )
    EmploymentDate = models.DateField()
    isAssistant = models.BooleanField(default=False)
    isTeacher = models.BooleanField(default=False)
    Position = models.CharField(max_length=255)
    Salary = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    Premium = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    def clean(self):
        if self.EmploymentDate < date(1990,1,1):
            raise ValidationError("Cant be lower than 1990y")
        if not self.isAssistant and not self.isTeacher:
            raise ValidationError("Cant be not teacher and not assistant!")

    def __str__(self):
        return self.Name 
