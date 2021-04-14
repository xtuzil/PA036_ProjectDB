from Data.GenerateSpeedViolationData import SpeedViolationDataGenerator
from os import path


class Helper:
    SPEED_VIOLATION_RECORDS_COUNT = 100000
    SPEED_VIOLATION_PATH = "Data/speedViolationData.json"
    PERSON_PATH = "Data/personData.json"

    @staticmethod
    def generate():
        # Generate data if they are not already
        if not path.exists(Helper.SPEED_VIOLATION_PATH):
            # file personData.json must exists
            if path.exists(Helper.PERSON_PATH):
                SpeedViolationDataGenerator.generate_speed_violation(Helper.PERSON_PATH,
                                                                     Helper.SPEED_VIOLATION_RECORDS_COUNT)
                return True
            else:
                print("File personData.json not accessible")
                return False

        return True
