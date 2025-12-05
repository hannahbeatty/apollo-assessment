
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import os
import pytest
from app import create_app
from app.database import db

@pytest.fixture
def test_app(tmp_path):
    # temporary test database
    test_db = tmp_path / "test.db"
    os.environ["TEST_DATABASE_PATH"] = str(test_db)

    # create the app with test config
    app = create_app(testing=True)

    # override DB URI for tests
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{test_db}"
    app.config["TESTING"] = True

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()


# tests!

def test_get_all_vehicles_empty(client):
    """Test getting all vehicles when database is empty"""
    response = client.get('/vehicle')
    assert response.status_code == 200
    assert response.json == []


def test_create_vehicle_success(client):
    """Test creating a valid vehicle"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 201
    
    data = response.json
    assert data["vin"] == "1HGBH41JXMN109186"
    assert data["manufacturer_name"] == "Honda"
    assert data["horse_power"] == 200


def test_create_vehicle_missing_field(client):
    """Test creating a vehicle with missing required field"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        # missing description
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 422
    assert "description" in response.json["errors"]


def test_create_vehicle_duplicate_vin(client):
    """Test creating a vehicle with duplicate VIN"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    # Create first vehicle
    client.post('/vehicle', json=vehicle_data)
    
    # Try to create duplicate
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 422
    assert "vin" in response.json["errors"]


def test_create_vehicle_invalid_fuel_type(client):
    """Test creating a vehicle with invalid fuel type"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "nuclear"  # invalid
    }
    
    response = client.post('/vehicle', json=vehicle_data)
    assert response.status_code == 422
    assert "fuel_type" in response.json["errors"]


def test_get_vehicle_by_vin(client):
    """Test getting a specific vehicle by VIN"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    # Create vehicle
    client.post('/vehicle', json=vehicle_data)
    
    # Get vehicle
    response = client.get('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 200
    assert response.json["vin"] == "1HGBH41JXMN109186"


def test_get_vehicle_not_found(client):
    """Test getting a vehicle that doesn't exist"""
    response = client.get('/vehicle/DOESNOTEXIST123')
    assert response.status_code == 404


def test_update_vehicle(client):
    """Test updating a vehicle"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    # Create vehicle
    client.post('/vehicle', json=vehicle_data)
    
    # Update vehicle
    update_data = {
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horse_power": 250,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    response = client.put('/vehicle/1HGBH41JXMN109186', json=update_data)
    assert response.status_code == 200
    assert response.json["description"] == "Updated description"
    assert response.json["horse_power"] == 250


def test_update_vehicle_not_found(client):
    """Test updating a vehicle that doesn't exist"""
    update_data = {
        "manufacturer_name": "Honda",
        "description": "Updated description",
        "horse_power": 250,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    response = client.put('/vehicle/DOESNOTEXIST123', json=update_data)
    assert response.status_code == 404


def test_delete_vehicle(client):
    """Test deleting a vehicle"""
    vehicle_data = {
        "vin": "1HGBH41JXMN109186",
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    # Create vehicle
    client.post('/vehicle', json=vehicle_data)
    
    # Delete vehicle
    response = client.delete('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 204
    
    # Verify it's deleted
    response = client.get('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 404


def test_delete_vehicle_not_found(client):
    """Test deleting a vehicle that doesn't exist"""
    response = client.delete('/vehicle/DOESNOTEXIST123')
    assert response.status_code == 404


def test_vin_case_insensitive(client):
    """Test that VIN is case insensitive"""
    vehicle_data = {
        "vin": "1hgbh41jxmn109186",  # lowercase
        "manufacturer_name": "Honda",
        "description": "A reliable sedan",
        "horse_power": 200,
        "model_name": "Accord",
        "model_year": 2020,
        "purchase_price": 25000.00,
        "fuel_type": "gasoline"
    }
    
    client.post('/vehicle', json=vehicle_data)
    
    # Try to get with uppercase
    response = client.get('/vehicle/1HGBH41JXMN109186')
    assert response.status_code == 200
    assert response.json["vin"] == "1HGBH41JXMN109186"  # should be uppercase in response