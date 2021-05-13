from ExperimentApp import ExperimentApp
from time import time

NUMBER_OF_ROUNDS = 3


def main():
    print("Running the app..")
    start = time()
    experiment_app = ExperimentApp()

    # possibly to run repeatedly in loop
    for i in range(NUMBER_OF_ROUNDS):
        experiment_app.run()

    end = time()
    print("\nFinal time: ", end - start)


if __name__ == '__main__':
    main()