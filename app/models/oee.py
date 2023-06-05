class OeeModel:
    def __init__(self, **kwargs):

        required_arguments = ['good_count', 'total_count', 'run_time', 'total_time', 'target_count']
        missing_arguments = set(required_arguments) - set(kwargs)
        if missing_arguments:
            raise ValueError("Missing required keyword arguments: {}".format(", ".join(missing_arguments)))

        try:

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

        if not isinstance(self.good_count, (int, float)) or not isinstance(self.total_count, (int, float)):
            raise ValueError("Both good_count and total_count must be numbers.")

        if self.total_count == 0:
            raise ValueError("total_count cannot be zero.")

        return self.good_count / self.total_count

    def calculate_availability(self):

        if not isinstance(self.run_time, (int, float)) or not isinstance(self.total_time, (int, float)):
            raise ValueError("Both run_time and total_time must be numbers.")

        if self.total_time == 0:
            raise ValueError("total_time cannot be zero.")

        return self.run_time / self.total_time

    def calculate_performance(self):

        if not isinstance(self.total_count, (int, float)) or not isinstance(self.target_count, (int, float)):
            raise ValueError("Both total_count and target_count must be numbers.")

        if self.target_count == 0:
            raise ValueError("target_count cannot be zero.")

        return self.total_count / self.target_count

    def calculate_oee(self):

        try:

            quality = self.calculate_quality()
            availability = self.calculate_availability()
            performance = self.calculate_performance()
            return quality * availability * performance

        except ValueError as ve:
            raise ValueError("Error calculating OEE: " + str(ve))

        except Exception as e:
            raise Exception("Unexpected error calculating OEE: " + str(e))

