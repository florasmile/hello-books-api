def test_get_all_authors_with_no_records(client):
    # Act
    response = client.get("/authors")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []

# do not have a get one author route
# def test_get_one_author(client, two_saved_authors):
#     # Act
#     response = client.get("/authors/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body == {
#         "id": 1,
#         "name": "Michelle Obama"
#     }

def test_create_one_author(client):
    # Act
    response = client.post("/authors", json={
        "name": "New Author"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "New Author"
    }
