from django.db import models

# Create your models here.
class GameModel(models.Model):    
    name = models.CharField(max_length=64)    
    platform = models.CharField(max_length=64)    
    year = models.DateField()
    genre = models.CharField(max_length=64)    
    publisher = models.CharField(max_length=64)    
    na_sales = models.FloatField()    
    eu_sales = models.FloatField()    
    jp_sales = models.FloatField() 
    other_sales = models.FloatField()   
    global_sales = models.FloatField()

    def __str__(self):        
        return f"{self.id}_{self.name}"


class MatchModel(models.Model):
    MatchNumber = models.SmallIntegerField()
    RoundNumber = models.SmallIntegerField()
    DateUtc = models.DateTimeField()
    Location = models.CharField(max_length=100)
    HomeTeam = models.CharField(max_length=100)
    AwayTeam = models.CharField(max_length=100)
    Group = models.CharField(max_length=100, blank=True, null=True)
    HomeTeamScore = models.SmallIntegerField()
    AwayTeamScore =  models.SmallIntegerField()

    def __str__(self):
        return str(self.Location)
    
