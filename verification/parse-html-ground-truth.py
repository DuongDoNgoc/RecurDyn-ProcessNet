#!/usr/bin/env python3
"""
HTML Ground Truth Parser for Phase 02
Extracts actual methods/properties from HTML files to populate expected values.
Implements fixes from researcher report: rubric+table pairing, CSS attribute selectors.
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class HTMLGroundTruth:
    """Ground truth extracted from HTML."""
    methods: List[Dict[str, str]]
    properties: List[Dict[str, str]]
    complexity: str
    html_pattern: str

class HTMLGroundTruthParser:
    def __init__(self, html_base_path: str = "output/extracted_chm"):
        self.html_base = Path(html_base_path)

    def parse_file(self, relative_path: str) -> HTMLGroundTruth:
        """Parse HTML file and extract ground truth."""
        file_path = self.html_base / relative_path

        if not file_path.exists():
            print(f"WARNING: File not found: {file_path}")
            return HTMLGroundTruth([], [], 'unknown', 'not_found')

        # Read and parse HTML
        with open(file_path, 'rb') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'lxml')

        # Extract methods and properties using rubric+table pairing
        methods = self._extract_members_by_rubric(soup, "Methods")
        properties = self._extract_members_by_rubric(soup, "Properties")

        # Classify complexity based on member count
        total_members = len(methods) + len(properties)
        if total_members == 0:
            complexity = 'simple'
        elif total_members <= 5:
            complexity = 'simple'
        elif total_members <= 15:
            complexity = 'medium'
        else:
            complexity = 'complex'

        # Determine HTML pattern
        html_pattern = self._determine_html_pattern(soup, methods, properties)

        return HTMLGroundTruth(methods, properties, complexity, html_pattern)

    def _extract_members_by_rubric(self, soup: BeautifulSoup, rubric_text: str) -> List[Dict[str, str]]:
        """
        Extract members (methods/properties) using rubric+table pairing.
        Implements fix: Use .find_next() for sibling navigation.
        """
        members = []

        # Find rubric paragraph with exact text match
        rubrics = soup.find_all('p', class_='rubric')

        for rubric in rubrics:
            if rubric.get_text(strip=True) == rubric_text:
                # Find next table after rubric (sibling navigation)
                # Use CSS attribute selector for multi-class tables
                table = rubric.find_next('table')

                if table and 'autosummary' in table.get('class', []):
                    members = self._parse_autosummary_table(table)
                    break

        return members

    def _parse_autosummary_table(self, table) -> List[Dict[str, str]]:
        """
        Parse autosummary table to extract member names and descriptions.
        Implements fix: Handle multi-class tables, normalize text.
        """
        members = []

        # Find tbody (explicit separation as recommended)
        tbody = table.find('tbody')
        if not tbody:
            return members

        rows = tbody.find_all('tr')

        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # First cell: member name (inside <code> tag)
                name_cell = cells[0]
                code_tag = name_cell.find('code')
                name = code_tag.get_text(strip=True) if code_tag else name_cell.get_text(strip=True)

                # Second cell: description
                desc_cell = cells[1]
                # Get first <p> tag inside cell, or cell text directly
                p_tag = desc_cell.find('p')
                description = p_tag.get_text(strip=True) if p_tag else desc_cell.get_text(strip=True)

                members.append({
                    'name': name,
                    'description': description
                })

        return members

    def _determine_html_pattern(self, soup: BeautifulSoup, methods: List, properties: List) -> str:
        """Determine which HTML pattern is used in this file."""
        # Check for rubric+table pattern
        rubrics = soup.find_all('p', class_='rubric')
        if rubrics:
            return 'rubric_table'

        # Check for field-list pattern
        field_lists = soup.find_all('dl', class_='field-list')
        if field_lists:
            return 'field_list'

        # Check for definition-list pattern
        dl_methods = soup.find_all('dl', class_='py method')
        dl_properties = soup.find_all('dl', class_='py property')
        if dl_methods or dl_properties:
            return 'definition_list'

        # Default pattern
        return 'unknown'

def update_manifest_with_ground_truth(manifest_path: str, output_path: str):
    """Update sample manifest with ground truth expected values."""
    # Load manifest
    with open(manifest_path) as f:
        manifest = json.load(f)

    parser = HTMLGroundTruthParser()

    print(f"Processing {len(manifest['samples'])} samples...")
    print("=" * 80)

    stats = {
        'total_samples': 0,
        'files_found': 0,
        'files_not_found': 0,
        'total_methods': 0,
        'total_properties': 0,
        'by_complexity': {'simple': 0, 'medium': 0, 'complex': 0, 'unknown': 0},
        'by_pattern': {}
    }

    # Process each sample
    for i, sample in enumerate(manifest['samples'], 1):
        print(f"[{i}/{len(manifest['samples'])}] {sample['class_name']}", end=' ... ')

        # Parse HTML
        ground_truth = parser.parse_file(sample['file'])

        # Update sample
        sample['expected_methods'] = len(ground_truth.methods)
        sample['expected_properties'] = len(ground_truth.properties)
        sample['complexity'] = ground_truth.complexity
        sample['html_pattern'] = ground_truth.html_pattern
        sample['methods_list'] = [m['name'] for m in ground_truth.methods]
        sample['properties_list'] = [p['name'] for p in ground_truth.properties]

        # Update stats
        stats['total_samples'] += 1
        if ground_truth.html_pattern != 'not_found':
            stats['files_found'] += 1
        else:
            stats['files_not_found'] += 1

        stats['total_methods'] += len(ground_truth.methods)
        stats['total_properties'] += len(ground_truth.properties)
        stats['by_complexity'][ground_truth.complexity] += 1

        pattern = ground_truth.html_pattern
        stats['by_pattern'][pattern] = stats['by_pattern'].get(pattern, 0) + 1

        print(f"M:{len(ground_truth.methods)} P:{len(ground_truth.properties)} [{ground_truth.complexity}]")

    print("=" * 80)
    print("\nStatistics:")
    print(f"  Files found: {stats['files_found']}/{stats['total_samples']}")
    print(f"  Total methods: {stats['total_methods']}")
    print(f"  Total properties: {stats['total_properties']}")
    print(f"\nComplexity distribution:")
    for complexity, count in sorted(stats['by_complexity'].items()):
        print(f"  {complexity}: {count}")
    print(f"\nHTML pattern distribution:")
    for pattern, count in sorted(stats['by_pattern'].items()):
        print(f"  {pattern}: {count}")

    # Update metadata
    manifest['metadata']['ground_truth_extracted'] = True
    manifest['metadata']['extraction_date'] = '2026-02-01'
    manifest['metadata']['stats'] = stats

    # Save updated manifest
    with open(output_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\n✅ Updated manifest saved: {output_path}")

    return stats

def main():
    print("=" * 80)
    print("Phase 02: HTML Ground Truth Extraction")
    print("=" * 80 + "\n")

    # Update manifest with ground truth
    stats = update_manifest_with_ground_truth(
        'verification/sample-manifest.json',
        'verification/sample-manifest-with-ground-truth.json'
    )

    print("\n" + "=" * 80)
    print("Phase 02: COMPLETE")
    print("=" * 80)
    print("\nNext: Phase 03 - Verification (compare extracted vs ground truth)")

if __name__ == '__main__':
    main()
