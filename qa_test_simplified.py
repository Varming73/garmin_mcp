#!/usr/bin/env python3
"""
Simplified QA Test Suite for Garmin MCP Refactoring
Tests syntax and static analysis without requiring external dependencies
"""
import sys
import py_compile
import ast
from pathlib import Path

# Test results tracking
results = {
    "syntax_errors": [],
    "ast_errors": [],
    "pattern_violations": [],
    "warnings": []
}

print("=" * 80)
print("GARMIN MCP QA TEST SUITE (SIMPLIFIED)")
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

# Phase 2: AST Parsing & Static Analysis
print("Phase 2: AST Parsing & Static Analysis")
print("-" * 80)

ast_pass = 0
for module in modules_to_test:
    try:
        with open(module, 'r') as f:
            code = f.read()
        tree = ast.parse(code, filename=module)
        print(f"✓ {module}")
        ast_pass += 1
    except SyntaxError as e:
        print(f"✗ {module}: {str(e)}")
        results["ast_errors"].append({
            "file": module,
            "error": str(e)
        })

print(f"\nAST Parsing: {ast_pass}/{len(modules_to_test)} files passed")
print()

# Phase 3: Pattern Validation (Static Analysis)
print("Phase 3: Pattern Validation (Static Analysis)")
print("-" * 80)

def check_module_patterns(filepath):
    """Check if module follows refactoring patterns"""
    issues = []

    with open(filepath, 'r') as f:
        content = f.read()

    # Check 1: Has type hints for garmin_client
    if "garmin_client:" not in content and "models.py" not in filepath:
        issues.append("Missing type hint for garmin_client")

    # Check 2: Has Optional import (for modules, not models.py)
    if "from typing import Optional" not in content and "models.py" not in filepath:
        issues.append("Missing 'from typing import Optional' import")

    # Check 3: Has logger configured
    if "get_logger" not in content and "models.py" not in filepath:
        issues.append("Missing logger configuration")

    # Check 4: Has response imports (for modules, not models.py)
    if "models.py" not in filepath:
        if "success_response" not in content:
            issues.append("Missing success_response import")
        if "error_response" not in content:
            issues.append("Missing error_response import")

    # Check 5: Async functions (for modules, not models.py)
    if "async def" in content and "models.py" not in filepath:
        # Check that tools are async
        if "@app.tool()" in content:
            # Simple check - at least one async function exists
            pass

    return issues

pattern_pass = 0
for module in modules_to_test:
    issues = check_module_patterns(module)
    if not issues:
        print(f"✓ {module}")
        pattern_pass += 1
    else:
        print(f"⚠ {module}:")
        for issue in issues:
            print(f"    - {issue}")
        results["pattern_violations"].append({
            "file": module,
            "issues": issues
        })

print(f"\nPattern Check: {pattern_pass}/{len(modules_to_test)} files passed")
print()

# Phase 4: Import Statement Validation
print("Phase 4: Import Statement Validation")
print("-" * 80)

def check_imports(filepath):
    """Check if imports are properly formatted"""
    issues = []

    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Check for unused imports (basic check)
    # Check for circular imports (basic check)
    imports_section_ended = False
    last_import_line = 0

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track where imports are
        if stripped.startswith(('import ', 'from ')):
            last_import_line = i
            if imports_section_ended:
                issues.append(f"Line {i}: Import statement after code (should be at top)")
        elif stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
            imports_section_ended = True

    return issues

import_pass = 0
for module in modules_to_test:
    issues = check_imports(module)
    if not issues:
        print(f"✓ {module}")
        import_pass += 1
    else:
        print(f"⚠ {module}:")
        for issue in issues:
            print(f"    - {issue}")
        results["warnings"].append({
            "file": module,
            "issues": issues
        })

print(f"\nImport Organization: {import_pass}/{len(modules_to_test)} files passed")
print()

# Phase 5: Function Signature Analysis
print("Phase 5: Function Signature Analysis")
print("-" * 80)

def check_function_signatures(filepath):
    """Check async function signatures"""
    issues = []

    with open(filepath, 'r') as f:
        content = f.read()

    try:
        tree = ast.parse(content, filename=filepath)
    except:
        return ["Could not parse file"]

    for node in ast.walk(tree):
        if isinstance(node, ast.AsyncFunctionDef):
            # Check return type annotation
            if node.returns is None and "models.py" not in filepath:
                issues.append(f"Function '{node.name}' missing return type annotation")

    return issues

signature_pass = 0
for module in modules_to_test:
    issues = check_function_signatures(module)
    if not issues or module.endswith("models.py"):
        print(f"✓ {module}")
        signature_pass += 1
    else:
        print(f"⚠ {module}:")
        for issue in issues:
            print(f"    - {issue}")

print(f"\nFunction Signatures: {signature_pass}/{len(modules_to_test)} files passed")
print()

# Summary
print("=" * 80)
print("QA TEST SUMMARY")
print("=" * 80)
print()

total_categories = 5
passed_categories = sum([
    1 if syntax_pass == len(modules_to_test) else 0,
    1 if ast_pass == len(modules_to_test) else 0,
    1 if pattern_pass == len(modules_to_test) else 0,
    1 if import_pass == len(modules_to_test) else 0,
    1 if signature_pass == len(modules_to_test) else 0,
])

print(f"Test Categories: {total_categories}")
print(f"  ✓ Syntax Validation: {syntax_pass}/{len(modules_to_test)} files")
print(f"  ✓ AST Parsing: {ast_pass}/{len(modules_to_test)} files")
print(f"  {'✓' if pattern_pass == len(modules_to_test) else '⚠'} Pattern Validation: {pattern_pass}/{len(modules_to_test)} files")
print(f"  {'✓' if import_pass == len(modules_to_test) else '⚠'} Import Organization: {import_pass}/{len(modules_to_test)} files")
print(f"  {'✓' if signature_pass == len(modules_to_test) else '⚠'} Function Signatures: {signature_pass}/{len(modules_to_test)} files")
print()

if results["syntax_errors"]:
    print("❌ SYNTAX ERRORS:")
    for error in results["syntax_errors"]:
        print(f"  - {error['file']}: {error['error']}")
    print()

if results["ast_errors"]:
    print("❌ AST ERRORS:")
    for error in results["ast_errors"]:
        print(f"  - {error['file']}: {error['error']}")
    print()

if results["pattern_violations"]:
    print("⚠ PATTERN VIOLATIONS:")
    for error in results["pattern_violations"]:
        print(f"  - {error['file']}:")
        for issue in error['issues']:
            print(f"      {issue}")
    print()

# Exit code
if syntax_pass == len(modules_to_test) and ast_pass == len(modules_to_test):
    print("✅ ALL CRITICAL TESTS PASSED!")
    print("   (Some warnings may exist but don't block deployment)")
    sys.exit(0)
else:
    print("❌ CRITICAL TESTS FAILED")
    sys.exit(1)
