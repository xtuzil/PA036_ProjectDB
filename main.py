from ExperimentApp import ExperimentApp
import time

def main():
    experiment_app = ExperimentApp()

    print("Running the app..")
    # possibly to run repeatedly in loop
    for i in range(5):
        time.sleep(5)
        experiment_app.run()


if __name__ == '__main__':
    main()