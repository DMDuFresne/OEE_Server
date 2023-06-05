from flask import jsonify
from app.models.oee import OeeModel


def calculate_oee(data):

    try:

        oee_model = OeeModel(**data)
        availability = oee_model.calculate_availability()
        performance = oee_model.calculate_performance()
        quality = oee_model.calculate_quality()
        oee = oee_model.calculate_oee()
        return {"availability": availability, "performance": performance, "quality": quality, "oee": oee}

    except ValueError as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 400

    except Exception as e:

        print(f"Error calculating OEE: {e}")
        return jsonify({'error': f'Error calculating OEE: {e}'}), 500

