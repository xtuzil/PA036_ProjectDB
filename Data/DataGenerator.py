from Data.SpeedViolationDataGenerator import SpeedViolationDataGenerator
from os import path


class DataGenerator:
    SPEED_VIOLATION_RECORDS_COUNT = 100000
    SPEED_VIOLATION_PATH = "Data/speedViolationData.json"
    PERSON_PATH = "Data/personData.json"

    @staticmethod
    def generate():
        # Generate data if they are not already
        if not path.exists(DataGenerator.SPEED_VIOLATION_PATH):
            print("Generating speed_violation data...")
            # file personData.json must exists
            if path.exists(DataGenerator.PERSON_PATH):
                SpeedViolationDataGenerator.generate_speed_violation(DataGenerator.PERSON_PATH,
                                                                     DataGenerator.SPEED_VIOLATION_RECORDS_COUNT)
                return True
            else:
                print("File personData.json not accessible")
                return False

        return True
