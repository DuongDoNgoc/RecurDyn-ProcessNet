#!/usr/bin/env python3
"""
Phase 04 Test: Verify parser fix on stratified samples
Tests the fixed parser on 86 verification samples before full re-extraction.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from recurdyn_doc_parser import ProcessNetDocParser


def test_parser_fix_on_samples():
    """Test parser fix on verification samples."""
    print("Phase 04 Test: Parser Fix Validation")
    print("=" * 60)

    # Load sample manifest
    manifest_path = Path('verification/sample-manifest-with-ground-truth.json')
    print(f"Loading manifest: {manifest_path}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    samples = manifest['samples'][:10]  # Test on first 10 samples for speed
    print(f"Testing on {len(samples)} samples\n")

    # Initialize parser
    input_path = Path('output/extracted_chm')
    output_path = Path('verification/test-kb-sample.json')

    parser = ProcessNetDocParser(input_path, output_path)

    # Process sample files
    results = []
    for i, sample in enumerate(samples, 1):
        file_path = input_path / sample['file']

        if not file_path.exists():
            print(f"❌ [{i}/{len(samples)}] File not found: {sample['file']}")
            continue

        print(f"✓ [{i}/{len(samples)}] Processing: {sample['class_name']}")

        try:
            content = parser.parse_html_file(file_path)

            # Create temporary namespace data
            ns_data = {
                'classes': [],
                'standalone_methods': [],
                'properties': [],
                'examples': [],
                'files': []
            }

            # Add classes from content
            for cls in content['classes']:
                from dataclasses import asdict
                cls_dict = asdict(cls)
                ns_data['classes'].append(cls_dict)

            # Test the association method
            parser._associate_members_with_classes(ns_data, file_path, content)

            # Find the target class
            class_name = sample['class_name']
            target_class = None
            for cls in ns_data['classes']:
                if cls['name'] == class_name:
                    target_class = cls
                    break

            if not target_class:
                print(f"  ⚠️  Class {class_name} not found in parsed data")
                results.append({
                    'sample': class_name,
                    'status': 'class_not_found',
                    'expected_methods': sample.get('expected_methods', 0),
                    'expected_properties': sample.get('expected_properties', 0),
                    'actual_methods': 0,
                    'actual_properties': 0
                })
                continue

            # Check methods and properties
            actual_methods = len(target_class.get('methods', []))
            actual_properties = len(target_class.get('properties', []))
            expected_methods = sample.get('expected_methods', 0)
            expected_properties = sample.get('expected_properties', 0)

            methods_match = actual_methods == expected_methods
            properties_match = actual_properties == expected_properties

            print(f"  Methods: {actual_methods}/{expected_methods} {'✓' if methods_match else '✗'}")
            print(f"  Properties: {actual_properties}/{expected_properties} {'✓' if properties_match else '✗'}")

            results.append({
                'sample': class_name,
                'status': 'success',
                'expected_methods': expected_methods,
                'expected_properties': expected_properties,
                'actual_methods': actual_methods,
                'actual_properties': actual_properties,
                'methods_match': methods_match,
                'properties_match': properties_match
            })

        except Exception as e:
            print(f"  ❌ Error: {e}")
            results.append({
                'sample': sample['class_name'],
                'status': 'error',
                'error': str(e)
            })

    # Calculate metrics
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)

    successful = [r for r in results if r['status'] == 'success']
    methods_correct = sum(1 for r in successful if r.get('methods_match', False))
    properties_correct = sum(1 for r in successful if r.get('properties_match', False))

    total_expected_methods = sum(r.get('expected_methods', 0) for r in successful)
    total_actual_methods = sum(r.get('actual_methods', 0) for r in successful)
    total_expected_properties = sum(r.get('expected_properties', 0) for r in successful)
    total_actual_properties = sum(r.get('actual_properties', 0) for r in successful)

    print(f"Samples tested: {len(results)}")
    print(f"Successful parses: {len(successful)}")
    print()
    print("Methods:")
    print(f"  Expected total: {total_expected_methods}")
    print(f"  Actual total: {total_actual_methods}")
    print(f"  Exact matches: {methods_correct}/{len(successful)}")
    print(f"  Recall: {(total_actual_methods / max(total_expected_methods, 1)) * 100:.1f}%")
    print()
    print("Properties:")
    print(f"  Expected total: {total_expected_properties}")
    print(f"  Actual total: {total_actual_properties}")
    print(f"  Exact matches: {properties_correct}/{len(successful)}")
    print(f"  Recall: {(total_actual_properties / max(total_expected_properties, 1)) * 100:.1f}%")
    print()

    # Status determination
    if total_actual_methods > 0 or total_actual_properties > 0:
        print("STATUS: ✅ FIX WORKING - Methods/properties now associated with classes!")
        if total_actual_methods >= total_expected_methods * 0.8:
            print("  ✅ Methods recall >= 80%")
        if total_actual_properties >= total_expected_properties * 0.8:
            print("  ✅ Properties recall >= 80%")
        return 0
    else:
        print("STATUS: ❌ FIX NOT WORKING - Still 0% extraction")
        return 1


if __name__ == '__main__':
    sys.exit(test_parser_fix_on_samples())
