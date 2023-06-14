from dashboards.component import Chart, Table, Text
from dashboards.dashboard import Dashboard, ModelDashboard
from dashboards.registry import registry

from demo.football.components import MatchForm
from demo.football.models import League, SPIMatch, Team
from demo.football.serializers import (
    BigFiveSPIbyLeagueSerializer,
    LeagueTableSerializer,
    OffenceVsDefenceSerializer,
    TeamRankTableSerializer,
    TopSPIbyLeagueSerializer,
    XGSerializer,
)


class RankingsDashboard(Dashboard):
    teams = Table(defer=TeamRankTableSerializer, grid_css_classes="span-12")
    top_spi_by_league = Chart(defer=TopSPIbyLeagueSerializer, grid_css_classes="span-6")
    big_five_spi_by_league = Chart(
        defer=BigFiveSPIbyLeagueSerializer, grid_css_classes="span-6"
    )
    offence_vs_defence = Chart(
        defer=OffenceVsDefenceSerializer, grid_css_classes="span-12"
    )

    class Meta:
        name = "Global Football SPI Rankings"


class LeagueDashboard(ModelDashboard):
    table = Table(defer=LeagueTableSerializer, grid_css_classes="span-12", page_size=20)

    class Meta:
        name = "League"
        model = League


class TeamDashboard(ModelDashboard):
    current_position = Text(grid_css_classes="span-3")
    recent_form = MatchForm(
        value=lambda **k: SPIMatch.objects.played().result(team=k["object"])[:5],
        grid_css_classes="span-9",
    )
    performance = Chart(defer=XGSerializer, grid_css_classes="span-12")

    class Meta:
        model = Team

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._meta.name = self.object.name

    def get_current_position_value(self, *args, **kwargs):
        table = Team.objects.calculate_table(league=self.object.league)
        for team in table:
            if team == self.object:
                return f"#{team.position}"


registry.register(RankingsDashboard)
registry.register(LeagueDashboard)
registry.register(TeamDashboard)
