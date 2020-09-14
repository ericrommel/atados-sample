from werkzeug.exceptions import abort


def test_400_bad_request(app, client):
    """
    Create route to abort the request with the 400 Bad Request
    """

    @app.route("/400")
    def bad_request():
        abort(400)

    response = client.get("/400")
    assert response.status_code == 400
    assert "400 Bad Request" in str(response.data)


def test_401_unauthorized(app, client):
    """
    Create route to abort the request with the 4001 Unauthorized
    """

    @app.route("/401")
    def unauthorized():
        abort(401)

    response = client.get("/401")
    assert response.status_code == 401
    assert "401 Unauthorized" in str(response.data)


def test_403_forbidden(app, client):
    """
    Create route to abort the request with the 403 Forbidden
    """

    @app.route("/403")
    def forbidden_error():
        abort(403)

    response = client.get("/403")
    assert response.status_code == 403
    assert "403 Forbidden" in str(response.data)


def test_404_not_found(app, client):
    """
    Access a page that does not exist
    """

    response = client.get("/notexistpage")
    assert response.status_code == 404
    assert "404 Not Found" in str(response.data)


def test_405_not_found(app, client):
    """
    Access a page that does not exist
    """

    @app.route("/405", methods=["DELETE"])
    def method_not_allowed():
        pass

    response = client.get("/405")
    assert response.status_code == 405
    assert "405 Method Not Allowed" in str(response.data)


def test_500_internal_server_error(app, client):
    """
    Create route to abort the request with the 500 Error
    """

    @app.route("/500")
    def internal_server_error():
        abort(500)

    response = client.get("/500")
    assert response.status_code == 500
    assert "500 Internal Server Error" in str(response.data)
