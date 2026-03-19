def test_404_handler(client):
    response = client.get("/a-url-that-does-not-exist")
    assert response.status_code == 404
    assert b'<h2 style="text-align: center;">Page not found</h2>' in response.data
