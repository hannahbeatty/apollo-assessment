from flask import Blueprint, request, jsonify
from app.database import db
from app.data_model import Vehicle
from app.vehicle_validator import validate_vehicle_body, ValidationError
from sqlalchemy.exc import IntegrityError


vehicle_bp = Blueprint('vehicles', __name__)


# GET all vehicles
@vehicle_bp.route('/vehicle', methods=['GET'])
def get_all_vehicles():
    """Return json format of all vehicles in database"""
    vehicles = Vehicle.query.all()
    return jsonify([v.to_dict() for v in vehicles]), 200


# POST new vehicle
@vehicle_bp.route('/vehicle', methods=['POST'])
def create_vehicle():
    """Add new vehicle to database, unique VIN"""
    body = request.get_json()
    
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
    
    try:
        # validate body (includes uniqueness check)
        validated = validate_vehicle_body(body)
        
        # create the object in db
        vehicle = Vehicle(**validated)
        db.session.add(vehicle)
        db.session.commit()
        
        return jsonify(vehicle.to_dict()), 201
        
    except ValidationError as e:
        return jsonify({"errors": e.errors}), 422
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# GET vehicle by VIN
@vehicle_bp.route('/vehicle/<vin>', methods=['GET'])
def get_vehicle(vin):
    """Return JSON for existing vehicle in database"""
    vehicle = db.session.get(Vehicle, vin.upper())
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    return jsonify(vehicle.to_dict()), 200


# PUT (update vehicle by VIN)
@vehicle_bp.route('/vehicle/<vin>', methods=['PUT'])
def update_vehicle(vin):
    """Update info for an existing vehicle"""
    body = request.get_json()
    
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400
    
    try:
        vehicle = db.session.get(Vehicle, vin.upper())
        
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        
        # validate body
        validated = validate_vehicle_body(body, is_update=True, current_vin=vin)
        
        # update vehicle (excluding VIN since it's the primary key)
        update_data = {k: v for k, v in validated.items() if k != 'vin'}
        for key, value in update_data.items():
            if hasattr(vehicle, key):
                setattr(vehicle, key, value)
        
        db.session.commit()
        return jsonify(vehicle.to_dict()), 200
        
    except ValidationError as e:
        return jsonify({"errors": e.errors}), 422
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Database integrity error"}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500


# DELETE vehicle by VIN
@vehicle_bp.route('/vehicle/<vin>', methods=['DELETE'])
def delete_vehicle(vin):
    """Remove an existing vehicle"""
    vehicle = db.session.get(Vehicle, vin.upper())
    
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    
    db.session.delete(vehicle)
    db.session.commit()
    
    return '', 204