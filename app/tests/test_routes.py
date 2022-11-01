def test_get_all_books_with_no_records(client): #We pass in the client fixture here, which we registered in conftest.py.
    #ACT
    response = client.get("/books") #This sends an HTTP request to /books. It returns an HTTP response object
    response_body = response.get_json()

    #ASSERT
    assert response.status_code == 200
    assert response_body == []

def test_get_one_book(client, two_saved_books): #can add multiple fixtures
    #ACT
    response = client.get("/books/1")
    response_body = response.get_json()

    #ASSERT
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Ocean Book",
        "description": "watr 4evr"
    }

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "New Book",
        "description": "The Best!"
    })
    response_body = response.get_json() #could alternatively use response.get_data(as_text=True), if we hadn't jsonified the response body in our POST/books route

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book successfully created"