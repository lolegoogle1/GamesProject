

def test_model(user):
    assert user.name == 'TestUser'


def test_user_login(user, client):
    response = client.post('/users/login', json={
        'login': user.login,
        'password': 'TestPassword'
    })
    assert response.status_code == 200
    assert response.get_json().get('access_token')


def test_user_reg(client):
    response = client.post('/users/signup', json={
        'name': 'TestUser',
        'login': 'TestUserTestLogin',
        'password': 'TestPassword'
    })
    assert response.status_code == 200
    assert response.get_json().get('access_token')