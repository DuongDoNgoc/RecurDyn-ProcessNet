# Main Plan Integration Changes

**Target:** `plans/260128-processnet-extraction/plan.md`

## Changes Required

### 1. Add Phase 3.5: Sample Verification

Insert after Phase 3 (HTML Parser Implementation):

```markdown
### Phase 3.5: Sample Verification
**Status:** Pending
**Files:** `tests/test-sample-extraction.py`

Tasks:
1. Select 5 representative HTML files (index, namespace, class, methods, examples)
2. Run sample extraction with parser
3. Validate extraction accuracy:
   - Title extraction matches expected
   - Namespace detection correct
   - Method count within ±20% tolerance
   - At least one signature exactly matches
4. Adjust parser if discrepancies found
5. Re-test until sample validation passes

**Success Criteria:**
- All 5 file types parse successfully
- Method counts within tolerance
- No critical extraction failures
```

### 2. Expand Phase 6: Validation & Testing

Replace existing Phase 6 content with:

```markdown
### Phase 6: Validation & Testing
**Status:** Pending
**Files:** `tests/*.py`

**Test Files:**
- `tests/conftest.py` - Shared fixtures
- `tests/test-sample-extraction.py` - Sample file validation
- `tests/test-parser-adjustments.py` - Parser regression tests
- `tests/test-spot-checks.py` - Random spot-check validation
- `tests/test-use-case-coverage.py` - Use case method tests

**Tasks:**
1. Setup pytest infrastructure with fixtures
2. Validate parsing success rate (>98% target)
3. Test query interface accuracy
4. Run spot-check validation on 10 random files
5. Verify use case coverage:
   - UC-1: DOE batch execution methods (Load, Clone, SetParameter, Run, SaveAs)
   - UC-2: Model introspection methods (GetAllBodies, GetAllJoints, GetEntityByID)
   - UC-3: Result processing methods (Result.Load, GetTimeArray, Export)
6. Generate extraction statistics report

**Success Metrics:**
| Metric | Threshold |
|--------|-----------|
| Parsing success rate | ≥98% |
| Method extraction accuracy | ≥90% |
| Example extraction accuracy | ≥85% |
| Spot-check pass rate | ≥85% |
| Use case method coverage | 100% |
```

### 3. Update Success Criteria

Replace existing success criteria with:

```markdown
## Success Criteria

- [ ] >98% HTML files successfully parsed
- [ ] All namespaces identified from documentation
- [ ] Method signatures extracted with >90% accuracy
- [ ] Query interface returns correct results
- [ ] Markdown output is readable and well-formatted
- [ ] Sample verification (5 files) passes all checks
- [ ] Spot-check validation (10 files) ≥85% pass rate
- [ ] All use case methods found (DOE, Model, Result)
- [ ] pytest suite runs without failures
```

### 4. Update File Structure

Add to file structure section:

```
├── tests/
│   ├── conftest.py
│   ├── test-sample-extraction.py
│   ├── test-parser-adjustments.py
│   ├── test-spot-checks.py
│   ├── test-use-case-coverage.py
│   └── fixtures/
│       └── sample-html/
```

### 5. Add Testing Dependencies

Add to Dependencies section:

```markdown
**Testing:**
- pytest (test framework)
- pytest-cov (coverage reporting)
- pytest-playwright (browser testing)

**MCP Integration:**
- @anthropic/mcp-server-playwright (browser automation)
- playwright browsers (chromium)
```

### 6. Add MCP Configuration

Create `.mcp/servers.json`:

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@anthropic/mcp-server-playwright"]
  }
}
```

## Integration Verification

After applying changes, verify:
1. Phase numbering is consistent (3.5 between 3 and 4)
2. All test files referenced exist or are planned
3. Success criteria are measurable
4. Use case method lists match PDR requirements
