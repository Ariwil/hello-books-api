def test_get_all_books_with_no_records(client): #We pass in the client fixture here, which we registered in conftest.py.
    #ACT
    response = client.get("/books") #This sends an HTTP request to /books. It returns an HTTP response object
    response_body = response.get_json()

    #ASSERT
    assert response.status_code == 200
    assert response_body == []