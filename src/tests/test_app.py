import pytest
import json
from app import app

@pytest.fixture
def client():
    """Fixture para cliente de prueba"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_devops_endpoint_success(client):
    """Prueba exitosa del endpoint /DevOps"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWV': 'test-jwt-12345',
        'Content-Type': 'application/json'
    }
    
    data = {
        "message": "This is a test",
        "to": "Juan Perez",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    
    response = client.post('/DevOps', json=data, headers=headers)
    
    assert response.status_code == 200
    assert response.json['message'] == 'Hello Juan Perez your message will be send'

def test_devops_endpoint_missing_api_key(client):
    """Prueba sin API Key"""
    headers = {'Content-Type': 'application/json'}
    data = {"test": "data"}
    
    response = client.post('/DevOps', json=data, headers=headers)
    assert response.status_code == 401

def test_devops_endpoint_wrong_api_key(client):
    """Prueba con API Key incorrecta"""
    headers = {
        'X-Parse-REST-API-Key': 'wrong-key-123',
        'X-JWT-KWV': 'test-jwt',
        'Content-Type': 'application/json'
    }
    data = {"message": "test"}
    
    response = client.post('/DevOps', json=data, headers=headers)
    assert response.status_code == 401

def test_devops_endpoint_missing_jwt(client):
    """Prueba sin JWT"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'Content-Type': 'application/json'
    }
    data = {"message": "test"}
    
    response = client.post('/DevOps', json=data, headers=headers)
    assert response.status_code == 401

def test_devops_endpoint_invalid_json(client):
    """Prueba con JSON inválido"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWV': 'test-jwt',
        'Content-Type': 'application/json'
    }
    
    # JSON mal formado
    response = client.post('/DevOps', data='not json', headers=headers)
    assert response.status_code == 400

def test_devops_endpoint_missing_field(client):
    """Prueba con campo faltante"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWV': 'test-jwt',
        'Content-Type': 'application/json'
    }
    
    # Falta el campo 'to'
    data = {
        "message": "This is a test",
        "from": "Rita Asturia",
        "timeToLifeSec": 45
    }
    
    response = client.post('/DevOps', json=data, headers=headers)
    assert response.status_code == 400

def test_devops_endpoint_wrong_method_get(client):
    """Prueba GET debe retornar ERROR"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWV': 'test-jwt'
    }
    
    response = client.get('/DevOps', headers=headers)
    assert response.status_code == 405
    assert response.data.decode() == 'ERROR'

def test_devops_endpoint_wrong_method_put(client):
    """Prueba PUT debe retornar ERROR"""
    headers = {
        'X-Parse-REST-API-Key': '2f5ae96c-b558-4c7b-a590-a501ae1c3f6c',
        'X-JWT-KWV': 'test-jwt'
    }
    
    response = client.put('/DevOps', headers=headers)
    assert response.status_code == 405
    assert response.data.decode() == 'ERROR'

def test_health_check(client):
    """Prueba endpoint de health check"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_not_found(client):
    """Prueba endpoint no existente"""
    response = client.get('/nonexistent')
    assert response.status_code == 404