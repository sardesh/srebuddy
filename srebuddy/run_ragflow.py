
from srebuddy.modules import logging_checker

if __name__ == "__main__":
    with open("srebuddy/data/sample_repo/sample_service.py") as f:
        code = f.read()

    logging_result = logging_checker.check_logging_implementation(code)
    print("\nLogging Check Result:\n", logging_result)
