from django.contrib import admin

from demo.football.models import League, SPIGlobalRank, SPIMatch, Team


class SPIMatchAdmin(admin.ModelAdmin):
    list_filter = ("team_one", "team_two", "team_one__league__name")


admin.site.register(League)
admin.site.register(Team)
admin.site.register(SPIGlobalRank)
admin.site.register(SPIMatch, SPIMatchAdmin)
