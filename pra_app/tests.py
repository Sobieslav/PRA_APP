import pytest
from django.test import TestCase
from decimal import Decimal
from django.contrib.auth.models import User
from pra_app.models import Game, Movie, Genre, Review
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_login_user(client):
    """
    Login view test, created user should be able to login
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    user.save()

    response = client.get('/login/')
    assert response.status_code == 200
    response = client.post('/login/', {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_failed_login_user(client):
    """
    Test for login view. Incorrect data provided
    """
    user = User.objects.create_user(username='testuser', password='testpassword')
    user.save()

    response = client.get('/login/')
    assert response.status_code == 200
    response = client.post('/login/', {'username': 'tesssstuser111', 'password': 'testpassssssssword1111'})
    assert response.status_code == 200  # Return to login page but on the screen the error message is shown


class TestForUrlCases(TestCase):
    """
    Group of tests related for URL's that are created on the app
    """

    def test_landing_page_view(self):
        """
        Test function that checks if the landing page is accessible
        """
        response = self.client.get('/')
        assert response.status_code == 200

    def test_login_page_view(self):
        """
        Test function that checks if the login page is accessible
        """
        response = self.client.get('/login/')
        assert response.status_code == 200

    def test_logout_page_view(self):
        """
        Test function that checks if the logout page is accessible
        """
        response = self.client.post('/logout/')
        assert response.status_code == 200

    def test_register_page_view(self):
        """
        Test function that checks if the register page is accessible
        """
        response = self.client.get('/register/')
        assert response.status_code == 200

    def test_games_page_view(self):
        """
        Test function that checks if the game list page is accessible
        """
        response = self.client.get('/games/')
        assert response.status_code == 200

    def test_movies_page_view(self):
        """
        Test function that checks if the movie list page is accessible
        """
        response = self.client.get('/movies/')
        assert response.status_code == 200

    def test_game_add_view(self):
        """
        Test function that checks if the game add page is accessible. As the only way to add games to the database
        is to be logged in the expected result should be redirection to login page feedback (302)
        """
        response = self.client.get('/games/add/')
        assert response.status_code == 302

    def test_movie_add_view(self):
        """
        Test function that checks if the movie add page is accessible. As the only way to add movies to the database
        is to be logged in the expected result should be redirection to login page feedback (302)
        """
        response = self.client.get('/movies/add/')
        assert response.status_code == 302

    def test_genre_add_view(self):
        """
        Test function that checks if the genre add page is accessible. As the only way to add genres to the database
        is to be logged in the expected result should be redirection to login page feedback (302)
        """
        response = self.client.get('/genre/add/')
        assert response.status_code == 302

    def test_games_details_view(self):
        """
        Test to check if given game details are visible. This case the game does not exist therefore
        the 404 feedback is expected.
        """
        game_id = 999
        response = self.client.get(f'/games/{game_id}/')
        assert response.status_code == 404

    def test_movie_details_view(self):
        """
        Test to check if given movie details are visible. This case the movie does not exist therefore
        the 404 feedback is expected.
        """
        movie_id = 999
        response = self.client.get(f'/movies/{movie_id}/')
        assert response.status_code == 404

    def test_search_results_url(self):
        """
        Test function that checks if the search result page is accessible
        """
        response = self.client.get('/search/')
        assert response.status_code == 200

    def test_game_edit_view(self):
        """
        Test to check if given game details can be edited. This case the game does not exist therefore
        the 404 feedback is expected.
        """
        game_id = 999
        response = self.client.get(f'/games/{game_id}/edit/')
        assert response.status_code == 404

    def test_movie_edit_view(self):
        """
        Test to check if given movie details can be edited. This case the movie does not exist therefore
        the 404 feedback is expected.
        """
        movie_id = 999
        response = self.client.get(f'/movies/{movie_id}/edit/')
        assert response.status_code == 404


class TestsForReviews(TestCase):

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

    def test_review_with_movie(self):
        """
        Test function which validates properly written review for movies (in range of set criteria)
        """
        review = Review.objects.create(user=self.user, movie=self.movie, rating=Decimal('7.2'),
                                       description='Nice movie')
        expected_rating = Decimal('7.2')
        expected_description = 'Nice movie'

        assert review.rating == expected_rating
        assert review.description == expected_description

    def test_review_with_game(self):
        """
        Test function which validates properly written review for games (in range of set criteria)
        """
        review = Review.objects.create(user=self.user, game=self.game, rating=Decimal('9.0'),
                                       description='Fantastic game')
        expected_rating = Decimal('9.0')
        expected_description = 'Fantastic game'

        assert review.rating == expected_rating
        assert review.description == expected_description

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
                {'__all__': ['A review must be associated with either a game or a movie that exists on the database.']}
            )
