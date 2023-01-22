#!/usr/bin/env python3
import sys
from integration_test import available_tests

print("Please specify the integration test to run")
test_index = 1
for test_option in available_tests:
    print(f"{test_index}) {test_option.name()}")
    test_index += 1

choice = input("Your choice?")

try:
    option = int(choice)
    if option > len(available_tests):
        raise "Option not available"
    else:
        test_class = available_tests[option - 1]
except:
    print(f"Invalid option: {choice}")
    sys.exit(1)

test_name = test_class.name()
print(f"Running test {choice}: {test_name}")

test = test_class()
test.run(sys.argv)
