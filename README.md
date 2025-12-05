# Vehicle Management API

A RESTful API for managing vehicle inventory built with Flask and SQLAlchemy.


## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. **Clone the repository**
```bash
   git clone <repository-url>
   cd apollo-assessment
```

2. **Create a virtual environment**
```bash
   python -m venv venv
```

3. **Activate the virtual environment**
   - Windows:
```bash
     venv\Scripts\activate
```
   - macOS/Linux:
```bash
     source venv/bin/activate
```

4. **Install dependencies**
```bash
   pip install -r requirements.txt
```


## Running the Application

Start the Flask development server:
```bash
python run.py
```

The API will be available at `http://127.0.0.1:5000`

## API Endpoints

### Get All Vehicles
```http
GET /vehicle
```

**Response:** `200 OK`
```json
[
  {
    "vin": "1HGBH41JXMN109186",
    "manufacturer_name": "Honda",
    "description": "A reliable sedan",
    "horse_power": 200,
    "model_name": "Accord",
    "model_year": 2020,
    "purchase_price": 25000.0,
    "fuel_type": "gasoline"
  }
]
```

### Get Vehicle by VIN
```http
GET /vehicle/<vin>
```

**Response:** `200 OK` or `404 Not Found`

### Create Vehicle
```http
POST /vehicle
Content-Type: application/json
```

**Request Body:**
```json
{
  "vin": "1HGBH41JXMN109186",
  "manufacturer_name": "Honda",
  "description": "A reliable sedan",
  "horse_power": 200,
  "model_name": "Accord",
  "model_year": 2020,
  "purchase_price": 25000.00,
  "fuel_type": "gasoline"
}
```

**Response:** `201 Created` or `422 Unprocessable Entity`

### Update Vehicle
```http
PUT /vehicle/<vin>
Content-Type: application/json
```

**Request Body:** (all fields optional except those being updated)
```json
{
  "manufacturer_name": "Honda",
  "description": "Updated description",
  "horse_power": 250,
  "model_name": "Accord",
  "model_year": 2021,
  "purchase_price": 28000.00,
  "fuel_type": "hybrid"
}
```

**Response:** `200 OK`, `404 Not Found`, or `422 Unprocessable Entity`

### Delete Vehicle
```http
DELETE /vehicle/<vin>
```

**Response:** `204 No Content` or `404 Not Found`

## Validation Rules

### Required Fields (POST only)
- `vin` - String, unique, case-insensitive
- `manufacturer_name` - Non-empty string
- `description` - Non-empty string
- `horse_power` - Positive integer
- `model_name` - Non-empty string
- `model_year` - Integer between 1886 and 2026
- `purchase_price` - Non-negative number
- `fuel_type` - One of: `gasoline`, `diesel`, `electric`, `hybrid`, `hydrogen`, `other`

### Field Constraints
- **VIN**: Must be unique, automatically converted to uppercase
- **horse_power**: Must be a positive integer
- **model_year**: Must be between 1886 (first automobile) and 2026
- **purchase_price**: Cannot be negative
- **fuel_type**: Case-insensitive, must be a valid fuel type

## Running Tests

Run the test suite with pytest:
```bash
pytest tests/tests.py
```

For verbose output:
```bash
pytest tests/tests.py -v
```



### Test Coverage

The test suite includes:
- Getting all vehicles (empty database)
- Creating a valid vehicle
- Creating a vehicle with missing fields
- Creating a vehicle with duplicate VIN
- Creating a vehicle with invalid fuel type
- Getting a vehicle by VIN
- Getting a non-existent vehicle
- Updating a vehicle
- Updating a non-existent vehicle
- Deleting a vehicle
- Deleting a non-existent vehicle
- VIN case insensitivity

## Example Usage

### Using cURL

**Create a vehicle:**
```bash
curl -X POST http://127.0.0.1:5000/vehicle \
  -H "Content-Type: application/json" \
  -d '{
    "vin": "1HGBH41JXMN109186",
    "manufacturer_name": "Honda",
    "description": "A reliable sedan",
    "horse_power": 200,
    "model_name": "Accord",
    "model_year": 2020,
    "purchase_price": 25000.00,
    "fuel_type": "gasoline"
  }'
```

**Get all vehicles:**
```bash
curl http://127.0.0.1:5000/vehicle
```

**Get a specific vehicle:**
```bash
curl http://127.0.0.1:5000/vehicle/1HGBH41JXMN109186
```

**Update a vehicle:**
```bash
curl -X PUT http://127.0.0.1:5000/vehicle/1HGBH41JXMN109186 \
  -H "Content-Type: application/json" \
  -d '{
    "manufacturer_name": "Honda",
    "description": "Updated description",
    "horse_power": 250,
    "model_name": "Accord",
    "model_year": 2020,
    "purchase_price": 25000.00,
    "fuel_type": "gasoline"
  }'
```

**Delete a vehicle:**
```bash
curl -X DELETE http://127.0.0.1:5000/vehicle/1HGBH41JXMN109186
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid JSON"
}
```

### 404 Not Found
```json
{
  "error": "Vehicle not found"
}
```

### 422 Unprocessable Entity
```json
{
  "errors": {
    "vin": ["VIN already exists"],
    "horse_power": ["horse_power must be positive"]
  }
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

## Technologies Used

- **Flask** - Web framework
- **SQLAlchemy** - ORM for database operations
- **SQLite** - Lightweight database
- **pytest** - Testing framework
- **pytest-flask** - Flask testing utilities

## Development Notes

- VINs are automatically made uppercase for consistency
- The database uses SQLite with an in-memory database for testing, EASY to change
- All string fields are trimmed of whitespace during validation
- Fuel types are normalized to lowercase
- The API follows RESTful conventions

## License

add mit if they let me

## Author

Hannah Beatty