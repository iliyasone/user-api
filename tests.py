import requests

# Set the base URL of the FastAPI app
BASE_URL = "http://127.0.0.1:8000"

def test_get_posts():
    response = requests.get(f"{BASE_URL}/posts?skip=0&limit=10")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Expecting a list of posts
    print("GET /posts passed")

def test_get_post(post_id):
    response = requests.get(f"{BASE_URL}/posts/{post_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert "label" in json_response  # Expecting a post with 'label'
    assert "content" in json_response
    assert "rating" in json_response
    print(f"GET /posts/{post_id} passed")

def test_create_post():
    new_post = {
        "label": "Test Post",
        "content": "This is a test post.",
        "hideRating": False
    }
    response = requests.put(f"{BASE_URL}/posts", json=new_post)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["label"] == new_post["label"]
    assert json_response["content"] == new_post["content"]
    print("PUT /posts passed")
    return json_response["id"] 

def test_vote_on_post(post_id):
    vote_data = {
        "vote": 1  # Upvote the post
    }
    response = requests.post(f"{BASE_URL}/posts/{post_id}/vote", json=vote_data)
    assert response.status_code == 200
    json_response = response.json()
    assert "rating" in json_response  # Expecting the updated rating
    print(f"POST /posts/{post_id}/vote passed")

def test_delete_vote(post_id):
    # Send a DELETE request to remove the vote
    response = requests.delete(f"{BASE_URL}/posts/{post_id}/vote")
    assert response.status_code == 200  # Expecting success

    json_response = response.json()
    assert "rating" in json_response  
    assert not json_response['isVoted']
    print(f"DELETE /posts/{post_id}/vote passed")

if __name__ == "__main__":
    test_get_posts()
    post_id = test_create_post()
    print(post_id)
    test_get_post(post_id)
    test_vote_on_post(post_id)
    test_delete_vote(post_id)