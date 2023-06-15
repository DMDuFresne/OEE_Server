import logging
from datetime import datetime
from app.models.oee import OeeModel

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f%z"

# Create a logger
logger = logging.getLogger(__name__)


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
        logger.error(f"Error calculating OEE: {e}")
        raise ValueError("Error calculating OEE")
    except Exception as e:
        logger.error(f"Error calculating OEE: {e}")
        raise Exception("Error calculating OEE")


def get_latest_oee(object_type, object_id):
    try:
        return OeeModel.get_latest_oee(object_type, object_id)
    except Exception as e:
        logger.error(f"Failed to fetch latest OEE data: {e}")
        raise Exception("An error occurred while fetching latest OEE data.")


def get_oee_by_date_range(object_type, object_id, start_date, end_date):
    try:
        # Call the get_oee_by_date_range method from the OeeModel class
        oee_data = OeeModel.get_oee_by_date_range(object_type, object_id, start_date, end_date)
        return oee_data

    except Exception as e:
        logger.error(f"Failed to fetch OEE data: {e}")
        raise Exception("An error occurred while fetching OEE data.")
