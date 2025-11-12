#!/usr/bin/env python3
"""
QA Test Suite for Garmin MCP Refactoring
Tests syntax, imports, and Pydantic model validation
"""
import sys
import py_compile
import traceback
from pathlib import Path

# Test results tracking
results = {
    "syntax_errors": [],
    "import_errors": [],
    "model_validation_errors": [],
    "warnings": []
}

print("=" * 80)
print("GARMIN MCP QA TEST SUITE")
print("=" * 80)
print()

# Phase 1: Syntax Validation
print("Phase 1: Python Syntax Validation")
print("-" * 80)

modules_to_test = [
    "src/garmin_mcp/models.py",
    "src/garmin_mcp/devices.py",
    "src/garmin_mcp/gear_management.py",
    "src/garmin_mcp/user_profile.py",
    "src/garmin_mcp/womens_health.py",
    "src/garmin_mcp/weight_management.py",
    "src/garmin_mcp/challenges.py",
    "src/garmin_mcp/training.py",
    "src/garmin_mcp/workouts.py",
    "src/garmin_mcp/data_management.py",
    "src/garmin_mcp/health_wellness.py",
]

syntax_pass = 0
for module in modules_to_test:
    try:
        py_compile.compile(module, doraise=True)
        print(f"✓ {module}")
        syntax_pass += 1
    except py_compile.PyCompileError as e:
        print(f"✗ {module}")
        results["syntax_errors"].append({
            "file": module,
            "error": str(e)
        })

print(f"\nSyntax Check: {syntax_pass}/{len(modules_to_test)} files passed")
print()

# Phase 2: Import Validation
print("Phase 2: Import Validation")
print("-" * 80)

import_tests = [
    ("models", "from garmin_mcp import models"),
    ("devices", "from garmin_mcp import devices"),
    ("gear_management", "from garmin_mcp import gear_management"),
    ("user_profile", "from garmin_mcp import user_profile"),
    ("womens_health", "from garmin_mcp import womens_health"),
    ("weight_management", "from garmin_mcp import weight_management"),
    ("challenges", "from garmin_mcp import challenges"),
    ("training", "from garmin_mcp import training"),
    ("workouts", "from garmin_mcp import workouts"),
    ("data_management", "from garmin_mcp import data_management"),
    ("health_wellness", "from garmin_mcp import health_wellness"),
]

import_pass = 0
for name, import_stmt in import_tests:
    try:
        exec(import_stmt)
        print(f"✓ {name}")
        import_pass += 1
    except Exception as e:
        print(f"✗ {name}: {str(e)}")
        results["import_errors"].append({
            "module": name,
            "error": str(e),
            "traceback": traceback.format_exc()
        })

print(f"\nImport Check: {import_pass}/{len(import_tests)} modules passed")
print()

# Phase 3: Pydantic Model Validation Tests
print("Phase 3: Pydantic Model Validation Tests")
print("-" * 80)

from garmin_mcp.models import (
    DateInput, DateRangeInput, ActivityIdInput, ListActivitiesInput,
    WeightInput, WeightWithTimestampsInput, DeleteWeighInsInput,
    GoalTypeInput, ChallengesPaginationInput, BadgeChallengesPaginationInput,
    ProgressSummaryInput, WorkoutIdInput, WorkoutJsonInput,
    UserProfileIdInput, GearUuidInput, DeviceIdInput, DeviceSolarInput,
    BodyCompositionInput, BloodPressureInput, HydrationInput
)

validation_tests = [
    # DateInput tests
    ("DateInput - valid", lambda: DateInput(date="2024-01-15"), True),
    ("DateInput - invalid format", lambda: DateInput(date="2024/01/15"), False),
    ("DateInput - invalid date", lambda: DateInput(date="2024-13-01"), False),

    # DateRangeInput tests
    ("DateRangeInput - valid", lambda: DateRangeInput(start_date="2024-01-01", end_date="2024-01-31"), True),
    ("DateRangeInput - end before start", lambda: DateRangeInput(start_date="2024-01-31", end_date="2024-01-01"), False),

    # ActivityIdInput tests
    ("ActivityIdInput - valid", lambda: ActivityIdInput(activity_id=12345), True),
    ("ActivityIdInput - zero", lambda: ActivityIdInput(activity_id=0), False),
    ("ActivityIdInput - negative", lambda: ActivityIdInput(activity_id=-1), False),

    # ListActivitiesInput tests
    ("ListActivitiesInput - default", lambda: ListActivitiesInput(), True),
    ("ListActivitiesInput - custom", lambda: ListActivitiesInput(limit=50), True),
    ("ListActivitiesInput - too large", lambda: ListActivitiesInput(limit=101), False),

    # WeightInput tests
    ("WeightInput - valid kg", lambda: WeightInput(weight=70.5, unit_key="kg"), True),
    ("WeightInput - valid lb", lambda: WeightInput(weight=155.0, unit_key="lb"), True),
    ("WeightInput - invalid unit", lambda: WeightInput(weight=70.0, unit_key="grams"), False),

    # GoalTypeInput tests
    ("GoalTypeInput - active", lambda: GoalTypeInput(goal_type="active"), True),
    ("GoalTypeInput - future", lambda: GoalTypeInput(goal_type="future"), True),
    ("GoalTypeInput - invalid", lambda: GoalTypeInput(goal_type="completed"), False),

    # ChallengesPaginationInput tests
    ("ChallengesPaginationInput - valid", lambda: ChallengesPaginationInput(start=0, limit=50), True),
    ("ChallengesPaginationInput - negative start", lambda: ChallengesPaginationInput(start=-1, limit=50), False),

    # BadgeChallengesPaginationInput tests
    ("BadgeChallengesPaginationInput - valid", lambda: BadgeChallengesPaginationInput(start=1, limit=50), True),
    ("BadgeChallengesPaginationInput - zero start", lambda: BadgeChallengesPaginationInput(start=0, limit=50), False),

    # ProgressSummaryInput tests
    ("ProgressSummaryInput - valid", lambda: ProgressSummaryInput(start_date="2024-01-01", end_date="2024-01-31", metric="distance"), True),

    # WorkoutIdInput tests
    ("WorkoutIdInput - valid", lambda: WorkoutIdInput(workout_id=999), True),
    ("WorkoutIdInput - zero", lambda: WorkoutIdInput(workout_id=0), False),

    # DeviceIdInput tests
    ("DeviceIdInput - valid", lambda: DeviceIdInput(device_id="device123"), True),
    ("DeviceIdInput - empty", lambda: DeviceIdInput(device_id=""), False),

    # DeviceSolarInput tests
    ("DeviceSolarInput - valid", lambda: DeviceSolarInput(device_id="device123", date="2024-01-15"), True),

    # BodyCompositionInput tests
    ("BodyCompositionInput - minimal", lambda: BodyCompositionInput(date="2024-01-15", weight=70.0), True),
    ("BodyCompositionInput - with metrics", lambda: BodyCompositionInput(date="2024-01-15", weight=70.0, percent_fat=15.5, bmi=22.5), True),
    ("BodyCompositionInput - invalid weight", lambda: BodyCompositionInput(date="2024-01-15", weight=-1), False),

    # BloodPressureInput tests
    ("BloodPressureInput - valid", lambda: BloodPressureInput(systolic=120, diastolic=80, pulse=70), True),
    ("BloodPressureInput - out of range", lambda: BloodPressureInput(systolic=400, diastolic=80, pulse=70), False),

    # HydrationInput tests
    ("HydrationInput - valid", lambda: HydrationInput(value_in_ml=500, cdate="2024-01-15", timestamp="2024-01-15T12:00:00.000Z"), True),
    ("HydrationInput - too much", lambda: HydrationInput(value_in_ml=20000, cdate="2024-01-15", timestamp="2024-01-15T12:00:00.000Z"), False),
]

validation_pass = 0
for test_name, test_func, should_pass in validation_tests:
    try:
        result = test_func()
        if should_pass:
            print(f"✓ {test_name}")
            validation_pass += 1
        else:
            print(f"✗ {test_name} - Expected validation error but passed")
            results["model_validation_errors"].append({
                "test": test_name,
                "error": "Expected validation error but model accepted invalid data"
            })
    except Exception as e:
        if not should_pass:
            print(f"✓ {test_name} (correctly rejected)")
            validation_pass += 1
        else:
            print(f"✗ {test_name} - Unexpected error: {str(e)}")
            results["model_validation_errors"].append({
                "test": test_name,
                "error": str(e)
            })

print(f"\nValidation Tests: {validation_pass}/{len(validation_tests)} tests passed")
print()

# Summary
print("=" * 80)
print("QA TEST SUMMARY")
print("=" * 80)
print()

total_tests = len(modules_to_test) + len(import_tests) + len(validation_tests)
total_passed = syntax_pass + import_pass + validation_pass

print(f"Total Tests Run: {total_tests}")
print(f"Total Passed: {total_passed}")
print(f"Total Failed: {total_tests - total_passed}")
print()

if results["syntax_errors"]:
    print("SYNTAX ERRORS:")
    for error in results["syntax_errors"]:
        print(f"  - {error['file']}: {error['error']}")
    print()

if results["import_errors"]:
    print("IMPORT ERRORS:")
    for error in results["import_errors"]:
        print(f"  - {error['module']}: {error['error']}")
    print()

if results["model_validation_errors"]:
    print("MODEL VALIDATION ERRORS:")
    for error in results["model_validation_errors"]:
        print(f"  - {error['test']}: {error['error']}")
    print()

# Exit code
if total_passed == total_tests:
    print("✅ ALL TESTS PASSED!")
    sys.exit(0)
else:
    print("❌ SOME TESTS FAILED")
    sys.exit(1)
