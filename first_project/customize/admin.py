import datetime
from django.contrib import admin
from customize.models import GameModel, MatchModel

class YearFilter(admin.SimpleListFilter):
    title = 'Year'
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = [(year, year.year)
                for year in model_admin.model.objects.dates(field_name='year', kind='year')]

        return sorted(years)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(year=self.value())
        else:
            return queryset


# class MatchYear(admin.SimpleListFilter):
#     title = 'Platform'
#     parameter_name = 'platform'
#
#     def lookups(self, request, model_admin):
#         date = [(location, location.) 
#                 for location in model_admin.model.objects.filter('Location')]
#
#         return sorted(date)
#
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(Location=self.value())
#         else:
#             return queryset

class GameAdmin(admin.ModelAdmin):
    list_display = ('name', 'publisher', 'platform', 'year', 'id')
    list_filter = (YearFilter, 'platform')
    search_fields = ('name', 'publisher')
    ordering = ('id',)

class MatchAdmin(admin.ModelAdmin):
    list_display = ('HomeTeam', 'AwayTeam', 'Location', 'MatchNumber', 'RoundNumber')
    list_filter = ('Location',)
    search_fields = ('HomeTeam', 'AwayTeam')
    ordering = ('id',)


# Register your models here.
admin.site.register(GameModel, GameAdmin)
admin.site.register(MatchModel, MatchAdmin)
