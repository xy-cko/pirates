import pytest
from unittest.mock import patch
from app import app

# --- Fixtures ---

@pytest.fixture
def client():
    """Sets up a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_translator():
    """Mocks the translator to avoid hitting external APIs during tests."""
    with patch('app.translator.to_mongolian') as mock_mn, \
         patch('app.translator.to_japanese') as mock_ja:
        mock_mn.return_value = "Mocked Mongolian"
        mock_ja.return_value = "Mocked Japanese"
        yield mock_mn, mock_ja

# --- Test Cases ---

# 1. Happy Path: Subject is "I"
def test_translate_i_subject(client, mock_translator):
    """Test that 'I' becomes 'Pirate King' and verbs conjugate properly."""
    response = client.post('/', json={
        "sentence": "I am eating an apple.",
        "magic_number": 4  # Divisors of 4: 1, 2, 4 (Count = 3)
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["english_sentence"] == "Pirate King is eating an apple."
    assert data["mongolian_sentence"] == "Mocked Mongolian"
    assert data["japanese_sentence"] == "Mocked Japanese"

# 2. Happy Path: Subject is a normal noun
def test_translate_normal_subject(client, mock_translator):
    """Test that a standard subject is replaced by the pirate count."""
    response = client.post('/', json={
        "sentence": "The dog barks loudly.",
        "magic_number": 7
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["english_sentence"] == "The 2 Pirates bark loudly."

# 3. Error Case: Missing required JSON keys
def test_missing_required_keys(client):
    """Test the application's response to an incomplete JSON payload."""
    response = client.post('/', json={
        "sentence": "I am here."
    })
    
    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid request"

# 4. Error Case: Invalid magic_number type
def test_invalid_magic_number_type(client):
    """Test validation when magic_number is not an integer."""
    response = client.post('/', json={
        "sentence": "I am here.",
        "magic_number": "seven"
    })
    
    assert response.status_code == 400
    assert response.get_json()["error"] == "Where is magic?"

# 5. Error Case: No subject in sentence
def test_no_subject_found(client):
    """Test behavior when the modifier cannot identify a subject."""
    response = client.post('/', json={
        "sentence": "Hello!",
        "magic_number": 2
    })
    
    assert response.status_code == 400
    assert response.get_json()["error"] == "Where am I?"

# 6. Edge Case: Zero as a magic number
def test_zero_magic_number(client, mock_translator):
    """Test divisor logic edge case where magic_number is 0."""
    response = client.post('/', json={
        "sentence": "He runs fast.",
        "magic_number": 0 
    })
    
    assert response.status_code == 200
    data = response.get_json()
    
    assert data["english_sentence"] == "0 Pirates run fast."