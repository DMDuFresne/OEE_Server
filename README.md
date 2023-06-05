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
