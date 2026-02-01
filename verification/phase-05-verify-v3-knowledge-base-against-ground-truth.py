#!/usr/bin/env python3
"""
Phase 05: Verify v3 knowledge base against ground truth
Modified version of phase-03 script to test the new v3 KB
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def load_json(file_path: Path) -> dict:
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_class_in_kb(kb: dict, class_name: str, namespace: str) -> dict:
    """Find class in knowledge base by name and namespace."""
    ns_data = kb.get('namespaces', {}).get(namespace, {})

    # Search in classes
    for cls in ns_data.get('classes', []):
        if cls.get('name') == class_name:
            return cls

    return None

def verify_sample(sample: dict, kb: dict) -> dict:
    """Verify a single sample against knowledge base."""
    class_name = sample['class_name']
    namespace = sample['namespace']
    expected_methods = sample.get('expected_methods', 0)
    expected_properties = sample.get('expected_properties', 0)

    # Find class in KB
    cls = find_class_in_kb(kb, class_name, namespace)

    if not cls:
        return {
            'sample_id': sample['id'],
            'class_name': class_name,
            'namespace': namespace,
            'status': 'class_not_found',
            'expected_methods': expected_methods,
            'expected_properties': expected_properties,
            'actual_methods': 0,
            'actual_properties': 0,
            'methods_match': False,
            'properties_match': False
        }

    # Get actual counts
    actual_methods = len(cls.get('methods', []))
    actual_properties = len(cls.get('properties', []))

    # Check matches
    methods_match = actual_methods == expected_methods
    properties_match = actual_properties == expected_properties

    return {
        'sample_id': sample['id'],
        'class_name': class_name,
        'namespace': namespace,
        'type': sample.get('type', 'unknown'),
        'complexity': sample.get('complexity', 'unknown'),
        'html_pattern': sample.get('html_pattern', 'unknown'),
        'status': 'found',
        'expected_methods': expected_methods,
        'expected_properties': expected_properties,
        'actual_methods': actual_methods,
        'actual_properties': actual_properties,
        'methods_match': methods_match,
        'properties_match': properties_match,
        'methods_diff': actual_methods - expected_methods,
        'properties_diff': actual_properties - expected_properties
    }

def calculate_metrics(results: list) -> dict:
    """Calculate accuracy metrics from verification results."""
    total_samples = len(results)
    classes_found = sum(1 for r in results if r['status'] == 'found')

    methods_match = sum(1 for r in results if r.get('methods_match', False))
    properties_match = sum(1 for r in results if r.get('properties_match', False))

    total_expected_methods = sum(r['expected_methods'] for r in results)
    total_actual_methods = sum(r['actual_methods'] for r in results)
    total_expected_properties = sum(r['expected_properties'] for r in results)
    total_actual_properties = sum(r['actual_properties'] for r in results)

    methods_recall = (total_actual_methods / max(total_expected_methods, 1)) if total_expected_methods > 0 else 0
    properties_recall = (total_actual_properties / max(total_expected_properties, 1)) if total_expected_properties > 0 else 0

    return {
        'total_samples': total_samples,
        'classes_found': classes_found,
        'class_discovery_rate': classes_found / max(total_samples, 1),
        'methods_exact_match_rate': methods_match / max(total_samples, 1),
        'properties_exact_match_rate': properties_match / max(total_samples, 1),
        'total_expected_methods': total_expected_methods,
        'total_actual_methods': total_actual_methods,
        'total_expected_properties': total_expected_properties,
        'total_actual_properties': total_actual_properties,
        'methods_recall': methods_recall,
        'properties_recall': properties_recall,
        'overall_accuracy': (methods_match + properties_match) / (2 * max(total_samples, 1))
    }

def main():
    """Main verification workflow."""
    # Paths - CHANGED TO V3
    manifest_path = Path('verification/sample-manifest-with-ground-truth.json')
    kb_path = Path('output/processnet-knowledge-v3.json')
    output_path = Path('verification/phase-05-v3-verification-results.json')

    print("Phase 05: V3 Knowledge Base Verification")
    print("=" * 60)

    # Load data
    print(f"Loading manifest: {manifest_path}")
    manifest = load_json(manifest_path)
    samples = manifest['samples']

    print(f"Loading knowledge base: {kb_path}")
    kb = load_json(kb_path)

    print(f"Samples to verify: {len(samples)}")
    print()

    # Run verification
    results = []
    for i, sample in enumerate(samples, 1):
        result = verify_sample(sample, kb)
        results.append(result)

        if i % 10 == 0:
            print(f"Progress: {i}/{len(samples)} samples verified")

    print(f"Verification complete: {len(results)} samples processed")
    print()

    # Calculate metrics
    metrics = calculate_metrics(results)

    # Save results
    output = {
        'metadata': {
            'verification_date': datetime.now().isoformat(),
            'manifest_file': str(manifest_path),
            'knowledge_base_file': str(kb_path),
            'total_samples': len(samples),
            'version': 'v3'
        },
        'metrics': metrics,
        'results': results
    }

    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    # Print summary
    print("=" * 60)
    print("V3 VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Total samples: {metrics['total_samples']}")
    print(f"Classes found: {metrics['classes_found']} ({metrics['class_discovery_rate']*100:.1f}%)")
    print()
    print("Methods:")
    print(f"  Expected: {metrics['total_expected_methods']}")
    print(f"  Actual:   {metrics['total_actual_methods']}")
    print(f"  Recall:   {metrics['methods_recall']*100:.2f}%")
    print()
    print("Properties:")
    print(f"  Expected: {metrics['total_expected_properties']}")
    print(f"  Actual:   {metrics['total_actual_properties']}")
    print(f"  Recall:   {metrics['properties_recall']*100:.2f}%")
    print()
    print(f"Overall Accuracy: {metrics['overall_accuracy']*100:.2f}%")
    print()

    # Status
    if metrics['methods_recall'] >= 0.80 and metrics['properties_recall'] >= 0.80:
        print("STATUS: ✅ PASSED - Extraction accuracy >= 80%")
        return 0
    elif metrics['methods_recall'] == 0 and metrics['properties_recall'] == 0:
        print("STATUS: ❌ CRITICAL FAILURE - 0% extraction accuracy")
        return 1
    else:
        print("STATUS: ⚠️  PARTIAL SUCCESS - Some extraction working but below 80% threshold")
        return 1

if __name__ == '__main__':
    sys.exit(main())
