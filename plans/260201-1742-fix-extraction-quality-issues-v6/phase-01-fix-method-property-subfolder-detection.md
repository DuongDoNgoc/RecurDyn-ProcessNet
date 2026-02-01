# Phase 01: Fix Method/Property Subfolder Detection

## Context Links
- Parent: [plan.md](./plan.md)
- Parser: `src/recurdyn-doc-parser.py`
- Journal: `docs/journals/260201-knowledge-base-extraction-journey-v3-through-v5-iteration.md`

## Overview
- **Priority:** P0 (Critical)
- **Status:** completed
- **Description:** Prevent method/property HTML files from creating standalone class entries

## Key Insights

From spot check analysis:
- File `Python/Professional/IApplication/Methods/IApplication_NewModelDocumentWithUnitSystem.html` creates class `IApplication_NewModelDocumentWithUnitSystem` instead of being method of `IApplication`
- The `_associate_members_with_classes()` method creates NEW class if parent not found
- Method files in `/Methods/` subfolders should NEVER create class entries

## Requirements

### Functional
1. Detect if file path contains `/Methods/` or `/Properties/`
2. If method/property file: extract as member, don't create class
3. Associate member with existing parent class only
4. If parent class doesn't exist, log warning but don't create fake class

### Non-Functional
- No performance regression (still <5 min for 40K files)
- Backward compatible JSON structure

## Architecture

```
File: Python/Professional/IApplication/Methods/IApplication_NewModelDocumentWithUnitSystem.html
                          ↓
                Is path contains /Methods/ or /Properties/?
                          ↓ YES
                Extract parent class from path: IApplication
                          ↓
                Find existing IApplication class in knowledge base
                          ↓
                Add method to IApplication.methods[]
                          ↓
                DON'T add to standalone_methods[]
                DON'T create new class entry
```

## Related Code Files

### Modify
- `src/recurdyn-doc-parser.py`:
  - `_extract_class_name_from_filename()` - add subfolder detection
  - `_associate_members_with_classes()` - skip class creation for member files
  - `build_knowledge_base()` - add member file handling

## Implementation Steps

1. Add method `_is_member_file(file_path)` to detect `/Methods/` or `/Properties/` in path
2. Add method `_extract_parent_class_from_path(file_path)` to get class name from directory structure
3. Modify `_associate_members_with_classes()`:
   - Remove class creation logic for member files
   - Only associate with EXISTING classes
4. Modify `build_knowledge_base()`:
   - Process class definition files FIRST (to ensure classes exist)
   - Then process member files (to associate with existing classes)
5. Update stats tracking to distinguish member file processing

## Todo List

- [ ] Add `_is_member_file()` detection method
- [ ] Add `_extract_parent_class_from_path()` method
- [ ] Modify `_associate_members_with_classes()` to not create classes for member files
- [ ] Reorder file processing: class files first, then member files
- [ ] Add logging for unassociated members (parent class not found)
- [ ] Test with IApplication method files

## Success Criteria

- [ ] Files in `/Methods/` do NOT create class entries
- [ ] Methods are added to existing parent class only
- [ ] No `IApplication_NewModelDocumentWithUnitSystem` class in output
- [ ] `IApplication.methods[]` contains `NewModelDocumentWithUnitSystem`

## Risk Assessment

- **Risk:** Some member files may not have parent class defined
- **Mitigation:** Log warnings for orphaned members, collect for review

## Security Considerations
- N/A (local file processing only)

## Next Steps
- After this phase: Phase 02 (enum member extraction)
