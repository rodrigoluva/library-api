from fastapi import status


def test_health_check(client):
    response = client.get('/health_check')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': '200 OK'}
