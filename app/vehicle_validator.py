from data_model import Vehicle


class ValidationError(Exception):
    def __init__(self, errors, status_code=422):
        self.errors = errors
        self.status_code = status_code
        super().__init__(str(errors))


def validate_vehicle_body(body, is_update=False, current_vin=None):
    errors = {}
    
    if not is_update:  # for POST
        required_fields = [
            "vin", "manufacturer_name", "description",
            "horse_power", "model_name", "model_year",
            "purchase_price", "fuel_type"
        ]

        for field in required_fields:
            if field not in body or body[field] is None:
                errors.setdefault(field, []).append(f"{field} is required")

    # Validate VIN
    if "vin" in body:
        vin = body["vin"]

        if not isinstance(vin, str):
            errors.setdefault("vin", []).append("VIN must be a string")
        elif not vin.strip():
            errors.setdefault("vin", []).append("VIN cannot be empty")
        else:
            # Uniqueness check (POST only, or PUT if VIN is changing)
            if not is_update or (current_vin and vin.upper() != current_vin.upper()):
                existing = Vehicle.query.get(vin.upper())
                if existing:
                    errors.setdefault("vin", []).append("VIN already exists")

    # Validate manufacturer_name
    if "manufacturer_name" in body and body["manufacturer_name"] is not None:
        if not isinstance(body["manufacturer_name"], str):
            errors.setdefault("manufacturer_name", []).append("manufacturer_name must be a string")
        elif not body["manufacturer_name"].strip():
            errors.setdefault("manufacturer_name", []).append("manufacturer_name cannot be empty")

    # Validate description
    if "description" in body and body["description"] is not None:
        if not isinstance(body["description"], str):
            errors.setdefault("description", []).append("description must be a string")
        elif not body["description"].strip():
            errors.setdefault("description", []).append("description cannot be empty")

    # Validate horse_power
    if "horse_power" in body and body["horse_power"] is not None:
        if not isinstance(body["horse_power"], int):
            errors.setdefault("horse_power", []).append("horse_power must be an integer")
        elif body["horse_power"] <= 0:
            errors.setdefault("horse_power", []).append("horse_power must be positive")

    # Validate model_name
    if "model_name" in body and body["model_name"] is not None:
        if not isinstance(body["model_name"], str):
            errors.setdefault("model_name", []).append("model_name must be a string")
        elif not body["model_name"].strip():
            errors.setdefault("model_name", []).append("model_name cannot be empty")

    # Validate model_year
    if "model_year" in body and body["model_year"] is not None:
        if not isinstance(body["model_year"], int):
            errors.setdefault("model_year", []).append("model_year must be an integer")
        elif body["model_year"] < 1886 or body["model_year"] > 2026:
            errors.setdefault("model_year", []).append("model_year must be between 1886 and 2026")

    # Validate purchase_price
    if "purchase_price" in body and body["purchase_price"] is not None:
        if not isinstance(body["purchase_price"], (int, float)):
            errors.setdefault("purchase_price", []).append("purchase_price must be a number")
        elif body["purchase_price"] < 0:
            errors.setdefault("purchase_price", []).append("purchase_price cannot be negative")

    # Validate fuel_type
    if "fuel_type" in body and body["fuel_type"] is not None:
        valid_fuel_types = ["gasoline", "diesel", "electric", "hybrid", "hydrogen", "other"]
        if not isinstance(body["fuel_type"], str):
            errors.setdefault("fuel_type", []).append("fuel_type must be a string")
        elif not body["fuel_type"].strip():
            errors.setdefault("fuel_type", []).append("fuel_type cannot be empty")
        elif body["fuel_type"].lower() not in valid_fuel_types:
            errors.setdefault("fuel_type", []).append(
                f"fuel_type must be one of: {', '.join(valid_fuel_types)}"
            )

    # For PUT: if a field is provided but null, reject it
    if is_update:
        for field, value in body.items():
            if field != "vin" and value is None:  # Allow VIN to remain unchanged
                errors.setdefault(field, []).append(f"{field} cannot be null")

    # Raise 422 error if validation failed
    if errors:
        raise ValidationError(errors, 422)
    
    # Normalize data
    normalized = body.copy()
    if "vin" in normalized:
        normalized["vin"] = normalized["vin"].upper().strip()
    if "manufacturer_name" in normalized and normalized["manufacturer_name"]:
        normalized["manufacturer_name"] = normalized["manufacturer_name"].strip()
    if "model_name" in normalized and normalized["model_name"]:
        normalized["model_name"] = normalized["model_name"].strip()
    if "description" in normalized and normalized["description"]:
        normalized["description"] = normalized["description"].strip()
    if "fuel_type" in normalized and normalized["fuel_type"]:
        normalized["fuel_type"] = normalized["fuel_type"].lower().strip()

    return normalized