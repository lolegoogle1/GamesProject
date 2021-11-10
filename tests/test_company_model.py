

def test_get_companies(companies, client):
    response = client.get('/api/companies')

    assert response.status_code == 200
    assert len(response.get_json()) == 1

    assert  response.get_json()[0] == {
        'description': 'TestDescription',
        'founded_date': '2000-01-01',
        'games': [],
        'id': 1,
        'name': 'TestCompany'
    }


def test_create_company(user_headers, client):
    response = client.post('/api/companies', json={
        'description': 'TestDescription',
        'founded_date': '2000-01-01',
        'name': 'TestCompany'
    }, headers=user_headers)

    assert response.status_code == 200
    assert  response.get_json()['name'] == 'TestCompany'
    assert response.get_json()['description'] == 'TestDescription'
    assert response.get_json()['founded_date'] == '2000-01-01'


def test_update_company(companies, user_headers, client):
    response = client.put(f'/api/companies/{companies.id}', json={
        'name': 'Updated',
        'description': 'Updated',
        'founded_date': '2021-01-01'
    }, headers=user_headers)
    assert response.status_code == 200
    assert response.get_json()['name'] == 'Updated'
    assert response.get_json()['description'] == 'Updated'
    assert response.get_json()['founded_date'] == '2021-01-01'


def test_delete_company(companies, user_headers, client):
    response = client.delete(f'/api/companies/{companies.id}', headers=user_headers)
    assert response.status_code == 204