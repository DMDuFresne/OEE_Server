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

        # Return the calculated values as a dictionary
        return {
            "availability": availability,
            "performance": performance,
            "quality": quality,
            "oee": oee,
            "availabilityString": f'{availability*100:.0f}%',
            "performanceString": f'{performance*100:.0f}%',
            "qualityString": f'{quality*100:.0f}%',
            "oeeString": f'{oee*100:.0f}%',
            "timestamp": timestamp,
        }

    except ValueError as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 400

    except Exception as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 500

