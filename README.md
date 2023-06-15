# OEE Calculation Application

This is a Flask-based application for calculating Overall Equipment Effectiveness (OEE) of a manufacturing process. It provides a RESTful API endpoint for performing OEE calculations based on the provided data.

## Features

- Calculates Availability, Performance, Quality, and Overall OEE based on input parameters.
- Handles missing or invalid input data gracefully, returning appropriate error messages.
- Uses a modular structure with a blueprint, model, and service for separation of concerns.

## Prerequisites

- Python 3.x
- Flask

## Installation

1. Clone the repository:
git clone https://github.com/your-username/oee-calculation-app.git
2. Change into the project directory:
cd oee-calculation-app
3. Create and activate a virtual environment (optional but recommended):
python3 -m venv venv source venv/bin/activate
4. Install the required dependencies:
pip install -r requirements.txt
## Usage

1. Set the Flask application environment variable:
export FLASK_APP=app.py
2. Run the application:
flask run
3. The application will start running at `http://localhost:5000`. You can use a tool like cURL or Postman to make HTTP POST requests to the `/oee/calculate` endpoint with the required input parameters in JSON format. For example:
curl -X POST -H "Content-Type: application/json" -d '{"good_count": 100, "total_count": 120, "run_time": 3600, "total_time": 4320, "target_count": 110}' http://localhost:5000/oee/calculate


# OEE API Documentation

This server is designed to handle assets and OEE calculations. It contains various routes for handling different types of assets and for performing OEE calculations.

## Models

### AssetModel

This model is used to represent an asset. It has the following attributes:

- `id`: An integer representing the unique identifier of the asset.
- `name`: A string representing the name of the asset.
- `description`: A string providing a description of the asset.
- `parent_id`: An integer representing the unique identifier of the parent asset.
- `object_type`: A string representing the type of the asset.

## Routes

### Asset Routes

- `GET /asset/all`: This route returns the entire asset tree. It does not require any parameters.

For each asset class (`EnterpriseModel`, `SiteModel`, `AreaModel`, `LineModel`, `CellModel`), there are the following routes:

- `POST /{asset_class}/create`: This route creates a new asset of the specified class. It requires a JSON body with the following parameters: 
  - `name`: The name of the asset.
  - `description`: The description of the asset.
  - `parent_id`: The ID of the parent asset.
  - `object_type`: The type of the asset.

- `GET /{asset_class}/all`: This route returns all assets of the specified class. It does not require any parameters.

- `GET /{asset_class}/{asset_id}`: This route returns the asset of the specified class with the given ID. It does not require any parameters.

- `PUT /{asset_class}/{asset_id}`: This route updates the asset of the specified class with the given ID. It requires a JSON body with the following parameters:
  - `name`: The new name of the asset.
  - `description`: The new description of the asset.
  - `parent_id`: The new parent ID of the asset.
  - `object_type`: The new type of the asset.

- `DELETE /{asset_class}/{asset_id}`: This route deletes the asset of the specified class with the given ID. It does not require any parameters.

### OEE Routes

- `POST /oee/calculate`: This route calculates OEE (Overall Equipment Efficiency). It requires a JSON body with the following parameters:
  - `total_count`: The total count of items.
  - `good_count`: The count of good items.
  - `ideal_run_rate`: The ideal run rate of the process.
  - `run_time`: The running time of the process.

- `POST /oee/calculate/store`: This route calculates OEE and stores the result. It requires a JSON body with the following parameters:
  - `total_count`: The total count of items.
  - `good_count`: The count of good items.
  - `ideal_run_rate`: The ideal run rate of the process.
  - `run_time`: The running time of the process.
  - `object_type`: The type of the object for which OEE is calculated.
  - `object_id`: The ID of the object for which OEE is calculated.

- `GET /oee/{object_type}/{object_id}`: This route retrieves the latest OEE data for the given object. It does not require any parameters.

- `GET /oee/history/{object_type}/{object_id}`: This route retrieves the OEE data for the given object within a specified date range. It requires query parameters `start_date` and `end_date`, which specify the start and end dates of the range, respectively.