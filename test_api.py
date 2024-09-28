import requests
import pytest

# Set the base URL of the FastAPI app
BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def new_post():
    return {
        "label": "Test Post",
        "content": "This is a test post.",
        "hideRating": False
    }

@pytest.fixture
def post_id(new_post):
    response = requests.put(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["label"] == new_post["label"]
    assert json_response["content"] == new_post["content"]
    return json_response["id"]  # Fixture now returns the post ID

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of posts

def test_get_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert "label" in json_response  # Expecting a post with 'label'
    assert "content" in json_response
    assert "rating" in json_response

def test_vote_on_post(post_id):
    vote_data = {"vote": 1}  # Upvote the post
    response = requests.post(f"{BASE_URL}/posts/{post_id}/vote", json=vote_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "rating" in json_response  # Expecting the updated rating
    assert json_response['vote'] == 1

def test_delete_vote(post_id):
    # Upvote the post first
    requests.post(f"{BASE_URL}/posts/{post_id}/vote", json={"vote": 1})

    # Send a DELETE request to remove the vote
    response = requests.delete(f"{BASE_URL}/posts/{post_id}/vote")
    assert response.status_code == 200  # Expecting success

    json_response = response.json()
    assert "rating" in json_response  
    assert json_response['vote'] == 0
