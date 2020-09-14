from flask import redirect

from tests.conftest import get_url


def test_list_volunteers_without_login_view(app, client):
    """
    Test list volunteers without login (a redirection should be done) - List will be shown
    """

    target_url = get_url(app=app, url="volunteer.list_volunteers")
    response = client.get(target_url)
    assert response.status_code == 200


def test_list_volunteers_with_login_view(app, auth, client):
    """
    Test list volunteers with login - List will be shown
    """

    target_url = get_url(app=app, url="volunteer.list_volunteers")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_detail_volunteers_without_login_view(app, client):
    """
    Test detail volunteers without login (a redirection should be done) - It will be shown
    """

    target_url = get_url(app=app, url="volunteer.volunteer_detail", id=1)
    response = client.get(target_url)
    assert response.status_code == 200


def test_detail_volunteers_with_login_view(app, auth, client):
    """
    Test detail volunteers with login -  - It will be shown
    """

    target_url = get_url(app=app, url="volunteer.volunteer_detail", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_detail_volunteer_that_does_not_exist_view(app, auth, client):
    """
    Test detail volunteer that does not exist
    """

    target_url = get_url(app=app, url="volunteer.volunteer_detail", id=1000000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 404


def test_add_volunteers_without_login_view(app, auth, client):
    """
    Test add volunteers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="volunteer.add_volunteer")
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="three@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    response = auth.generic_post(target_url, a_dict)
    assert response.status_code == 201


def test_add_volunteers_with_login_view(app, auth, client):
    """
    Test add volunteers with login
    """

    target_url = get_url(app=app, url="volunteer.add_volunteer")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="three@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    response = auth.generic_post(target_url, a_dict)
    assert response.status_code == 201


def test_add_volunteer_that_already_exists_view(app, auth, client):
    """
    Test add volunteer that already exists
    """

    target_url = get_url(app=app, url="volunteer.add_volunteer")
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="one@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    response = auth.generic_post(target_url, a_dict)
    assert response.status_code == 403


def test_edit_volunteers_without_login_view(app, auth, client):
    """
    Test edit volunteers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="volunteer.edit_volunteer", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.put(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_edit_volunteers_with_login_non_admin_view(app, auth, client):
    """
    Test edit volunteers with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="volunteer.edit_volunteer", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="three@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 403


def test_edit_volunteers_with_login_admin_view(app, auth, client):
    """
    Test edit volunteers with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="volunteer.edit_volunteer", id=1)
    auth.login(dict(email="admin@admin.com", password="123456"))
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="three@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 200


def test_edit_volunteer_that_does_not_exist_view(app, auth, client):
    """
    Test edit volunteer that does not exist
    """

    target_url = get_url(app=app, url="volunteer.edit_volunteer", id=1000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.put(target_url)
    assert response.status_code == 404


def test_edit_volunteer_using_value_that_already_exist_view(app, auth, client):
    """
    Test edit volunteer using a value that already exist in the database
    """

    target_url = get_url(app=app, url="volunteer.edit_volunteer", id=1)
    a_dict = dict(
        first_name="First Name",
        last_name="Last Name",
        email="one@volunteer.com",
        district="District IX",
        city="Budapest",
    )
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = auth.generic_put(target_url, a_dict)
    assert response.status_code == 200


def test_delete_volunteers_without_login_view(app, auth, client):
    """
    Test delete volunteers without login (a redirection should be done)
    """

    target_url = get_url(app=app, url="volunteer.delete_volunteer", id=1)
    redirect_url = redirect(get_url(app=app, url="auth.login", next_url=target_url))
    response = client.delete(target_url)
    assert response.status_code == 302
    assert redirect_url.data == response.data


def test_delete_volunteers_with_login_non_admin_view(app, auth, client):
    """
    Test delete volunteers with login but with no access permission (non-admin user)
    """

    target_url = get_url(app=app, url="volunteer.delete_volunteer", id=1)
    auth.login(dict(email="non-admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 403


def test_delete_volunteers_with_login_admin_view(app, auth, client):
    """
    Test delete volunteers with login and the user has access permission (is an admin user)
    """

    target_url = get_url(app=app, url="volunteer.delete_volunteer", id=1)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 200


def test_delete_volunteer_that_does_not_exist_view(app, auth, client):
    """
    Test delete volunteer that does not exist
    """

    target_url = get_url(app=app, url="volunteer.delete_volunteer", id=1000)
    auth.login(dict(email="admin@admin.com", password="123456"))
    response = client.delete(target_url)
    assert response.status_code == 404
