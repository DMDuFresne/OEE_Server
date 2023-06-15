# Import the necessary modules
from flask import jsonify
from datetime import datetime
from app.models.oee import OeeModel

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"


def calculate_oee(data):

    try:

        # Create an instance of OeeModel using the provided data
        oee_model = OeeModel(**data)

        # Calculate availability, performance, quality, and overall OEE
        availability = oee_model.calculate_availability()
        performance = oee_model.calculate_performance()
        quality = oee_model.calculate_quality()
        oee = oee_model.calculate_oee()
        timestamp = datetime.now().strftime(DATETIME_FORMAT)

        # Add the new values to the existing data dictionary
        data["availability"] = availability
        data["performance"] = performance
        data["quality"] = quality
        data["oee"] = oee
        data["timestamp"] = timestamp

        # Return the updated data dictionary
        return data

    except ValueError as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 400

    except Exception as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 500
