# Phase 02: Add Enum Member Table Extraction

## Context Links
- Parent: [plan.md](./plan.md)
- Depends on: [Phase 01](./phase-01-fix-method-property-subfolder-detection.md)
- Parser: `src/recurdyn-doc-parser.py`

## Overview
- **Priority:** P1 (High)
- **Status:** completed
- **Description:** Extract enum member values from HTML tables

## Key Insights

From spot check:
```html
<!-- Enum member table in RFlexMassInvariantType.html -->
<table class="docutils align-default">
<tbody>
<tr><td><p>RFlexMassInvariantType_Full</p></td><td><p>1</p></td></tr>
<tr><td><p>RFlexMassInvariantType_Partial</p></td><td><p>0</p></td></tr>
</tbody>
</table>
```

Current parser extracts 0 properties. Should extract 2 enum members with values.

## Requirements

### Functional
1. Detect enum pages (class with `IntEnum` base or enum keyword)
2. Find enum member tables (`<table class="docutils">` near enum definition)
3. Extract member name and value from table rows
4. Add as properties with `default` field containing integer value

### Non-Functional
- Handle missing value column gracefully
- Skip non-enum tables (method parameter tables, etc.)

## Architecture

```
HTML: <table class="docutils">
        <tr><td>EnumName_Value1</td><td>1</td></tr>
        <tr><td>EnumName_Value2</td><td>0</td></tr>
      </table>
                    ↓
            Is parent class an enum? (Bases: IntEnum)
                    ↓ YES
            Extract rows as properties:
              - name: "Value1"
              - type: "int"
              - default: "1"
```

## Related Code Files

### Modify
- `src/recurdyn-doc-parser.py`:
  - Add `extract_enum_members()` method
  - Modify `extract_sphinx_classes()` to detect enums
  - Call enum extraction for enum classes

## Implementation Steps

1. Add `_is_enum_class(soup, class_def)` detection method
   - Check for `IntEnum` in inheritance
   - Check for "enum" keyword in class definition
2. Add `extract_enum_members(soup)` method
   - Find `<table class="docutils">` tables
   - Filter to tables after class definition
   - Extract name/value pairs from rows
3. Modify `extract_sphinx_classes()`:
   - After extracting class, check if enum
   - If enum, call `extract_enum_members()` and add to properties
4. Handle edge cases:
   - Tables without value column → use member name only
   - Multiple tables → pick one closest to class definition

## Todo List

- [ ] Add `_is_enum_class()` detection
- [ ] Add `extract_enum_members()` method
- [ ] Integrate enum extraction into class parsing
- [ ] Test with `RFlexMassInvariantType.html`
- [ ] Verify enum members appear as properties with values

## Success Criteria

- [ ] `RFlexMassInvariantType` has 2 properties (was 0)
- [ ] Property `RFlexMassInvariantType_Full` has default=1
- [ ] Property `RFlexMassInvariantType_Partial` has default=0
- [ ] All enums have at least 1 member property

## Risk Assessment

- **Risk:** Non-enum tables may be misidentified as enum members
- **Mitigation:** Only extract from tables within enum class pages

## Next Steps
- After this phase: Phase 03 (relationship validation)
