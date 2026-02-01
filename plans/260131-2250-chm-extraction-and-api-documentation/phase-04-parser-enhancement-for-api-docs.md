# Phase 04: Parser Enhancement for API Documentation

## Context
- **Parent Plan:** [plan.md](plan.md)
- **Prerequisite:** Phase 03 complete (HTML structure analyzed)
- **Research:** [researcher-02-api-doc-structure.md](research/researcher-02-api-doc-structure.md)
- **Baseline:** `src/recurdyn-doc-parser.py` (0 methods extracted from tutorial)

## Overview
**Date:** 2026-01-31
**Description:** Enhance parser to extract parameters, return types, and class structure from API documentation
**Priority:** P1 (Core extraction capability)
**Status:** done
**Completed:** 2026-02-01
**Review Status:** Complete - Score 8.5/10

## Key Insights
From research and current parser:
- Current: Only extracts method name (no parameters)
- Missing: Return types, parameter details, class hierarchy
- Data structures have fields but aren't populated
- Need: Enhanced regex patterns, span-based parsing

## Requirements

### Functional
- Extract parameter names and types from signatures
- Parse return types from method signatures
- Extract class definitions and inheritance
- Handle property documentation
- Preserve namespace structure

### Non-Functional
- Maintain backward compatibility
- No performance degradation
- Pass existing test suite

## Architecture

```
Current Parser:
  extract_method_signatures() → extracts name only

Enhanced Parser:
  extract_method_signatures()
    ├── parse_parameters() → extract name, type, default
    ├── parse_return_type() → extract return type
    ├── extract_properties() → handle property syntax
    └── extract_classes() → class hierarchy

Data Structures:
  Parameter: + is_optional, is_out
  Method: + returns, return_description, exceptions, is_static
  ClassDef: + base_classes, implemented_interfaces
```

## Related Code Files

### Files to Modify
- `src/recurdyn-doc-parser.py` - Main parser enhancements

### Files to Use
- `tests/fixtures/html-samples/*.html` - Test fixtures from Phase 03

### Files to Create
- `tests/test_parser_enhancements.py` - New test cases

## Implementation Steps

1. **Update dataclass structures**
   ```python
   @dataclass
   class Parameter:
       name: str
       type: str = ""
       description: str = ""
       default: Optional[str] = None
       is_optional: bool = False      # NEW
       is_out: bool = False           # NEW

   @dataclass
   class Method:
       name: str
       signature: str = ""
       description: str = ""
       parameters: list = field(default_factory=list)
       returns: str = ""              # ENHANCE
       return_description: str = ""   # NEW
       exceptions: list = field(default_factory=list)  # NEW
       is_static: bool = False        # NEW
       access_modifier: str = ""      # NEW
   ```

2. **Add parameter extraction method**
   ```python
   def parse_parameters(self, sig_text: str) -> list:
       """Extract parameters from method signature."""
       # Match: TypeName paramName, TypeName paramName = defaultValue
       # Pattern from research: r'(\w+(?:<[\w\s,]+>)?)\s+(\w+)(?:\s*=\s*([^,)]+))?'
       # Return list of Parameter objects
   ```

3. **Add return type parsing**
   ```python
   def parse_return_type(self, sig_text: str, dt_element) -> tuple:
       """Extract return type from signature or description."""
       # Strategy 1: Parse from <span class="sig-prename">
       # Strategy 2: Extract text before method name
       # Strategy 3: Look for "Returns:" in <dd>
       # Return (type, description)
   ```

4. **Enhance method signature extraction**
   ```python
   def extract_method_signatures(self, soup: BeautifulSoup) -> list:
       """Extract method signatures with parameters and returns."""
       # For each <dt>:
       #   - Extract full signature text
       #   - Parse method name
       #   - Parse parameters via parse_parameters()
       #   - Parse return type via parse_return_type()
       #   - Get description from <dd>
   ```

5. **Add property extraction**
   ```python
   def extract_properties(self, soup: BeautifulSoup) -> list:
       """Extract property definitions."""
       # Look for property patterns:
       #   - PropertyName: PropertyType
       #   - { get; } or { get; set; }
       #   - "read-only" in description
   ```

6. **Add class extraction**
   ```python
   def extract_classes(self, soup: BeautifulSoup) -> list:
       """Extract class definitions with inheritance."""
       # Look for <dl class="class">
       # Parse class name, base classes, inheritance
   ```

7. **Update namespace handling**
   ```python
   def determine_namespace(self, title: str, content: dict) -> str:
       """Enhanced namespace detection."""
       # Detect ProcessNet.Model, ProcessNet.Geometry, etc.
       # Parse from title, file path, or content
   ```

8. **Create new test cases**
   ```python
   # tests/test_parser_enhancements.py
   def test_parameter_extraction():
       """Verify parameter names and types extracted correctly."""

   def test_return_type_extraction():
       """Verify return type parsed from signature."""

   def test_optional_parameters():
       """Verify optional parameters detected."""

   def test_property_read_only_detection():
       """Verify property read-only status."""

   def test_class_hierarchy():
       """Verify inheritance chain captured."""
   ```

9. **Run tests and verify**
   ```bash
   python -m pytest tests/test_parser_enhancements.py -v
   ```

## Todo List

- [x] Update Parameter dataclass with new fields
- [x] Update Method dataclass with new fields
- [x] Implement parse_parameters() method
- [x] Implement parse_return_type() method
- [x] Enhance extract_method_signatures()
- [x] Implement extract_properties() method
- [x] Implement extract_classes() method
- [x] Update determine_namespace() method
- [x] Create test_parser_enhancements.py
- [x] Run tests and fix failures

## Success Criteria
- Parameters extracted with name and type
- Return types captured for methods
- Properties extracted with read-only flag
- Class definitions include inheritance
- All new tests pass
- Existing tests still pass

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| HTML structure differs from Phase 03 | Medium | High | Use defensive parsing, fallback patterns |
| Complex parameter types break regex | Medium | Medium | Use iterative parsing, handle edge cases |
| Performance degradation | Low | Medium | Benchmark before/after, optimize if needed |
| Breaking existing functionality | Low | High | Run existing test suite first |

## Security Considerations
- Input validation for regex patterns
- Handle malformed HTML gracefully
- No code execution from parsed content

## Completion Summary

### Status: DONE (2026-02-01)

**Implementation:** All 10 core tasks completed
- Parameter/return type extraction ✓
- Property/class extraction ✓
- Namespace detection ✓
- Test suite: 9/9 passed ✓

**Code Review:** 8.5/10
- Excellent backward compatibility
- Strong test coverage (100% pass rate)
- YAGNI/KISS/DRY compliant
- 3 high-priority items identified (see review)

**Files Modified:**
- `src/recurdyn-doc-parser.py` (~600 lines added/modified)
- `tests/test-sphinx-parser-enhancement-parameter-property-class-extraction.py` (245 lines)

**Known Issues (Pre-Phase 05):**
1. Properties extracted but not stored in KB structure
2. Regex complexity in parameter parsing (DoS risk)
3. Missing description truncation safety

## Next Steps
- Proceed to [Phase 05: Re-extraction](phase-05-run-enhanced-parser-on-api-docs.md)
- Run enhanced parser on full API documentation
- Address H1-H3 findings from code review
