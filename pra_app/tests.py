import pytest
from django.template.loader import render_to_string
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import Client
from pra_app.models import Game, Movie, Genre, Review
from pra_app.forms import LoginForm, ReviewForm
from decimal import Decimal
from django.core.exceptions import ValidationError


# TESTS FOR VIEWS

class ViewsTestCase(TestCase):
    """
    Test group for client related views on the app (access rights to certain views related to login and register oneself)
    """

    def setUp(self):
        """
        Function that sets up the client built in object to use during the tests.
        """
        self.client = Client()

    def test_landing_page_view(self):
        """
        Test function that checks if the main landing page is accessible and visible from the client side.
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_view_get(self):
        """
        Test function that checks if the login page is accessible and if the login form can also be accessed.
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_login_view_post_valid(self):
        """
        Test function which creates a test user and checks if the login attempt with those data will provide response
        of positive login attempt
        """
        user = User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 302)

    def test_login_view_post_invalid(self):
        """
        Test function that checks and validates unsuccessfull login attempt where the testuser account does not exist
        on the database
        """
        response = self.client.post(reverse('login'), {'username': 'nonexistent', 'password': 'incorrect'})
        self.assertEqual(response.status_code, 200)  # Should stay on the login page
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('Invalid username or password', str(response.content))

    def test_register_view_get(self):
        """
        Test function that checks if the register resource is accessible from the client side.
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')


class GameViewTestCase(TestCase):
    """
    Class group for game oriented views that are created on the app
    """

    def setUp(self):
        """
        Test function that creates a client instance (using the built-in Client repository) and creates
        test game, genre objects. This is to set up the initial state or environment for the test case.
        """
        self.client = Client()
        self.game = Game.objects.create(title='Test Game', release_date='2023-01-01')
        self.genre = Genre.objects.create(name='Action')
        self.game.genres.add(self.genre)

    def test_games_view(self):
        """
        Test function that checks if the list of all games page is accessible and visible from the client side.
        """
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'games.html')

    def test_game_details_view(self):
        """
        Test function which checks if certain game details page is accessible and visible from the client side.
        """
        response = self.client.get(reverse('game_details', args=[self.game.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'game-details.html')

    def test_game_edit_view_unauthenticated(self):
        """
        Test function that validates if the game edit resource is accessible from the client side.
        """
        response = self.client.get(reverse('game_edit', args=[self.game.id]))
        self.assertEqual(response.status_code, 302)


class MovieViewTestCase(TestCase):
    """
    Class group for movie oriented views that are created on the app
    """

    def setUp(self):
        """
        Test function that sets up a client instance and creates test movie with genre that will be used at later
        movie related tests
        """
        self.client = Client()
        self.movie = Movie.objects.create(title='Test Movie', release_date='2023-01-01')
        self.genre = Genre.objects.create(name='Drama')
        self.movie.genres.add(self.genre)

    def test_movies_view(self):
        """
        Test function
        """
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies.html')

    def test_movie_details_view(self):
        """
        Test function that checks if the movie details resource is accessible from the client side
        """
        response = self.client.get(reverse('movie_details', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movie-details.html')

    def test_movie_edit_view_unauthenticated(self):
        """
        Test function that validates if unauthenticated user is able to edit specific movie details.
        Expected response is the 302 response that will redirect the test user to login page.
        """
        response = self.client.get(reverse('movie_edit', args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)


class ReviewFormTestCase(TestCase):
    """
    Class group of tests that are related to review cases available on the app
    """

    def test_review_form_valid(self):
        """
        Test function that checks if the review provided by the test case is valid (fits the criteria)
        """
        form_data = {'description': 'Test review', 'rating': 5}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_review_form_invalid(self):
        """
        Test function that checks if the review provided by the test case is exceeding the set criteria
        """
        form_data = {'description': 'Test review', 'rating': 11}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())


# TESTS FOR MODELS

class ReviewModelTestCase(TestCase):
    """
    Class for model oriented tests on the app
    """

    def setUp(self):
        """
        Test function that sets up a test user case. This instance creates a game and movie for testing
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.genre = Genre.objects.create(name='Comedy')
        self.game = Game.objects.create(title='Test Game', release_date='2023-01-01', description='Description')
        self.game.genres.add(self.genre)
        self.movie = Movie.objects.create(title='Test Movie', release_date='2023-01-01', description='Description')
        self.movie.genres.add(self.genre)

    def test_review_creation(self):
        """
        Test function that adds to the model a test review. The review data are within the set criteria
        """
        review = Review.objects.create(user=self.user, game=self.game, rating=Decimal('8.5'), description='Good game')
        self.assertEqual(str(review), 'Review by testuser')
        self.assertEqual(review.rating, Decimal('8.5'))
        self.assertEqual(review.description, 'Good game')

    def test_review_invalid_rating(self):
        """
        Test function that creates invalid review.
        """
        with self.assertRaises(ValidationError) as context:
            review = Review(user=self.user, game=self.game, rating=Decimal('11'), description='Invalid rating')
            review.full_clean()

        self.assertEqual(
            str(context.exception.messages[0]),
            'Ensure this value is less than or equal to 10.'
        )

    def test_review_no_game_or_movie(self):
        """
        Test function that checks if it is possible to create review where no movie or game is selected or existing.
        """
        review = Review(user=self.user, rating=Decimal('8.5'), description='Review without game or movie')

        try:
            review.save()
        except ValidationError as e:
            self.assertEqual(
                e.message_dict,
                {'__all__': ['A review must be associated with either a game or a movie, but not both.']}
            )

    def test_review_with_movie(self):
        """
        Test function which validates properly written review for movies (in range of set criteria)
        """
        review = Review.objects.create(user=self.user, movie=self.movie, rating=Decimal('7.2'),
                                       description='Nice movie')
        self.assertEqual(str(review), 'Review by testuser')
        self.assertEqual(review.rating, Decimal('7.2'))
        self.assertEqual(review.description, 'Nice movie')

    def test_review_with_game(self):
        """
        Test function which validates properly written review for games (in range of set criteria)
        """
        review = Review.objects.create(user=self.user, game=self.game, rating=Decimal('9.0'),
                                       description='Fantastic game')
        self.assertEqual(str(review), 'Review by testuser')
        self.assertEqual(review.rating, Decimal('9.0'))
        self.assertEqual(review.description, 'Fantastic game')


# TESTS FOR URL'S

class URLTestCase(TestCase):
    """
    Class for URL accessibility test group
    """

    def setUp(self):
        """
        Test function that creates a test user case.
        """
        self.test_user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

    def test_main_url(self):
        """
        Test function that checks if the landing page (main page) is accessible
        """
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 200)

    def test_login_url(self):
        """
        Test function that checks if the login page is accessible
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_game_list_url(self):
        """
        Test function that checks if the game list page is accessible
        """
        response = self.client.get(reverse('game_list'))
        self.assertEqual(response.status_code, 200)

    def test_movie_list_url(self):
        """
        Test function that checks if the movie list page is accessible
        """
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)

    def test_register_url(self):
        """
        Test function that checks if the user registration page is accessible
        """
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_game_add_url(self):
        """
        Test function that checks if the game add page is accessible and validates that logged users can access
        the resource (simulates login by test user)
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('game_add'))
        self.assertEqual(response.status_code, 200)

    def test_movie_add_url(self):
        """
        Test function that checks if the movie add page is accessible and validates that logged users can access
        the resource (simulates login by test user)
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('movie_add'))
        self.assertEqual(response.status_code, 200)

    def test_genre_add_url(self):
        """
        Test function that checks if the  genre add page is accessible and validates that logged users can access
        the resource (simulates login by test user)
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('genre_add'))
        self.assertEqual(response.status_code, 200)

    def test_search_results_url(self):
        """
        Test function that checks if the search result page is accessible
        """
        response = self.client.get(reverse('search_results'))
        self.assertEqual(response.status_code, 200)
