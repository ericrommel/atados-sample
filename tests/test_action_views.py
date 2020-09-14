from tests.conftest import get_url


def test_list_actions_without_login_view(app, client):
    """
    Test list actions without login - List will be shown
    """

    target_url = get_url(app=app, url="action.list_actions")
    response = client.get(target_url)
    assert response.status_code == 200


def test_list_actions_with_login_non_admin_view(app, auth, client):
    """
    Test list actions with login but with no access permission (non-admin user) - List will be shown
    """

    target_url = get_url(app=app, url="action.list_actions")
    auth.login(a_dict=dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_list_actions_with_login_admin_view(app, auth, client):
    """
    Test list actions with login and the user has access permission (is an admin user) - List will be shown
    """

    target_url = get_url(app=app, url="action.list_actions")
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_actions_details_without_login_view(app, client):
    """
    Test list actions details without login (a redirection should be done) - It will be shown
    """

    target_url = get_url(app=app, url="action.list_actions", id=1)
    response = client.get(target_url)
    assert response.status_code == 200


def test_actions_details_with_login_non_admin_view(app, auth, client):
    """
    Test list actions details with login but with no access permission (non-admin user) - It will be shown
    """

    target_url = get_url(app=app, url="action.list_actions", id=1)
    auth.login(a_dict=dict(email="non-admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_actions_details_with_login_admin_view(app, auth, client):
    """
    Test list actions_details with login and the user has access permission (is an admin user) - It will be shown
    """

    target_url = get_url(app=app, url="action.list_actions", id=1)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 200


def test_action_detail_does_not_exist_view(app, auth, client):
    """
    Test list action detail whose doesn't exist
    """

    target_url = get_url(app=app, url="action.action_detail", id=10000000)
    auth.login(a_dict=dict(email="admin@admin.com", password="123456"))
    response = client.get(target_url)
    assert response.status_code == 404
