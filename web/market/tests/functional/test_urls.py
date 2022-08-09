from flask import url_for, request

# test home page only


def test_home_page(client):
    response = client.get('/home')
    assert response.status_code == 200
    assert b'Home Page' in response.data

# test user login and logout redirects


def test_logout_redirect(client):
    # test login route
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Username' in response.data
    assert b'Password' in response.data

    # test user login
    response = client.post(
        '/login', data=dict(username='test1', password='testpass1'))
    assert response.status_code == 200

    # test user logout redirect
    response = client.get(url_for('account.logout_page'),
                          follow_redirects=True)
    assert response.status_code == 200
    assert request.path == url_for('account.home_page')
    assert b'Home Page' in response.data
