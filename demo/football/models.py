from django.db import models
from django.db.models import (
    Case,
    Count,
    F,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
    Window,
)
from django.db.models.functions import Rank
from django.utils.timezone import now


class League(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TeamQuerySet(models.QuerySet):
    def calculate_table(self, league):
        (
            home_games,
            away_games,
            home_points,
            away_points,
            home_gd,
            away_gd,
        ) = SPIMatch.objects.table_annotations()

        return (
            self.filter(league=league)
            .annotate(
                home_games=Subquery(home_games),
                away_games=Subquery(away_games),
                games=F("home_games") + F("away_games"),
                home_points=Subquery(home_points),
                away_points=Subquery(away_points),
                points=F("home_points") + F("away_points"),
                home_gd=Subquery(home_gd),
                away_gd=Subquery(away_gd),
                gd=F("home_gd") + F("away_gd"),
            )
            .annotate(
                position=Window(expression=Rank(), order_by=["-points", "-gd"]),
            )
            .order_by("position")
        )


class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    objects = TeamQuerySet.as_manager()

    def __str__(self):
        return self.name


class SPIGlobalRank(models.Model):
    rank = models.IntegerField()
    prev_rank = models.IntegerField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    offence = models.DecimalField(max_digits=4, decimal_places=2)
    defence = models.DecimalField(max_digits=4, decimal_places=2)
    spi = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return str(self.rank)


class SPIMatchQuerySet(models.QuerySet):
    def played(self):
        return self.filter(date__lt=now())

    def upcoming(self):
        return self.filter(date__gte=now())

    def result(self, team):
        return (
            self.filter(Q(team_one=team) | Q(team_two=team))
            .annotate(
                result=Case(
                    When(score_two__gt=F("score_one"), team_two=team, then=Value("w")),
                    When(score_one__gt=F("score_two"), team_one=team, then=Value("w")),
                    When(score_two=F("score_one"), then=Value("d")),
                    default=Value("l"),
                ),
            )
            .order_by("-date")
        )

    def home_subquery(self):
        return (
            SPIMatch.objects.played()
            .filter(team_one__pk=OuterRef("pk"))
            .order_by()
            .values("team_one")
        )

    def away_subquery(self):
        return (
            SPIMatch.objects.played()
            .filter(team_one__pk=OuterRef("pk"))
            .order_by()
            .values("team_one")
        )

    def table_annotations(self):
        home = (
            SPIMatch.objects.played()
            .filter(team_one__pk=OuterRef("pk"))
            .order_by()
            .values("team_one")
        )
        home_points = home.annotate(
            points=Sum(
                Case(
                    When(score_one__gt=F("score_two"), then=3),
                    When(score_one=F("score_two"), then=1),
                    default=0,
                )
            )
        ).values("points")
        home_games = home.annotate(games=Count("team_two")).values("games")
        home_gd = home.annotate(gd=Sum("score_one") - Sum("score_two")).values("gd")

        away = (
            SPIMatch.objects.played()
            .filter(team_two__pk=OuterRef("pk"))
            .order_by()
            .values("team_two")
        )
        away_games = away.annotate(games=Count("team_one")).values("games")
        away_points = away.annotate(
            points=Sum(
                Case(
                    When(score_two__gt=F("score_one"), then=3),
                    When(score_two=F("score_one"), then=1),
                    default=0,
                )
            )
        ).values("points")
        away_gd = away.annotate(gd=Sum("score_two") - Sum("score_one")).values("gd")
        return home_games, away_games, home_points, away_points, home_gd, away_gd


class SPIMatch(models.Model):
    season = models.IntegerField()
    date = models.DateField()
    team_one = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_team"
    )
    team_two = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_team"
    )
    spi_one = models.DecimalField(max_digits=4, decimal_places=2)
    spi_two = models.DecimalField(max_digits=4, decimal_places=2)
    prob_one = models.DecimalField(max_digits=5, decimal_places=4)
    prob_two = models.DecimalField(max_digits=5, decimal_places=4)
    prob_tie = models.DecimalField(max_digits=5, decimal_places=4)
    proj_score_one = models.DecimalField(max_digits=4, decimal_places=2)
    proj_score_two = models.DecimalField(max_digits=4, decimal_places=2)
    importance_one = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    importance_two = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    score_one = models.IntegerField(null=True, blank=True)
    score_two = models.IntegerField(null=True, blank=True)
    xg_one = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    xg_two = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    nsxg_one = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    nsxg_two = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    adj_score_one = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )
    adj_score_two = models.DecimalField(
        max_digits=4, decimal_places=2, null=True, blank=True
    )

    objects = SPIMatchQuerySet.as_manager()

    def __str__(self):
        if self.score_one is not None and self.score_two is not None:
            return f"{self.date}: {self.team_one.name} ({self.score_one}) vs {self.team_two.name} ({self.score_two})"
        return f"{self.date}: {self.team_one.name} vs {self.team_two.name}"
