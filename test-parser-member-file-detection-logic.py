#!/usr/bin/env python3
"""Quick test script to verify member file detection logic."""

from pathlib import Path
import sys
sys.path.insert(0, 'src')

# Import directly from the module file
import importlib.util
spec = importlib.util.spec_from_file_location("parser", "src/recurdyn-doc-parser.py")
parser_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(parser_module)

# Get the class
ProcessNetDocParser = parser_module.ProcessNetDocParser

# Create parser instance
parser = ProcessNetDocParser(
    input_path=Path("test_data"),  # Dummy path
    output_path=Path("test_output.json")
)

# Test cases
test_cases = [
    ("Python/Professional/IApplication/Methods/IApplication_NewModelDocumentWithUnitSystem.html", True, "IApplication"),
    ("Python/Professional/IApplication/Properties/IApplication_Version.html", True, "IApplication"),
    ("Python/Professional/IApplication.html", False, None),
    ("Python/Professional/IBody/Methods/IBody_GetMass.html", True, "IBody"),
    ("Python/Professional/CoreExample.html", False, None),
]

print("Testing member file detection:")
print("=" * 80)

all_passed = True
for path_str, expected_is_member, expected_parent in test_cases:
    file_path = Path(path_str)

    # Test _is_member_file
    is_member = parser._is_member_file(file_path)

    # Test _extract_parent_class_from_path
    parent = parser._extract_parent_class_from_path(file_path)

    # Verify results
    is_member_ok = is_member == expected_is_member
    parent_ok = parent == expected_parent

    status = "✓" if (is_member_ok and parent_ok) else "✗"
    all_passed = all_passed and is_member_ok and parent_ok

    print(f"{status} {path_str}")
    print(f"  Is member: {is_member} (expected {expected_is_member}) - {'OK' if is_member_ok else 'FAIL'}")
    print(f"  Parent class: {parent} (expected {expected_parent}) - {'OK' if parent_ok else 'FAIL'}")
    print()

print("=" * 80)
if all_passed:
    print("✓ All tests PASSED")
    sys.exit(0)
else:
    print("✗ Some tests FAILED")
    sys.exit(1)
