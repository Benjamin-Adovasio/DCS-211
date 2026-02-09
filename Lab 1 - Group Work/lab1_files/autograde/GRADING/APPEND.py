
#############################################################################
from typing import Callable
def testHarness(fcn: Callable, arg: str, expected: str | list) -> int:
    ''' function to help test an arbitrary function having one argument
    Parameters:
        fcn: the actual function being tested (pass without calling)
        arg: the argument being passed to the tested function
        expected: the expected result, either str or list in the context here
    Returns:
        None -- just prints
    '''
    result = fcn(arg)  # call the student's function, passing the given argument

    # see https://unicode-table.com/en/sets/check/
    # replace these as you see fit
    mark = "✓" if result == expected else "✗"
    print(f"Testing {fcn.__name__}({repr(arg)}):")
    print(f"\t {mark} result   = {result}")
    print(f"\t   expected = {expected}")

    if result == expected:
        return 1   # correct +1
    return 0       # incorrect +0

###################
def main_grading():
    count = 0
    tests = 0

    arg = []; expected = 0; tests += 1
    count += testHarness(compute_sum, arg, expected)

    arg = [0]; expected = 0; tests += 1
    count += testHarness(compute_sum, arg, expected)

    arg = [1,2,3]; expected = 6; tests += 1
    count += testHarness(compute_sum, arg, expected)

    arg = [-1,2,-3]; expected = -2; tests += 1
    count += testHarness(compute_sum, arg, expected)

    
    arg = []; expected = None; tests += 1
    count += testHarness(compute_product, arg, expected)

    arg = [0]; expected = 0; tests += 1
    count += testHarness(compute_product, arg, expected)

    arg = [1,2,3]; expected = 6; tests += 1
    count += testHarness(compute_product, arg, expected)

    arg = [-1,2,-3]; expected = 6; tests += 1
    count += testHarness(compute_product, arg, expected)

    arg = [-1,-2,-3]; expected = -6; tests += 1
    count += testHarness(compute_product, arg, expected)

    arg = [-1,-2,-3,0]; expected = 0; tests += 1
    count += testHarness(compute_product, arg, expected)

    print('-' * 30)
    print(f"Total tests passed: {count} / {tests}")
    print('-' * 30)

if __name__ == "__main__":
    main_grading()
