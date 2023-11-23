import pytest
from unittest.mock import patch, MagicMock
from docker import DockerClient
from app import app
import json

SECRET_KEY = 'my-secret-key'

# Fixture to set up the test client
@pytest.fixture
def client():
    # Set the app in testing mode
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test case for invalid token
def test_get_cpu_data_invalid_key(client):
    response = client.get('/data/cpu', headers={'Authorization': 'Bearer {}'.format('invalid key')})
    data = json.loads(response.data.decode('utf-8'))
    
    # Assert that the status code is 200 and the message indicates an invalid token
    assert response.status_code == 200
    assert data['message'] == 'token is invalid'

# Test case for valid CPU data retrieval
def test_get_cpu_data_valid_key(client):
    with patch('app.psutil.cpu_percent') as mock_cpu_percent:
        mock_cpu_percent.return_value = 50

        response = client.get('/data/cpu', headers={'Authorization': 'Bearer {}'.format(SECRET_KEY)})
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert that the status code is 200 and CPU percent is as expected
        assert response.status_code == 200
        assert data['cpu_percent'] == 50

# Test case for valid memory data retrieval
def test_get_memory_data_valid_key(client):
    with patch('app.psutil.virtual_memory') as mock_virtual_memory:
        mock_virtual_memory.return_value.free = 1024
        mock_virtual_memory.return_value.total = 2048

        response = client.get('/data/memory', headers={'Authorization': 'Bearer {}'.format(SECRET_KEY)})
        data = json.loads(response.data.decode('utf-8'))
        
        # Assert that the status code is 200 and memory data is as expected
        assert response.status_code == 200
        assert 'free_memory' in data
        assert 'total_memory' in data
        assert 'memory_usage' in data
        assert data['free_memory'] == 1024
        assert data['total_memory'] == 2048

# Test case for valid container statistics retrieval
def test_get_container_stats_valid_key(client):
    with patch('docker.from_env') as mock_docker_from_env:
        mock_client = MagicMock(spec=DockerClient)
        mock_container = MagicMock()
        mock_container.name = 'test_container'
        mock_stats = {'stats': 'some_stats'}

        # Configure mock objects for DockerClient and container
        mock_client.containers.list.return_value = [mock_container]
        mock_container.stats.return_value = mock_stats

        mock_docker_from_env.return_value = mock_client

        response = client.get('/data/containers/stats', headers={'Authorization': 'Bearer {}'.format(SECRET_KEY)})
        
        # Assert that the status code is 200 and container stats are as expected
        assert response.status_code == 200
        data = response.get_json()
        assert 'test_container' in data
        assert data['test_container'] == mock_stats
