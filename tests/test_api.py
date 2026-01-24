"""Tests for Flask API endpoints."""

import pytest
import json
from app.app import create_app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for the /health endpoint."""

    def test_health_returns_200(self, client):
        """Test that health endpoint returns 200 OK."""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_returns_json(self, client):
        """Test that health endpoint returns JSON."""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data == {"status": "healthy"}


class TestConjugateEndpoint:
    """Tests for the /conjugate endpoint."""

    def test_conjugate_requires_post(self, client):
        """Test that GET requests are not allowed."""
        response = client.get('/conjugate')
        assert response.status_code == 405

    def test_conjugate_requires_json(self, client):
        """Test that non-JSON requests return 400."""
        response = client.post('/conjugate', data='not json')
        assert response.status_code == 400

    def test_conjugate_requires_verb_field(self, client):
        """Test that missing 'verb' field returns 400."""
        response = client.post(
            '/conjugate',
            data=json.dumps({}),
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'verb' in data['error'].lower()

    def test_conjugate_rejects_empty_verb(self, client):
        """Test that empty verb string returns 400."""
        response = client.post(
            '/conjugate',
            data=json.dumps({"verb": ""}),
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_conjugate_rejects_non_string_verb(self, client):
        """Test that non-string verb returns 400."""
        response = client.post(
            '/conjugate',
            data=json.dumps({"verb": 123}),
            content_type='application/json'
        )
        assert response.status_code == 400

    @pytest.mark.slow
    def test_conjugate_valid_verb_returns_200(self, client):
        """Test that valid verb returns 200 with proper structure."""
        response = client.post(
            '/conjugate',
            data=json.dumps({"verb": "to be"}),
            content_type='application/json'
        )
        assert response.status_code == 200

    @pytest.mark.slow
    def test_conjugate_response_structure(self, client):
        """Test that response has required fields."""
        response = client.post(
            '/conjugate',
            data=json.dumps({"verb": "to be"}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        # Check required fields
        assert 'english' in data
        assert 'greek' in data
        assert 'conjugations' in data
        assert 'confidence' in data
        assert 'notes' in data

        # Check types
        assert isinstance(data['english'], str)
        assert isinstance(data['greek'], str)
        assert isinstance(data['conjugations'], list)
        assert isinstance(data['confidence'], (int, float))
        assert isinstance(data['notes'], str)

        # Check conjugations structure
        assert len(data['conjugations']) == 6
        for conj in data['conjugations']:
            assert 'pronoun' in conj
            assert 'form' in conj
            assert isinstance(conj['pronoun'], str)
            assert isinstance(conj['form'], str)

    @pytest.mark.slow
    def test_conjugate_confidence_range(self, client):
        """Test that confidence is between 0 and 1."""
        response = client.post(
            '/conjugate',
            data=json.dumps({"verb": "to be"}),
            content_type='application/json'
        )
        data = json.loads(response.data)
        assert 0.0 <= data['confidence'] <= 1.0
