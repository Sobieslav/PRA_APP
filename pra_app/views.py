from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.contrib import messages

from .forms import ReviewForm, LoginForm, GameAddForm, MovieAddForm, AddGenreForm, SearchForm, GameEditForm
from .models import Game, Movie, Review, Genre, User


class LandingPageView(View):
    """
    landing page view - main page of the app
    """

    def get(self, request):
        return render(request, 'index.html')


class LoginView(View):
    """
    Login page view - used to log users to the app
    Requires existing account on the database in order to be logged in.
    """

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"Username: {username}, Password: {password}")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'main')
                return redirect(next_url)

        error_message = form.error_messages.get('invalid_login', 'Invalid username or password. Please try again.')
        return render(request, 'login.html', {'form': form, 'error_message': error_message})


class RegisterView(View):
    """
    New user register page view - used to register new users to the app
    """

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        email = request.POST['email']

        if password != confirm_password:
            return render(request, 'register.html', {'error_message': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error_message': 'Username already exists'})

        user = User(username=username, password=make_password(password), email=email)
        user.save()

        return redirect('/login/')


class GamesView(View):
    """
    View containing list of all games that are on the database, sorted by their names alphabetically
    Paginator is set to include 5 results per page (can be extended)
    """
    template_name = 'games.html'
    games_per_page = 5

    def get(self, request):
        sort_by = request.GET.get('sort_by', 'title')
        games = Game.objects.all().order_by(sort_by)
        paginator = Paginator(games, self.games_per_page)
        page = request.GET.get('page')

        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'games': games})


class GameDetailsView(View):
    """
    A view to show the specific game details once selected at GamesView view.
    """

    template_name = 'game-details.html'

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        reviews = Review.objects.filter(game_id=game)
        total_score = sum(review.rating for review in reviews)
        average_score = total_score / len(reviews) if reviews else 0
        genres = game.genres.all()
        return render(request, self.template_name, {'game': game, 'average_score': average_score, 'genres': genres})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddGameReviewView(View):
    """
    View containing the option to write game reviews for registered users
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    template_name = 'game-rev.html'

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        form = ReviewForm()
        return render(request, self.template_name, {'game': game, 'form': form})

    def post(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.game = game
            review.user = request.user
            review.save()
            # Redirect to a success page or back to the game details page
            return redirect('game_details', game_id=game_id)  # Adjust the URL name as needed
        return render(request, self.template_name, {'game': game, 'form': form})


class ViewGameReviewsView(View):
    """
    View containing a list of all reviews that a certain game received.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    template_name = 'view-game-reviews.html'

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        reviews = Review.objects.filter(game_id=game_id).select_related('user')

        return render(request, self.template_name, {'game': game, 'reviews': reviews})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class GameAddView(View):
    """
    View for adding a new game to the database.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """

    template_name = 'add-game.html'

    def get(self, request):
        form = GameAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = GameAddForm(request.POST)
        if form.is_valid():
            game = form.save()
            return redirect('game_details', game_id=game.id)
        return render(request, self.template_name, {'form': form})


class MoviesView(View):
    """
    View containing list of all movies available on the database, sorted by their names
    Paginator is set to include 5 results per page (can be tweaked)
    """
    template_name = 'movies.html'
    movies_per_page = 5

    def get(self, request):
        sort_by = request.GET.get('sort_by', 'title')
        movies = Movie.objects.all().order_by(sort_by)
        paginator = Paginator(movies, self.movies_per_page)
        page = request.GET.get('page')

        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'movies': movies})


class MovieDetailsView(View):
    """
    A view to show the specific movie details when selected from MoviesView view.
    """

    template_name = 'movie-details.html'

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        genres = movie.genres.all()
        return render(request, self.template_name, {'movie': movie, 'genres': genres})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class MovieReviewAddView(View):
    """
    Resource for adding a movie review for selected movie.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    template_name = 'movie-rev.html'

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        form = ReviewForm()
        return render(request, self.template_name, {'movie': movie, 'form': form})

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('movie_details', movie_id=movie.id)

        return render(request, self.template_name, {'movie': movie, 'form': form})


class MovieReviewsView(View):
    """
    View containing a list of all reviews for a certain movie.
    """
    template_name = 'view-movie-reviews.html'

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        reviews = Review.objects.filter(movie_id=movie_id).select_related('user')

        return render(request, self.template_name, {'movie': movie, 'reviews': reviews})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class MovieAddView(View):
    """
    View for adding a new movie to the database.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """

    template_name = 'add-movie.html'

    def get(self, request):
        form = MovieAddForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = MovieAddForm(request.POST)
        if form.is_valid():
            movie = form.save()
            return redirect('movie_details', movie_id=movie.id)  # You should have a movie_details URL defined
        return render(request, self.template_name, {'form': form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class AddGenreView(CreateView):
    """
    Resource to add new genre to the database. Once added it can be added to specific games/movies when needed.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    model = Genre
    form_class = AddGenreForm
    template_name = 'add-genre.html'
    success_url = reverse_lazy('genre_add')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        if Genre.objects.filter(name=name).exists():
            form.add_error('name', 'Genre already exists.')
            return self.form_invalid(form)

        # Genre does not exist, proceed to save it
        messages.success(self.request, 'Genre added successfully.')
        return super().form_valid(form)


class SearchResultsView(View):
    """
    Resource that searches on the game and movie database titles that fit the search criteria.
    Returns list of games and movies that fit the search criteria
    """
    template_name = 'search-results.html'

    def get(self, request):
        form = SearchForm()
        query = request.GET.get('query')

        games = []
        movies = []

        if query:
            games = Game.objects.filter(title__icontains=query)
            movies = Movie.objects.filter(title__icontains=query)

        context = {
            'form': form,
            'query': query,
            'games': games,
            'movies': movies,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class GameEditView(View):
    """
    Resource that allows to edit already created game details.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    template_name = 'game-edit.html'

    def get(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        form = GameEditForm(instance=game)
        return render(request, self.template_name, {'game': game, 'form': form})

    def post(self, request, game_id):
        game = get_object_or_404(Game, pk=game_id)
        form = GameEditForm(request.POST, instance=game)
        if form.is_valid():
            form.save()
            return redirect('game_details', game_id=game.id)  # Redirect to the game details page
        return render(request, self.template_name, {'game': game, 'form': form})


@method_decorator(login_required(login_url='/login/'), name='dispatch')
class MovieEditView(View):
    """
    Resource that allows to edit already created movie details.
    If accessed as unknown user (not logged in or anonymous) the user is redirected to login page
    """
    template_name = 'movie-edit.html'

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        form = MovieAddForm(instance=movie)
        return render(request, self.template_name, {'form': form, 'movie': movie})

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        form = MovieAddForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_details', movie_id=movie.id)  # Redirect to movie details page
        return render(request, self.template_name, {'form': form, 'movie': movie})
