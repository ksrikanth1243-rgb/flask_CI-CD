# tests/test_routes.py
"""Test suite for Flask application routes"""

import pytest
import json
from app import create_app, db


class TestIndexRoute:
    """Tests for the index route"""
    
    def test_index_status_code(self, client):
        """Test index route returns 200 status code"""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_index_response_format(self, client):
        """Test index route returns JSON with expected fields"""
        response = client.get('/')
        data = json.loads(response.data)
        
        assert 'message' in data
        assert 'version' in data
        assert 'timestamp' in data
        assert data['message'] == 'Welcome to Flask Practice Application'
    
    def test_index_content_type(self, client):
        """Test index route returns JSON content type"""
        response = client.get('/')
        assert response.content_type == 'application/json'


class TestHealthRoute:
    """Tests for the health check route"""
    
    def test_health_status_code(self, client):
        """Test health check returns 200 status code"""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_response_structure(self, client):
        """Test health check response structure"""
        response = client.get('/health')
        data = json.loads(response.data)
        
        assert data['status'] == 'healthy'
        assert data['service'] == 'flask_practice'
        assert 'timestamp' in data
    
    def test_health_json_format(self, client):
        """Test health check returns valid JSON"""
        response = client.get('/health')
        try:
            json.loads(response.data)
            assert True
        except json.JSONDecodeError:
            pytest.fail("Response is not valid JSON")


class TestGetUsersRoute:
    """Tests for GET /api/users route"""
    
    def test_get_users_status_code(self, client):
        """Test get users returns 200 status code"""
        response = client.get('/api/users')
        assert response.status_code == 200
    
    def test_get_users_returns_list(self, client):
        """Test get users returns a list"""
        response = client.get('/api/users')
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        assert len(data) == 2
    
    def test_get_users_content_format(self, client):
        """Test get users returns users with correct structure"""
        response = client.get('/api/users')
        data = json.loads(response.data)
        
        for user in data:
            assert 'id' in user
            assert 'name' in user
            assert 'email' in user


class TestCreateUserRoute:
    """Tests for POST /api/users route"""
    
    def test_create_user_success(self, client):
        """Test successful user creation"""
        new_user = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test User'
        assert data['email'] == 'test@example.com'
    
    def test_create_user_missing_fields(self, client):
        """Test user creation with missing required fields"""
        incomplete_user = {
            'name': 'Test User'
        }
        
        response = client.post(
            '/api/users',
            data=json.dumps(incomplete_user),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_user_empty_body(self, client):
        """Test user creation with empty body"""
        response = client.post(
            '/api/users',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_create_user_no_json(self, client):
        """Test user creation with no JSON data"""
        response = client.post(
            '/api/users',
            data='',
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestGetUserByIdRoute:
    """Tests for GET /api/users/<id> route"""
    
    def test_get_existing_user(self, client):
        """Test get existing user returns 200"""
        response = client.get('/api/users/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 1
        assert 'name' in data
        assert 'email' in data
    
    def test_get_nonexistent_user(self, client):
        """Test get non-existent user returns 404"""
        response = client.get('/api/users/999')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_user_second_id(self, client):
        """Test get user with id 2"""
        response = client.get('/api/users/2')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['id'] == 2


class TestUpdateUserRoute:
    """Tests for PUT /api/users/<id> route"""
    
    def test_update_user_success(self, client):
        """Test successful user update"""
        update_data = {
            'name': 'Updated Name',
            'email': 'updated@example.com'
        }
        
        response = client.put(
            '/api/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
        assert data['email'] == 'updated@example.com'
    
    def test_update_nonexistent_user(self, client):
        """Test update non-existent user returns 404"""
        update_data = {
            'name': 'Updated Name'
        }
        
        response = client.put(
            '/api/users/999',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
    
    def test_update_user_partial(self, client):
        """Test partial user update"""
        update_data = {
            'name': 'New Name'
        }
        
        response = client.put(
            '/api/users/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'New Name'


class TestDeleteUserRoute:
    """Tests for DELETE /api/users/<id> route"""
    
    def test_delete_user_success(self, client):
        """Test successful user deletion"""
        response = client.delete('/api/users/1')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'message' in data
    
    def test_delete_nonexistent_user(self, client):
        """Test delete non-existent user returns 404"""
        response = client.delete('/api/users/999')
        assert response.status_code == 404
    
    def test_delete_second_user(self, client):
        """Test delete user with id 2"""
        response = client.delete('/api/users/2')
        assert response.status_code == 200


class TestEchoRoute:
    """Tests for POST /api/echo route"""
    
    def test_echo_simple_data(self, client):
        """Test echo endpoint with simple data"""
        echo_data = {
            'message': 'hello',
            'number': 42
        }
        
        response = client.post(
            '/api/echo',
            data=json.dumps(echo_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['echo'] == echo_data
    
    def test_echo_complex_data(self, client):
        """Test echo endpoint with complex nested data"""
        echo_data = {
            'user': {
                'name': 'John',
                'age': 30
            },
            'tags': ['python', 'flask']
        }
        
        response = client.post(
            '/api/echo',
            data=json.dumps(echo_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200


class TestCalculateRoute:
    """Tests for POST /api/calculate route"""
    
    def test_calculate_success(self, client):
        """Test calculate endpoint with valid data"""
        calc_data = {
            'a': 10,
            'b': 5
        }
        
        response = client.post(
            '/api/calculate',
            data=json.dumps(calc_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['addition'] == 15
        assert data['subtraction'] == 5
        assert data['multiplication'] == 50
        assert data['division'] == 2
    
    def test_calculate_division_by_zero(self, client):
        """Test calculate with division by zero"""
        calc_data = {
            'a': 10,
            'b': 0
        }
        
        response = client.post(
            '/api/calculate',
            data=json.dumps(calc_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['division'] is None
    
    def test_calculate_missing_fields(self, client):
        """Test calculate with missing fields"""
        calc_data = {
            'a': 10
        }
        
        response = client.post(
            '/api/calculate',
            data=json.dumps(calc_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_calculate_invalid_values(self, client):
        """Test calculate with invalid values"""
        calc_data = {
            'a': 'not a number',
            'b': 5
        }
        
        response = client.post(
            '/api/calculate',
            data=json.dumps(calc_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_calculate_float_values(self, client):
        """Test calculate with float values"""
        calc_data = {
            'a': 10.5,
            'b': 2.5
        }
        
        response = client.post(
            '/api/calculate',
            data=json.dumps(calc_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['addition'] == 13.0
        assert data['division'] == 4.2


class TestErrorHandling:
    """Tests for error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
        
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_method_not_allowed(self, client):
        """Test method not allowed error"""
        response = client.delete('/')
        assert response.status_code in [404, 405]


class TestContentTypes:
    """Tests for content type handling"""
    
    def test_json_content_type_in_responses(self, client):
        """Test all endpoints return JSON content type"""
        endpoints = [
            ('/', 'GET'),
            ('/health', 'GET'),
            ('/api/users', 'GET'),
        ]
        
        for endpoint, method in endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            assert response.content_type == 'application/json'
