#!/usr/bin/env python3
"""
Validation script for Phase 02: Query Interface Fixes
Tests that all methods are searchable from classes[] structure
"""

import subprocess
import json
import sys

def run_command(cmd):
    """Run command and return output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout, result.returncode

def test_search_returns_results():
    """Test 1: Search should return results for CreateBody"""
    print("Test 1: Search for 'CreateBody' should return results...")
    output, code = run_command('python3 src/processnet-query-interface.py --kb output/processnet-knowledge-v6.json --search "CreateBody"')

    if "Name:" in output and "Type: method" in output:
        print("  ✓ PASS: Search returns method results")
        return True
    else:
        print("  ✗ FAIL: No results found")
        return False

def test_statistics_count():
    """Test 2: Statistics should show 6773 methods"""
    print("\nTest 2: Statistics should count methods from classes...")
    output, code = run_command('echo "stats" | python3 src/processnet-query-interface.py --kb output/processnet-knowledge-v6.json')

    if "methods: 6773" in output:
        print("  ✓ PASS: Method count is 6773")
        return True
    else:
        print(f"  ✗ FAIL: Unexpected method count in output:\n{output}")
        return False

def test_list_namespace_methods():
    """Test 3: List namespace should show methods from classes"""
    print("\nTest 3: Listing namespace should show methods...")
    output, code = run_command('echo "list ProcessNet" | python3 src/processnet-query-interface.py --kb output/processnet-knowledge-v6.json')

    if "Methods (2244):" in output or "Methods (" in output:
        print("  ✓ PASS: Namespace lists methods from classes")
        return True
    else:
        print("  ✗ FAIL: No methods listed")
        return False

def test_description_search():
    """Test 4: Description search should work"""
    print("\nTest 4: Description search should find examples...")
    output, code = run_command('echo "desc create body" | python3 src/processnet-query-interface.py --kb output/processnet-knowledge-v6.json')

    if "Type: example" in output or "Type: method" in output:
        print("  ✓ PASS: Description search returns results")
        return True
    else:
        print("  ✗ FAIL: No results from description search")
        return False

def main():
    print("="*60)
    print("Phase 02 Validation: Query Interface Fixes")
    print("="*60)

    tests = [
        test_search_returns_results,
        test_statistics_count,
        test_list_namespace_methods,
        test_description_search
    ]

    results = []
    for test in tests:
        results.append(test())

    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All validation tests PASSED")
        return 0
    else:
        print("✗ Some tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
