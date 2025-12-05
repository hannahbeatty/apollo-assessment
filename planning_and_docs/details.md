## Project Structure Overview

app/
│
├── __init__.py          # make into module for pytests
├── api.py               # Routes and HTTP method handlers
├── config.py            # coclasses (production, testing)
├── data_model.py        # SQLAlchemy Vehicle model
├── database.py          # SQLAlchemy database instance
└── vehicle_validator.py # Centralized validation logic

run.py                   # Entry point for local development
tests.py                 # Complete pytest suite
instance/                # Automatically created SQLite database



## Database Schema

| Column            | Type     | Constraints                     |
|-------------------|----------|----------------------------------|
| vin               | String   | Primary key, uppercase           |
| manufacturer_name | String   | Required                         |
| description       | String   | Required                         |
| horse_power       | Integer  | Required, > 0                    |
| model_name        | String   | Required                         |
| model_year        | Integer  | 1886–2026                        |
| purchase_price    | Numeric  | >= 0                             |
| fuel_type         | String   | One of allowed types             |


