from django.core.management.base import BaseCommand

import numpy as np
import pandas as pd

from demo.football.models import League, SPIGlobalRank, SPIMatch, Team


class Command(BaseCommand):
    help = "Import the demo data"

    def import_global(self):
        global_url = "https://projects.fivethirtyeight.com/soccer-api/club/spi_global_rankings.csv"
        global_data = pd.read_csv(global_url)
        global_data = global_data.replace({np.nan: None})

        SPIGlobalRank.objects.all().delete()  # clear down for re-runs

        for index, row in global_data.iterrows():
            team, _ = Team.objects.get_or_create(
                name=row["name"],
                league=League.objects.get_or_create(name=row["league"])[0],
            )
            SPIGlobalRank.objects.create(
                rank=row["rank"],
                prev_rank=row["prev_rank"],
                team=team,
                offence=row["off"],
                defence=row["def"],
                spi=row["spi"],
            )

        print("Import of global ranks completed.")

    def import_matches(self):
        matches_url = "https://projects.fivethirtyeight.com/soccer-api/club/spi_matches_latest.csv"
        matches_data = pd.read_csv(matches_url)
        matches_data = matches_data.replace({np.nan: None})

        SPIMatch.objects.all().delete()  # clear down for re-runs

        for index, row in matches_data.iterrows():
            league = League.objects.get_or_create(name=row["league"])[0]
            team_one, _ = Team.objects.get_or_create(name=row["team1"], league=league)
            team_two, _ = Team.objects.get_or_create(name=row["team2"], league=league)
            SPIMatch.objects.create(
                season=row["season"],
                date=row["date"],
                team_one=team_one,
                team_two=team_two,
                spi_one=row["spi1"],
                spi_two=row["spi2"],
                prob_one=row["prob1"],
                prob_two=row["prob2"],
                prob_tie=row["probtie"],
                proj_score_one=row["proj_score1"],
                proj_score_two=row["proj_score2"],
                importance_one=row["importance1"],
                importance_two=row["importance2"],
                score_one=row["score1"],
                score_two=row["score2"],
                xg_one=row["xg1"],
                xg_two=row["xg2"],
                nsxg_one=row["nsxg1"],
                nsxg_two=row["nsxg2"],
                adj_score_one=row["adj_score1"],
                adj_score_two=row["adj_score2"],
            )

        print("Import of global ranks completed.")

    def handle(self, *args, **options):
        self.import_global()
        self.import_matches()
