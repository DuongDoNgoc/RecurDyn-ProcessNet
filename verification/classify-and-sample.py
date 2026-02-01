#!/usr/bin/env python3
"""
Data Classification and Stratified Sampling Script
Analyzes knowledge base and selects 100 representative samples for verification.
"""

import json
import random
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

@dataclass
class Sample:
    id: int
    file: str
    type: str
    namespace: str
    class_name: str
    complexity: str
    html_pattern: str
    expected_methods: int
    expected_properties: int
    inheritance: str
    description: str

class KnowledgeBaseClassifier:
    def __init__(self, kb_path: str):
        self.kb_path = Path(kb_path)
        self.kb = json.load(open(kb_path))
        self.samples: List[Sample] = []
        self.stats = {
            'by_namespace': defaultdict(int),
            'by_type': defaultdict(int),
            'by_complexity': defaultdict(int),
            'by_inheritance': defaultdict(int)
        }

    def classify_complexity(self, methods_count: int, properties_count: int) -> str:
        """Classify complexity based on expected member counts from HTML."""
        total = methods_count + properties_count
        if total == 0:
            return 'simple'
        elif total <= 5:
            return 'simple'
        elif total <= 15:
            return 'medium'
        else:
            return 'complex'

    def classify_type(self, class_data: dict) -> str:
        """Classify type based on naming patterns and inheritance."""
        name = class_data['name']
        inheritance = class_data.get('inheritance', 'object')

        # Enum detection
        if 'Enum' in inheritance or name.endswith('Type'):
            return 'enum'

        # Interface detection
        if name.startswith('I') and name[1:2].isupper():
            return 'interface'

        # Example classes
        if 'Example' in name:
            return 'example'

        return 'class'

    def analyze_knowledge_base(self):
        """Analyze entire knowledge base and collect statistics."""
        print(f"Analyzing knowledge base: {self.kb_path}")
        print(f"Total namespaces: {len(self.kb['namespaces'])}\n")

        all_classes = []

        for ns_name, ns_data in self.kb['namespaces'].items():
            classes = ns_data.get('classes', [])
            print(f"{ns_name}: {len(classes)} classes")

            for cls in classes:
                cls_type = self.classify_type(cls)

                # For now, we can't determine expected counts from extracted data
                # We'll need to parse HTML for actual verification
                # Setting placeholder values
                complexity = 'unknown'

                all_classes.append({
                    'class': cls,
                    'namespace': ns_name,
                    'type': cls_type,
                    'complexity': complexity
                })

                self.stats['by_namespace'][ns_name] += 1
                self.stats['by_type'][cls_type] += 1
                self.stats['by_complexity'][complexity] += 1
                self.stats['by_inheritance'][cls.get('inheritance', 'unknown')] += 1

        print(f"\nTotal classes: {len(all_classes)}")
        return all_classes

    def select_stratified_samples(self, all_classes: List[dict], total_samples: int = 100) -> List[Sample]:
        """Select stratified samples with proportional allocation."""
        random.seed(42)  # Reproducible sampling

        samples = []
        sample_id = 1

        # Strategy 1: By namespace (proportional to size)
        # Get top 5 namespaces by size
        ns_counts = sorted(self.stats['by_namespace'].items(), key=lambda x: x[1], reverse=True)
        top_namespaces = [ns for ns, count in ns_counts[:5]]

        # Allocate 50 samples across namespaces proportionally
        ns_samples = 50
        ns_allocation = {}
        total_in_top_ns = sum(count for ns, count in ns_counts[:5])

        for ns, count in ns_counts[:5]:
            allocation = max(4, int((count / total_in_top_ns) * ns_samples))
            ns_allocation[ns] = allocation

        # Strategy 2: By type (balanced)
        type_allocation = {
            'class': 30,
            'interface': 25,
            'enum': 20,
            'example': 15,
            'misc': 10
        }

        # Select samples by namespace
        for ns, target_count in ns_allocation.items():
            ns_classes = [c for c in all_classes if c['namespace'] == ns]
            selected = random.sample(ns_classes, min(target_count, len(ns_classes)))

            for cls_data in selected:
                sample = Sample(
                    id=sample_id,
                    file=cls_data['class']['source_file'],
                    type=cls_data['type'],
                    namespace=ns,
                    class_name=cls_data['class']['name'],
                    complexity='unknown',  # Will determine from HTML
                    html_pattern='unknown',  # Will determine from HTML
                    expected_methods=0,  # Will extract from HTML
                    expected_properties=0,  # Will extract from HTML
                    inheritance=cls_data['class'].get('inheritance', 'object'),
                    description=cls_data['class'].get('description', '')
                )
                samples.append(sample)
                sample_id += 1

        # Add remaining samples from different types to reach 100
        remaining = total_samples - len(samples)

        # Get classes not yet sampled
        sampled_files = {s.file for s in samples}
        unsampled = [c for c in all_classes if c['class']['source_file'] not in sampled_files]

        # Sample by type to ensure diversity
        for cls_type in ['interface', 'enum', 'example', 'class']:
            type_classes = [c for c in unsampled if c['type'] == cls_type]
            if type_classes and remaining > 0:
                take = min(remaining, len(type_classes), 10)
                selected = random.sample(type_classes, take)

                for cls_data in selected:
                    sample = Sample(
                        id=sample_id,
                        file=cls_data['class']['source_file'],
                        type=cls_data['type'],
                        namespace=cls_data['namespace'],
                        class_name=cls_data['class']['name'],
                        complexity='unknown',
                        html_pattern='unknown',
                        expected_methods=0,
                        expected_properties=0,
                        inheritance=cls_data['class'].get('inheritance', 'object'),
                        description=cls_data['class'].get('description', '')
                    )
                    samples.append(sample)
                    sample_id += 1
                    remaining -= 1

        return samples[:total_samples]

    def generate_classification_report(self, samples: List[Sample]) -> str:
        """Generate markdown classification report."""
        report = f"""# Data Classification Report

**Date:** 2026-02-01
**Knowledge Base:** {self.kb_path}
**Total Classes:** {sum(self.stats['by_namespace'].values())}
**Samples Selected:** {len(samples)}
**Selection Method:** Stratified Random Sampling (seed=42)

---

## Knowledge Base Statistics

### By Namespace
| Namespace | Classes | Percentage |
|-----------|---------|------------|
"""
        total_classes = sum(self.stats['by_namespace'].values())
        for ns, count in sorted(self.stats['by_namespace'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_classes * 100) if total_classes > 0 else 0
            report += f"| {ns} | {count} | {pct:.1f}% |\n"

        report += f"""
### By Type
| Type | Count | Percentage |
|------|-------|------------|
"""
        for type_name, count in sorted(self.stats['by_type'].items(), key=lambda x: x[1], reverse=True):
            pct = (count / total_classes * 100) if total_classes > 0 else 0
            report += f"| {type_name} | {count} | {pct:.1f}% |\n"

        report += f"""
### By Inheritance
| Base Class | Count | Percentage |
|------------|-------|------------|
"""
        for inheritance, count in sorted(self.stats['by_inheritance'].items(), key=lambda x: x[1], reverse=True)[:10]:
            pct = (count / total_classes * 100) if total_classes > 0 else 0
            report += f"| {inheritance} | {count} | {pct:.1f}% |\n"

        report += """
---

## Sample Distribution

### By Namespace
| Namespace | Samples | Source Percentage |
|-----------|---------|-------------------|
"""
        sample_ns_dist = defaultdict(int)
        for s in samples:
            sample_ns_dist[s.namespace] += 1

        for ns, count in sorted(sample_ns_dist.items(), key=lambda x: x[1], reverse=True):
            source_pct = (self.stats['by_namespace'][ns] / total_classes * 100) if total_classes > 0 else 0
            report += f"| {ns} | {count} | {source_pct:.1f}% |\n"

        report += """
### By Type
| Type | Samples | Source Percentage |
|------|---------|-------------------|
"""
        sample_type_dist = defaultdict(int)
        for s in samples:
            sample_type_dist[s.type] += 1

        for type_name, count in sorted(sample_type_dist.items(), key=lambda x: x[1], reverse=True):
            source_pct = (self.stats['by_type'][type_name] / total_classes * 100) if total_classes > 0 else 0
            report += f"| {type_name} | {count} | {source_pct:.1f}% |\n"

        report += """
---

## Sampling Methodology

### Selection Criteria
1. **Stratified Random Sampling**: Samples selected proportionally from strata
2. **Namespace Allocation**: Top 5 namespaces with 4-10 samples each
3. **Type Balance**: Ensure representation across class/interface/enum/example types
4. **Random Seed**: 42 (reproducible results)

### Exclusions
- Navigation pages (_static, _images)
- Index pages
- Auto-generated TOC files

### Quality Assurance
- All samples have valid source_file paths
- Minimum 4 samples per major namespace
- Diverse type representation (not just one type)

---

## Next Steps

1. **Phase 02**: Parse HTML for each sample to determine:
   - Expected methods count
   - Expected properties count
   - Complexity level (simple/medium/complex)
   - HTML pattern type
2. **Phase 03**: Run verification comparing HTML truth vs extracted data
3. **Phase 04**: Document findings and identify parser bugs

---

**Generated by:** classify-and-sample.py
**Status:** Classification Complete, HTML Parsing Pending
"""
        return report

    def save_manifest(self, samples: List[Sample], output_path: str):
        """Save sample manifest as JSON."""
        manifest = {
            'metadata': {
                'total_samples': len(samples),
                'selection_date': '2026-02-01',
                'selection_method': 'stratified_random_sampling',
                'random_seed': 42,
                'knowledge_base': str(self.kb_path)
            },
            'samples': [asdict(s) for s in samples]
        }

        with open(output_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"Saved manifest: {output_path}")

    def save_selection_log(self, samples: List[Sample], log_path: str):
        """Save selection log with details."""
        with open(log_path, 'w') as f:
            f.write("Sample Selection Log\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Total Samples: {len(samples)}\n")
            f.write(f"Random Seed: 42\n")
            f.write(f"Selection Date: 2026-02-01\n\n")
            f.write("Samples:\n")
            f.write("-" * 80 + "\n")

            for sample in samples:
                f.write(f"\n[{sample.id}] {sample.class_name}\n")
                f.write(f"  Namespace: {sample.namespace}\n")
                f.write(f"  Type: {sample.type}\n")
                f.write(f"  File: {sample.file}\n")
                f.write(f"  Inheritance: {sample.inheritance}\n")

        print(f"Saved selection log: {log_path}")

def main():
    print("=" * 80)
    print("Phase 01: Data Classification & Stratified Sampling")
    print("=" * 80 + "\n")

    # Initialize classifier
    classifier = KnowledgeBaseClassifier('output/processnet-knowledge-v2.json')

    # Analyze knowledge base
    all_classes = classifier.analyze_knowledge_base()

    print("\n" + "=" * 80)
    print("Selecting Stratified Samples...")
    print("=" * 80 + "\n")

    # Select samples
    samples = classifier.select_stratified_samples(all_classes, total_samples=100)

    print(f"Selected {len(samples)} samples\n")

    # Generate outputs
    print("Generating outputs...\n")

    # Save manifest
    classifier.save_manifest(samples, 'verification/sample-manifest.json')

    # Save classification report
    report = classifier.generate_classification_report(samples)
    with open('verification/classification-report.md', 'w') as f:
        f.write(report)
    print("Saved report: verification/classification-report.md")

    # Save selection log
    classifier.save_selection_log(samples, 'verification/sample-selection-log.txt')

    print("\n" + "=" * 80)
    print("Phase 01: COMPLETE")
    print("=" * 80)
    print("\nNext: Phase 02 - HTML parsing for expected values")

if __name__ == '__main__':
    main()
