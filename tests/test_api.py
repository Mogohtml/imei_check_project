import pytest
from app.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_check_imei_api(client):
    response = client.post('/api/imei/check-imei', json={
        'imei': '123456789012345',
        'token': 'valid_token_1'
    })
    assert response.status_code == 200
    assert 'error' not in response.json
