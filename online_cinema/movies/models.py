from django.db import models

class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
    )
    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    birth_year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    img_link = models.URLField(
        max_length=1000,
        null=True,
        blank=True
    )

    description = models.TextField(
        null=True,
        blank=True
    )

    duration = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    year = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.PROTECT,
        related_name='movies',
    )

    actors = models.ManyToManyField(
        Actor,
        related_name='movies',
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title