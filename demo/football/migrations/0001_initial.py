# Generated by Django 4.2 on 2023-04-13 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="League",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "league",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="football.league",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SPIMatch",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("season", models.IntegerField()),
                ("date", models.DateField()),
                ("spi_one", models.DecimalField(decimal_places=2, max_digits=4)),
                ("spi_two", models.DecimalField(decimal_places=2, max_digits=4)),
                ("prob_one", models.DecimalField(decimal_places=4, max_digits=5)),
                ("prob_two", models.DecimalField(decimal_places=4, max_digits=5)),
                ("prob_tie", models.DecimalField(decimal_places=4, max_digits=5)),
                ("proj_score_one", models.DecimalField(decimal_places=2, max_digits=4)),
                ("proj_score_two", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "importance_one",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                (
                    "importance_two",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=5, null=True
                    ),
                ),
                ("score_one", models.IntegerField(blank=True, null=True)),
                ("score_two", models.IntegerField(blank=True, null=True)),
                (
                    "xg_one",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "xg_two",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "nsxg_one",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "nsxg_two",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "adj_score_one",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "adj_score_two",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=4, null=True
                    ),
                ),
                (
                    "team_one",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="home_team",
                        to="football.team",
                    ),
                ),
                (
                    "team_two",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="away_team",
                        to="football.team",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SPIGlobalRank",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rank", models.IntegerField()),
                ("prev_rank", models.IntegerField(blank=True, null=True)),
                ("offence", models.DecimalField(decimal_places=2, max_digits=4)),
                ("defence", models.DecimalField(decimal_places=2, max_digits=4)),
                ("spi", models.DecimalField(decimal_places=2, max_digits=4)),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="football.team"
                    ),
                ),
            ],
        ),
    ]