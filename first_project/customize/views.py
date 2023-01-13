import csv
import json
import datetime

from telebot.types import Location
from .models import GameModel, MatchModel
from django.http import HttpResponse
# Create your views here.

def upload_data(request):
    with open('vgsales.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)
            try:
                created = GameModel.objects.get_or_create(

                    platform=row[2],
                    name=row[1],
                    year=datetime.date(int(row[3]), 1, 1),
                    genre=row[4],
                    publisher=row[5],
                    na_sales=row[6],
                    eu_sales=row[7],
                    jp_sales=row[8],
                    other_sales=row[9],
                    global_sales=row[10],
                )
            except:
                pass
    return HttpResponse("Done!")

def json_upload(request):
    with open('test.json') as f:
        reader = json.load(f)
        for row in reader:
            try:
                created = MatchModel.objects.get_or_create(

                    MatchNumber = row['MatchNumber'],
                    RoundNumber = row['RoundNumber'],
                    DateUtc = row['DateUtc'],
                    Location = row['Location'],
                    HomeTeam = row['HomeTeam'],
                    AwayTeam = row['AwayTeam'],
                    Group = row['Group'],
                    HomeTeamScore = row['HomeTeamScore'],
                    AwayTeamScore = row['AwayTeamScore'],
                )
            except:
                pass
    return HttpResponse("Done!")

def text_load(request):
    try:
        file = open('text.txt', 'w')
        for row in MatchModel.objects.all():
            file.write(f'\nMatchNumber - {row.MatchNumber}\
                       \nRoundNumber - {row.RoundNumber}\
                       \nDateUtc - {row.DateUtc}\
                       \nLocation - {row.Location}\
                       \nHomeTeam - {row.HomeTeam}\
                       \nAwayTeam - {row.AwayTeam}\
                       \nGroup - {row.Group}\
                       \nHomeTeamScore - {row.HomeTeamScore}\
                       \nAwayTeamScore - {row.AwayTeamScore}\
                       \n***')
    except:
        pass
    return HttpResponse("Done!")
