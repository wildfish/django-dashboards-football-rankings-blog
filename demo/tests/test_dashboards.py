from django.urls import reverse

import pytest
from model_bakery import baker

from demo.football.dashboards import LeagueDashboard, RankingsDashboard, TeamDashboard
from demo.football.models import League, Team


pytestmark = pytest.mark.django_db()


@pytest.fixture(autouse=True)
def rankings_url():
    return reverse("dashboards:football_rankingsdashboard")


@pytest.fixture(autouse=True)
def league_url():
    league = baker.make(League)
    return reverse("dashboards:football_leaguedashboard_detail", args=(league.pk,))


@pytest.fixture(autouse=True)
def team_url():
    team = baker.make(Team)
    return reverse("dashboards:football_teamdashboard_detail", args=(team.pk,))


def test_rankings__expected_dashboard_and_components(
    rankings_url, client, django_assert_num_queries
):
    with django_assert_num_queries(0):
        response = client.get(rankings_url)

    dashboard = response.context["dashboard"]
    assert isinstance(dashboard, RankingsDashboard)
    assert len(dashboard.components) == 4
    assert sum(d.is_deferred for d in dashboard.components.values()) == 4


def test_league__expected_dashboard_and_components(
    league_url, client, django_assert_num_queries
):
    with django_assert_num_queries(1):
        response = client.get(league_url)

    dashboard = response.context["dashboard"]
    assert isinstance(dashboard, LeagueDashboard)
    assert len(dashboard.components) == 1
    assert sum(d.is_deferred for d in dashboard.components.values()) == 1


def test_team__expected_dashboard_and_components(
    team_url, client, django_assert_num_queries
):
    with django_assert_num_queries(4):
        response = client.get(team_url)

    dashboard = response.context["dashboard"]
    assert isinstance(dashboard, TeamDashboard)
    assert len(dashboard.components) == 3
    assert sum(d.is_deferred for d in dashboard.components.values()) == 1
