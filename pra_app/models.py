from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField(max_length=124)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=124)
    release_date = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1,
                                 validators=[MinValueValidator(1), MaxValueValidator(10)])
    description = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username}"
