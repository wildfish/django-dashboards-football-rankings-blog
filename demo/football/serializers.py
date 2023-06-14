from typing import Any

from django.db.models import Case, Q, Sum, Value, When
from django.urls import reverse

import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dashboards.component.chart import ChartSerializer
from dashboards.component.table import TableSerializer

from demo.football.models import SPIGlobalRank, SPIMatch, Team


BIG_FIVE = [
    "Barclays Premier League",
    "German Bundesliga",
    "Spanish Primera Division",
    "Italy Serie A",
    "French Ligue 1",
]


class TeamRankTableSerializer(TableSerializer):
    class Meta:
        columns = {
            "rank": "Rank #",
            "prev_rank": "Prev #",
            "team__name": "Team",
            "team__league__name": "League",
            "offence": "Offence",
            "defence": "Defence",
            "spi": "SPI",
        }

    def get_queryset(self, *args, **kwargs):
        return SPIGlobalRank.objects.all().select_related("team", "team__league")

    def get_team__name_value(self, obj):
        league_url = reverse(
            "dashboards:football_teamdashboard_detail", args=(obj.team.pk,)
        )
        return f'<a href="{league_url}">{obj.team.name}</a>'

    def get_team__league__name_value(self, obj):
        league_url = reverse(
            "dashboards:football_leaguedashboard_detail", args=(obj.team.league.pk,)
        )
        return f'<a href="{league_url}">{obj.team.league.name}</a>'


class LeagueTableSerializer(TableSerializer):
    class Meta:
        columns = {
            "position": "#",
            "name": "Team",
            "home_games": "Home games",
            "home_points": "Home points",
            "home_gd": "Home GD",
            "away_points": "Away points",
            "away_games": "Away games",
            "away_gd": "Away GD",
            "games": "Games",
            "gd": "Goal Diff",
            "points": "Points",
        }
        order = ["position"]

    def get_queryset(self, *args, object=None, **kwargs):
        return Team.objects.calculate_table(league=object)

    def get_name_value(self, obj):
        league_url = reverse("dashboards:football_teamdashboard_detail", args=(obj.pk,))
        return f'<a href="{league_url}">{obj.name}</a>'


class TopSPIbyLeagueSerializer(ChartSerializer):
    def get_queryset(self, *args, **kwargs):
        return (
            SPIGlobalRank.objects.values("team__league__name")
            .annotate(total=Sum("spi"))
            .values("team__league__name", "total")
            .order_by("-total")[:10]
        )

    def to_fig(self, data: Any) -> go.Figure:
        fig = px.bar(
            data,
            x=data["team__league__name"],
            y=data["total"],
        )
        return fig

    class Meta:
        title = "Leagues with highest overall SPI"


class BigFiveSPIbyLeagueSerializer(ChartSerializer):
    def get_queryset(self, *args, **kwargs):
        return SPIGlobalRank.objects.values(
            "rank", "team__name", "team__league__name", "spi"
        ).filter(team__league__name__in=BIG_FIVE)

    def to_fig(self, data: Any) -> go.Figure:
        data["inverse_rank"] = data["rank"].values[::-1]
        fig = px.scatter(
            data,
            x="spi",
            y="rank",
            color="team__league__name",
            size="inverse_rank",
            hover_data=["team__name"],
        )
        fig["layout"]["yaxis"]["autorange"] = "reversed"
        return fig

    class Meta:
        title = "Big 5 SPI spread"


class OffenceVsDefenceSerializer(ChartSerializer):
    def get_queryset(self, *args, **kwargs):
        return SPIGlobalRank.objects.values(
            "rank", "offence", "defence", "spi", "team__name"
        )

    def to_fig(self, data: Any) -> go.Figure:
        data["rank_group"] = pd.cut(data["rank"], 5, labels=False)
        fig = go.Figure()
        fig.add_trace(go.Box(y=data["offence"], x=data["rank_group"], name="Offence"))
        fig.add_trace(go.Box(y=data["defence"], x=data["rank_group"], name="Defence"))
        fig.update_traces(boxpoints="all", jitter=0)
        fig["layout"]["xaxis"]["autorange"] = "reversed"
        return fig

    class Meta:
        title = "Offence vs Defence, teams split into 5 ranks 0 being the best."


class XGSerializer(ChartSerializer):
    def get_queryset(self, *args, object=None, **kwargs):
        return (
            SPIMatch.objects.filter(Q(team_one=object) | Q(team_two=object))
            .annotate(
                xg=Case(
                    When(team_one=object, then="xg_one"),
                    default="xg_two",
                ),
                actual=Case(
                    When(team_one=object, then="score_one"),
                    default="score_two",
                ),
                home_or_away=Case(
                    When(team_one=object, then=Value("home")),
                    default=Value("away"),
                ),
                vs=Case(
                    When(team_one=object, then="team_two__name"),
                    default="team_one__name",
                ),
            )
            .values("xg", "date", "home_or_away", "vs", "actual")
        )

    def to_fig(self, data: Any) -> go.Figure:
        fig = px.scatter(
            data,
            x="date",
            y="xg",
            color="home_or_away",
            hover_data=["vs", "actual"],
        )
        return fig
