def test_get_all_genres_with_no_records(client):
    # Act
    response = client.get("/genres")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

def test_get_one_with_two_saved_genres(client, two_saved_genres):
    # Act
    response = client.get("/genres/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "fiction"
    }

def test_create_one_genre(client):
    # Act
    response = client.post("/genres", json={
        "name": "novel"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "novel"
    }
