import pytest

from types import SimpleNamespace
import random
import string

from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.models import User, Review


def test_index(client):
    resp = client.get("/")
    assert resp.status_code == 200

    search = SimpleNamespace(search_query="guardians", submit="Search")
    form = SearchForm(formdata=None, obj=search)
    response = client.post("/", data=form.data, follow_redirects=True)

    assert b"Guardians of the Galaxy" in response.data


@pytest.mark.parametrize(
    ("query", "message"),
    [
        ("", "This field is required."),  # Empty query test case
        ("a", "Too many results"),  # Very short string test case
        ("".join(random.choices(string.ascii_letters + string.digits, k=20)), "Movie not found"),  # Gibberish string test case
        ("".join(random.choices(string.ascii_letters + string.digits, k=101)), "Field must be between 1 and 100 characters long.")  # Too long string test case
    ]
)
def test_search_input_validation(client, query, message):
    # Create a search form with the given query
    search = SimpleNamespace(search_query=query, submit="Search")
    form = SearchForm(formdata=None, obj=search)
    # Post the form to the index route
    response = client.post("/", data=form.data, follow_redirects=True)
    # Check if the expected error message is in the response
    assert message.encode('utf-8') in response.data


def test_movie_review(client, auth):
    # Register and login
    auth.register(username="testuser", email="testuser@example.com", passwrd="testpassword", confirm="testpassword")
    auth.login(username="testuser", password="testpassword")

    # The movie ID for 'Guardians of the Galaxy'
    guardians_id = "tt2015381"
    url = f"/movies/{guardians_id}"

    # Generate a random review content
    review_content = ''.join(random.choices(string.ascii_letters + string.digits, k=50))

    # Submit a movie review
    review = SimpleNamespace(text=review_content, submit="Enter Comment")
    form = MovieReviewForm(formdata=None, obj=review)
    response = client.post(url, data=form.data, follow_redirects=True)

    # Test that the review shows up on the page
    assert review_content.encode('utf-8') in response.data

    # Test that the review is saved in the database
    assert Review.objects(content=review_content).count() == 1





@pytest.mark.parametrize(
    "movie_id, status_code, message",
    [
        ("", 404, None),  # Empty movie_id should give a 404
        ("tt123", 200, "Incorrect IMDb ID"),  # Too short
        ("tt1234567", 200, "Movie not found"),  # Invalid but correct length
        ("tt123456789", 200, "Incorrect IMDb ID"),  # Too long
    ]
)
def test_movie_review_redirects(client, movie_id, status_code, message):
    url = f"/movies/{movie_id}"
    response = client.get(url)
    assert response.status_code == status_code
    if message:
        assert message in response.get_data(as_text=True)

@pytest.mark.parametrize(
    ("comment", "message"), 
    (
    )
)
def test_movie_review_input_validation(client, auth, comment, message):
    assert False


    

    
