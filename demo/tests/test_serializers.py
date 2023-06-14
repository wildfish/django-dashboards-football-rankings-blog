import json

import pytest
from model_bakery import baker

from demo.football.models import League, SPIGlobalRank, SPIMatch, Team
from demo.football.serializers import (
    LeagueTableSerializer,
    TeamRankTableSerializer,
    XGSerializer,
)


pytestmark = pytest.mark.django_db()

"""
    Basic examples of how Dashboards can be tested.
"""


def test_team_rank_table_serializer():
    a, b = baker.make(SPIGlobalRank, _quantity=2)
    result = TeamRankTableSerializer().serialize()

    assert result.columns == {
        "rank": "Rank #",
        "prev_rank": "Prev #",
        "team__name": "Team",
        "team__league__name": "League",
        "offence": "Offence",
        "defence": "Defence",
        "spi": "SPI",
    }
    assert len(result.data) == 2
    assert result.data[0]["rank"] == a.rank
    assert result.data[1]["rank"] == b.rank


def test_team_rank_table_serializer__column_override__team_name():
    a, b = baker.make(SPIGlobalRank, _quantity=2)
    result = TeamRankTableSerializer().serialize()

    assert (
        result.data[0]["team__name"]
        == f'<a href="/dashboard/football/teamdashboard/{a.team.pk}/">{a.team.name}</a>'
    )
    assert (
        result.data[1]["team__name"]
        == f'<a href="/dashboard/football/teamdashboard/{b.team.pk}/">{b.team.name}</a>'
    )


def test_team_rank_table_serializer__no_data():
    result = TeamRankTableSerializer().serialize()

    assert len(result.data) == 0


def test_league_table_serializer():
    league = baker.make(League)
    a, b = baker.make(Team, league=league, _quantity=2)
    baker.make(Team, _quantity=1)
    serializer = LeagueTableSerializer()
    result = serializer.serialize(object=league)

    assert result.columns == {
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
    assert len(result.data) == 2


def test_league_table_serializer__column_override__team_name():
    league = baker.make(League)
    a, b = baker.make(Team, league=league, _quantity=2)
    baker.make(Team, _quantity=1)
    serializer = LeagueTableSerializer()
    result = serializer.serialize(object=league)

    assert (
        result.data[0]["name"]
        == f'<a href="/dashboard/football/teamdashboard/{a.pk}/">{a.name}</a>'
    )
    assert (
        result.data[1]["name"]
        == f'<a href="/dashboard/football/teamdashboard/{b.pk}/">{b.name}</a>'
    )


def test_league_table_serializer__no_data():
    result = LeagueTableSerializer().serialize()

    assert len(result.data) == 0


def test_xg_serializer():
    team_one, team_two = baker.make(Team, _quantity=2)
    a, b = baker.make(SPIMatch, team_one=team_one, team_two=team_two, _quantity=2)
    result = XGSerializer().serialize(object=team_one)
    data = json.loads(result)["data"][0]

    assert len(data["x"]) == 2
    assert data["x"][0] == str(a.date)
    assert data["x"][1] == str(b.date)


def test_xg_serializer__no_data():
    result = XGSerializer().serialize()

    assert json.loads(result) == {
        "layout": {
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "annotations": [
                {
                    "text": "XGSerializer - No data",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 28},
                }
            ],
        }
    }
