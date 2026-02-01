---
phase: 04
title: "Parser Bug Fixes - Method/Property to Class Association"
status: pending
effort: 2h
depends_on: [phase-03]
---

# Phase 04: Parser Bug Fixes - Method/Property to Class Association

## Context

- **Plan**: [plan.md](./plan.md)
- **Source**: `src/recurdyn-doc-parser.py`
- **Bug Location**: `build_knowledge_base()` lines 783-903

## Overview

Fix three parser bugs to correctly associate methods and properties with their parent classes.

## Bug Analysis

### Bug #1: Methods Not Populated in ClassDef

**Current Code (lines 855-866):**
```python
if content['methods']:
    for method in content['methods']:
        method_dict = asdict(method)
        ns_data['standalone_methods'].append(method_dict)  # WRONG: Goes to namespace
```

**Expected Behavior:** Methods should populate `class.methods[]` when associated with a class.

### Bug #2: Properties Not Populated in ClassDef

**Current Code (lines 836-845):**
```python
if content['properties']:
    for prop in content['properties']:
        prop_dict = asdict(prop)
        ns_data['properties'].append(prop_dict)  # WRONG: Goes to namespace
```

**Expected Behavior:** Properties should populate `class.properties[]` when associated with a class.

### Bug #3: Missing File-Based Association Logic

HTML naming convention: `ClassName_MethodName.html` or `ClassName.html`
This convention should be used to associate methods/properties with classes.

## Implementation Steps

### Step 1: Add Class-Member Association Logic

Add to `build_knowledge_base()` after line 880:

```python
def _associate_members_with_classes(self, ns_data: dict, file_path: str):
    """Associate methods/properties with their parent classes based on file naming."""
    rel_path = str(file_path.name)  # e.g., "IApplication_GetModel.html"

    # Pattern: ClassName_MemberName.html or ClassName.MemberName.html
    if '_' in rel_path or '.' in rel_path.replace('.html', ''):
        parts = rel_path.replace('.html', '').replace('.', '_').split('_')
        if len(parts) >= 2:
            class_name = parts[0]

            # Find matching class in namespace
            for cls in ns_data['classes']:
                if cls['name'].lower() == class_name.lower():
                    # Associate methods from this file
                    for method in ns_data['standalone_methods']:
                        if method.get('source_file', '').endswith(rel_path):
                            if method not in cls['methods']:
                                cls['methods'].append(method)

                    # Associate properties from this file
                    for prop in ns_data.get('properties', []):
                        if prop.get('source_file', '').endswith(rel_path):
                            if prop not in cls['properties']:
                                cls['properties'].append(prop)
                    break
```

### Step 2: Enhance parse_html_file for Class Context

Modify `parse_html_file()` to detect class context from HTML:

```python
def _detect_parent_class(self, soup: BeautifulSoup, file_path: Path) -> str:
    """Detect parent class from HTML content or file name."""
    # Method 1: Check for class breadcrumb
    breadcrumb = soup.find('li', class_='breadcrumb-item')
    if breadcrumb:
        link = breadcrumb.find('a')
        if link and link.get('href', '').endswith('.html'):
            return link.get_text(strip=True)

    # Method 2: Extract from file name
    name = file_path.stem  # e.g., "IApplication_GetModel"
    if '_' in name:
        return name.split('_')[0]

    return ""
```

### Step 3: Add Rubric+Table Pairing with find_next()

For autosummary tables, use sibling navigation:

```python
def _extract_autosummary_with_context(self, soup: BeautifulSoup):
    """Extract autosummary tables with rubric context."""
    results = {'methods': [], 'properties': []}

    for rubric in soup.find_all('p', class_='rubric'):
        rubric_text = rubric.get_text(strip=True).lower()

        # Find next sibling table
        table = rubric.find_next('table', class_=lambda x: x and 'autosummary' in str(x))
        if not table:
            continue

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 2:
                name = cells[0].get_text(strip=True)
                desc = cells[1].get_text(strip=True)

                if 'method' in rubric_text:
                    results['methods'].append({'name': name, 'description': desc})
                elif 'propert' in rubric_text or 'attribute' in rubric_text:
                    results['properties'].append({'name': name, 'description': desc})

    return results
```

### Step 4: Add CSS Attribute Selectors

Use attribute selectors for autosummary tables:

```python
# In extract_method_signatures or new method
autosummary_tables = soup.select('table[class*="autosummary"]')
for table in autosummary_tables:
    # Process table rows...
```

### Step 5: Create Unit Tests

File: `tests/test-parser-class-member-association.py`

```python
import pytest
from src.recurdyn_doc_parser import ProcessNetDocParser

class TestClassMemberAssociation:
    def test_method_associated_with_class(self, parser, sample_html):
        """Methods should appear in class.methods[]."""
        result = parser.parse_html_file(sample_html)
        # Verify methods are in class
        for cls in result['classes']:
            assert len(cls.methods) > 0 or cls.name in ['EmptyClass']

    def test_property_associated_with_class(self, parser, sample_html):
        """Properties should appear in class.properties[]."""
        result = parser.parse_html_file(sample_html)
        for cls in result['classes']:
            if 'Property' in str(sample_html):
                assert len(cls.properties) > 0

    def test_file_naming_association(self, parser):
        """File IApplication_GetModel.html associates GetModel with IApplication."""
        # Test file-based association logic
        pass
```

## Success Criteria

- [ ] Methods populate ClassDef.methods[]
- [ ] Properties populate ClassDef.properties[]
- [ ] File-based association working
- [ ] Autosummary table parsing enhanced
- [ ] All existing tests still pass
- [ ] New unit tests pass

## Output Artifacts

- Modified `src/recurdyn-doc-parser.py`
- New test file `tests/test-parser-class-member-association.py`

## Risks

| Risk | Mitigation |
|------|------------|
| Regression in existing extraction | Run full test suite before/after |
| Incorrect associations | Validate with spot check samples |
| Performance impact | Measure extraction time |
