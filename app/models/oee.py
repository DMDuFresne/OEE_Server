# Define the OeeModel class
class OeeModel:
    def __init__(self, **kwargs):

        # Define the required arguments for OeeModel initialization
        required_arguments = ['good_count', 'total_count', 'run_time', 'total_time', 'target_count']

        # Check for missing required arguments
        missing_arguments = set(required_arguments) - set(kwargs)
        if missing_arguments:
            raise ValueError("Missing required keyword arguments: {}".format(", ".join(missing_arguments)))

        try:

            # Convert and assign the provided values to instance variables
            self.good_count = float(kwargs['good_count'])
            self.total_count = float(kwargs['total_count'])
            self.run_time = float(kwargs['run_time'])
            self.total_time = float(kwargs['total_time'])
            self.target_count = float(kwargs['target_count'])

        except KeyError as ke:
            raise ValueError("Missing required keyword argument: '{}'".format(ke))

        except TypeError as te:
            raise ValueError("Error initializing OeeModel: " + str(te))

    def calculate_quality(self):

        # Check if good_count and total_count are numbers
        if not isinstance(self.good_count, (int, float)) or not isinstance(self.total_count, (int, float)):
            raise ValueError("Both good_count and total_count must be numbers.")

        # Check if total_count is not zero
        if self.total_count == 0:
            raise ValueError("total_count cannot be zero.")

        # Calculate and return the quality aspect of OEE
        return self.good_count / self.total_count

    def calculate_availability(self):

        # Check if run_time and total_time are numbers
        if not isinstance(self.run_time, (int, float)) or not isinstance(self.total_time, (int, float)):
            raise ValueError("Both run_time and total_time must be numbers.")

        # Check if total_time is not zero
        if self.total_time == 0:
            raise ValueError("total_time cannot be zero.")

        # Calculate and return the availability aspect of OEE
        return self.run_time / self.total_time

    def calculate_performance(self):

        # Check if total_count and target_count are numbers
        if not isinstance(self.total_count, (int, float)) or not isinstance(self.target_count, (int, float)):
            raise ValueError("Both total_count and target_count must be numbers.")

        # Check if target_count is not zero
        if self.target_count == 0:
            raise ValueError("target_count cannot be zero.")

        # Calculate and return the performance aspect of OEE
        return self.total_count / self.target_count

    def calculate_oee(self):

        try:

            # Calculate the quality, availability, and performance aspects of OEE
            quality = self.calculate_quality()
            availability = self.calculate_availability()
            performance = self.calculate_performance()

            # Calculate and return the overall OEE
            return quality * availability * performance

        except ValueError as ve:
            raise ValueError("Error calculating OEE: " + str(ve))

        except Exception as e:
            raise Exception("Unexpected error calculating OEE: " + str(e))

