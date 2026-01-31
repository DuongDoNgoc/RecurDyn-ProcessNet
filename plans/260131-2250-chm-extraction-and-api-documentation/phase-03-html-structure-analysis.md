# Phase 03: HTML Structure Analysis

## Context
- **Parent Plan:** [plan.md](plan.md)
- **Prerequisite:** Phase 02 complete (HTML files in WSL)
- **Research:** [researcher-02-api-doc-structure.md](research/researcher-02-api-doc-structure.md)

## Overview
**Date:** 2026-01-31
**Description:** Analyze extracted HTML to determine actual structure and patterns for parser enhancement
**Priority:** P1 (Critical - parser enhancement depends on this)
**Status:** pending
**Review Status:** Not started

## Key Insights
From research:
- Current parser assumes Sphinx DL/DT/DD structure
- Need to verify actual class names and HTML patterns
- Unknown: Method signature format, parameter documentation style
- Create test fixtures for regression testing

## Requirements

### Functional
- Sample 5-10 representative HTML files
- Document actual HTML structure patterns
- Identify method signature, parameter, return type formats
- Create test fixtures for parser enhancement

### Non-Functional
- Analysis completes in <30 minutes
- Results documented in report

## Architecture

```
Sample Files:
  ├── Namespace doc: ProcessNet.Model.html
  ├── Class doc: Body.html, Geometry.html
  ├── Method doc: CreateArc.html, GetAllBodies.html
  └── Example doc: Tutorial.html

Analysis Output:
  ├── HTML structure patterns (class/ID names)
  ├── Method signature format
  ├── Parameter documentation style
  ├── Return type presentation
  └── Test fixtures for regression tests
```

## Related Code Files

### Files to Use
- `src/recurdyn-doc-parser.py` - Current parser implementation
- `knowledge/extracted_chm/*.html` - Source files

### Files to Create
- `tests/fixtures/html-samples/` - Sample HTML for testing
- `reports/parser-analysis-report.md` - Analysis findings

## Implementation Steps

1. **List all extracted HTML files**
   ```bash
   find knowledge/extracted_chm -name "*.html" -type f | sort
   ```

2. **Select representative samples**
   - Look for files with API-related names
   - Target: 5-10 files covering different patterns
   ```bash
   # Find API-related files
   find knowledge/extracted_chm -name "*.html" | grep -iE "(class|method|interface|api)" | head -10
   ```

3. **Analyze HTML structure**
   For each sample file:
   ```bash
   # Examine HTML structure
   cat knowledge/extracted_chm/sample.html | head -100

   # Look for method patterns
   grep -o '<dt[^>]*class="[^"]*"' knowledge/extracted_chm/sample.html | sort | uniq

   # Find all class attributes
   grep -o 'class="[^"]*"' knowledge/extracted_chm/sample.html | sort | uniq
   ```

4. **Document method signature patterns**
   - Extract a few example `<dt>` blocks
   - Identify parameter format (inline, nested, separate)
   - Check for return type indicators
   ```bash
   # Extract definition terms
   grep -A 5 '<dt' knowledge/extracted_chm/sample.html | head -50
   ```

5. **Document parameter documentation**
   - Check if parameters in nested `<dl>`
   - Look for parameter tables
   - Identify description patterns

6. **Create test fixtures**
   ```bash
   mkdir -p tests/fixtures/html-samples
   cp knowledge/extracted_chm/sample1.html tests/fixtures/html-samples/
   cp knowledge/extracted_chm/sample2.html tests/fixtures/html-samples/
   # ... copy representative samples
   ```

7. **Generate analysis report**
   Create `reports/parser-analysis-report.md` with:
   - File list analyzed
   - HTML class/ID patterns found
   - Method signature format
   - Parameter documentation style
   - Return type presentation
   - Code example format
   - Recommended parser enhancements

## Todo List

- [ ] List all extracted HTML files
- [ ] Select 5-10 representative samples
- [ ] Analyze HTML structure (classes, IDs)
- [ ] Document method signature patterns
- [ ] Document parameter documentation style
- [ ] Document return type presentation
- [ ] Create test fixtures from samples
- [ ] Generate analysis report

## Success Criteria
- 5-10 sample files analyzed
- HTML patterns documented (class names, structure)
- Method signature format identified
- Parameter format identified
- Test fixtures created
- Analysis report generated

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| No HTML files found | Very Low | High | Verify Phase 02 completed |
| HTML structure varies wildly | Medium | High | Sample more files, find common patterns |
| No method signatures found | Low | High | Check for alternative structures (tables) |
| Cannot determine pattern | Low | Medium | Assume generic fallback patterns |

## Security Considerations
- Read-only analysis (no modifications)
- No external dependencies

## Next Steps
- Proceed to [Phase 04: Parser Enhancement](phase-04-parser-enhancement-for-api-docs.md)
- Use analysis results to update parser

## Expected Output Structure

Based on research, expected patterns:

```html
<!-- Method signature -->
<dt class="sig sig-object py">
    <span class="sig-prename">ReturnType</span>
    <span class="sig-name">MethodName</span>
    <span class="sig-paren">(</span>
    <span class="sig-param">ParamType paramName</span>
    <span class="sig-paren">)</span>
</dt>
<dd>Method description</dd>
```

**Note:** Actual structure may differ - analysis will confirm.
