import sys
import os

# Import the test module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tests import test_exercise_and_chart

# Discover and run test functions
tests = [name for name in dir(test_exercise_and_chart) if name.startswith("test_")]

passed = 0
failed = 0

print("=== Running Custom Test Suite ===")
for test_name in sorted(tests):
    test_func = getattr(test_exercise_and_chart, test_name)
    try:
        test_func()
        print(f"[PASS] {test_name}")
        passed += 1
    except AssertionError as e:
        print(f"[FAIL] {test_name}")
        print(f"  AssertionError: {e}")
        failed += 1
    except Exception as e:
        print(f"[ERROR] {test_name}")
        print(f"  {type(e).__name__}: {e}")
        failed += 1

print("\n=== Test Run Summary ===")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed > 0:
    sys.exit(1)
