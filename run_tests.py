import sys
import os

# Import the test modules directly by adding tests folder to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests"))
import test_exercise_and_chart
import test_features
import test_coach_tip
import test_fitness_score
import test_insights

from main import limiter
limiter.enabled = False

# Discover and run test functions
tests_1 = [(test_exercise_and_chart, name) for name in dir(test_exercise_and_chart) if name.startswith("test_")]
tests_2 = [(test_features, name) for name in dir(test_features) if name.startswith("test_")]
tests_3 = [(test_coach_tip, name) for name in dir(test_coach_tip) if name.startswith("test_")]
tests_4 = [(test_fitness_score, name) for name in dir(test_fitness_score) if name.startswith("test_")]
tests_5 = [(test_insights, name) for name in dir(test_insights) if name.startswith("test_")]
all_tests = sorted(tests_1 + tests_2 + tests_3 + tests_4 + tests_5, key=lambda x: x[1])

passed = 0
failed = 0

print("=== Running Custom Test Suite ===")
for test_mod, test_name in all_tests:
    test_func = getattr(test_mod, test_name)
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
