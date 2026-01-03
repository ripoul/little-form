def test_404_handler(client):
    response = client.get("/une-url-qui-nexiste-pas")
    assert response.status_code == 404
    assert b'<h2 style="text-align: center;">Page not found</h2>' in response.data
