from datetime import datetime


class OEE:
    def __init__(self, data):
        self.availability = data['availability']
        self.performance = data['performance']
        self.quality = data['quality']
        self.time = datetime.now()
