from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from .models import Review, Game, Movie, Genre


class ReviewForm(forms.ModelForm):
    """
    Basic form that allows logged users to write reviews
    Checks if the selected score is from 1-10 range.
    """
    rating = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="Rating must be at least 1."),
            MaxValueValidator(10, message="Rating must be at most 10."),
        ]
    )

    class Meta:
        model = Review
        fields = ['description', 'rating']


class LoginForm(forms.Form):
    """
    Form which allows to log users to the app.
    Provides error message when login or password will not match any credentials stored on the database
    """
    username = forms.CharField(label="Login")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    error_messages = {
        'invalid_login': 'Invalid username or password. Please try again.',
    }


class GameAddForm(forms.ModelForm):
    """
    Simple form that allows for logged users to add new games to the database
    """
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Game
        fields = ['title', 'release_date', 'description', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MovieAddForm(forms.ModelForm):
    """
    Simple form that allows for logged users to add new movies to the database
    """
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'description', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }


class AddGenreForm(forms.ModelForm):
    """
    Simple form that allows for logged users to add new genres to the database
    """

    class Meta:
        model = Genre
        fields = ['name']


class SearchForm(forms.Form):
    """
    Form that allows users to search for movies or games that met the search criteria
    """
    query = forms.CharField(max_length=100, label='Search')


class GameEditForm(forms.ModelForm):
    """
    Form that allows for logged users to be able to edit already existing game details
    """
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Game
        fields = ['title', 'release_date', 'description', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }


class MovieEditForm(forms.ModelForm):
    """
    Form that allows for logged users to be able to edit already existing movie details
    """
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Movie
        fields = ['title', 'release_date', 'description', 'genres']
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
        }
