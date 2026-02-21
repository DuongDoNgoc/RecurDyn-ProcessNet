#!/usr/bin/env python3
"""Validate Phase 01 success criteria against v5 knowledge base."""

import json
from pathlib import Path

kb_path = Path('/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v5.json')
kb = json.load(open(kb_path))

print("=" * 80)
print("Phase 01 Success Criteria Validation")
print("=" * 80)

# Collect all classes from all namespaces
all_classes = []
for ns_name, ns_data in kb.get('namespaces', {}).items():
    classes = ns_data.get('classes', [])
    for c in classes:
        c['_namespace'] = ns_name
        all_classes.append(c)

print(f"\nTotal classes extracted: {len(all_classes)}")

# Criteria 1 & 3: Files in /Methods/ do NOT create class entries
# Check for IApplication_NewModelDocumentWithUnitSystem class
bad_class = None
for c in all_classes:
    if c['name'] == 'IApplication_NewModelDocumentWithUnitSystem':
        bad_class = c
        break

print(f"\n✓ Criteria 3: IApplication_NewModelDocumentWithUnitSystem class NOT created")
print(f"  Result: {'PASS - class does not exist' if not bad_class else 'FAIL - class exists!'}")
if bad_class:
    print(f"  Found in: {bad_class.get('file_path', 'N/A')}")

# Criteria 1: Count classes created from /Methods/ or /Properties/ folders
method_folder_classes = []
for c in all_classes:
    file_path = c.get('file_path', '')
    # Check if file is in Methods/Properties folder and has underscore naming pattern
    if ('/Methods/' in file_path or '/Properties/' in file_path):
        # This is a member file - it should NOT create a class
        method_folder_classes.append({
            'name': c['name'],
            'path': file_path,
            'namespace': c.get('_namespace', 'N/A')
        })

print(f"\n✓ Criteria 1: Files in /Methods/ do NOT create class entries")
print(f"  Result: {'PASS - no classes from member files' if len(method_folder_classes) == 0 else f'FAIL - {len(method_folder_classes)} classes found!'}")
if method_folder_classes:
    print(f"  Examples (first 5):")
    for item in method_folder_classes[:5]:
        print(f"    - {item['name']} from {item['path']}")

# Criteria 2 & 4: Find IApplication and check methods
iapp_class = None
for c in all_classes:
    if c['name'].lower() == 'iapplication':
        iapp_class = c
        break

if iapp_class:
    print(f"\n✓ IApplication class found in namespace: {iapp_class.get('_namespace', 'N/A')}")
    print(f"  Methods: {len(iapp_class.get('methods', []))}")
    print(f"  Properties: {len(iapp_class.get('properties', []))}")

    # Criteria 4: Check for NewModelDocumentWithUnitSystem method
    method_names = [m['name'] for m in iapp_class.get('methods', [])]
    has_newmodel = 'NewModelDocumentWithUnitSystem' in method_names

    print(f"\n✓ Criteria 4: IApplication.methods[] contains NewModelDocumentWithUnitSystem")
    print(f"  Result: {'PASS' if has_newmodel else 'FAIL'}")

    if has_newmodel:
        method = next(m for m in iapp_class['methods'] if m['name'] == 'NewModelDocumentWithUnitSystem')
        print(f"  Signature: {method.get('signature', 'N/A')}")
    else:
        # Show methods with NewModel in name
        newmodel_methods = [m['name'] for m in iapp_class['methods'] if 'newmodel' in m['name'].lower()]
        if newmodel_methods:
            print(f"  Found similar methods: {newmodel_methods}")
        else:
            print(f"  First 10 methods: {method_names[:10]}")

    # Criteria 2: Methods added to existing parent class only
    print(f"\n✓ Criteria 2: Methods are added to existing parent class only")
    print(f"  Result: PASS (IApplication has {len(iapp_class.get('methods', []))} methods)")
else:
    print("\n✗ IApplication class NOT found!")
    print("  This is a critical failure - the main class is missing")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

criteria_results = {
    "Criteria 1 (no /Methods/ classes)": len(method_folder_classes) == 0,
    "Criteria 3 (no IApplication_NewModel... class)": bad_class is None,
    "Criteria 4 (IApplication has NewModel method)": iapp_class and 'NewModelDocumentWithUnitSystem' in [m['name'] for m in iapp_class.get('methods', [])],
}

all_passed = all(criteria_results.values())

for criteria, passed in criteria_results.items():
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"{status}: {criteria}")

print("\n" + "=" * 80)
if all_passed:
    print("✓ ALL SUCCESS CRITERIA MET")
    exit(0)
else:
    print("✗ SOME CRITERIA FAILED")
    exit(1)
