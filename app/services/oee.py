# Import the necessary modules
from flask import jsonify
from app.models.oee import OeeModel


def calculate_oee(data):

    try:

        # Create an instance of OeeModel using the provided data
        oee_model = OeeModel(**data)

        # Calculate availability, performance, quality, and overall OEE
        availability = oee_model.calculate_availability()
        performance = oee_model.calculate_performance()
        quality = oee_model.calculate_quality()
        oee = oee_model.calculate_oee()

        # Return the calculated values as a dictionary
        return {"availability": availability, "performance": performance, "quality": quality, "oee": oee}

    except ValueError as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 400

    except Exception as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 500

