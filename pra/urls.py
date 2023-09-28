"""
URL configuration for pra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from pra_app.views import LandingPageView, LoginView, GamesView, MoviesView, RegisterView, AddGameReviewView, \
    GameDetailsView, ViewGameReviewsView, GameAddView, MovieDetailsView, MovieReviewAddView, MovieReviewsView, \
    MovieAddView, AddGenreView, SearchResultsView, GameEditView, MovieEditView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='main'),
    path('login/', LoginView.as_view(), name='login'),
    path('games/', GamesView.as_view(), name='game_list'),
    path('games/<game_id>', GameDetailsView.as_view(), name='game_details'),
    path('view-game-reviews/<game_id>', ViewGameReviewsView.as_view(), name='view_game_reviews'),
    path('movies/', MoviesView.as_view(), name='movie_list'),
    path('movies/<movie_id>', MovieDetailsView.as_view(), name='movie_details'),
    path('register/', RegisterView.as_view(), name='register'),
    path('games/review/<game_id>/', AddGameReviewView.as_view(), name="game_rev"),
    path('games/add/', GameAddView.as_view(), name='game_add'),
    path('movies/review/<movie_id>', MovieReviewAddView.as_view(), name='movie_rev'),
    path('view-movie-reviews/<movie_id>', MovieReviewsView.as_view(), name='view_movie_reviews'),
    path('movies/add/', MovieAddView.as_view(), name='movie_add'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('genre/add/', AddGenreView.as_view(), name='genre_add'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('games/<game_id>/edit', GameEditView.as_view(), name='game_edit'),
    path('movies/<movie_id>/edit', MovieEditView.as_view(), name='movie_edit'),

]
