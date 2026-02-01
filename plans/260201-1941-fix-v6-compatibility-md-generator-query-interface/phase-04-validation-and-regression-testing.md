---
phase: 04
title: "Validation and Regression Testing"
status: pending
effort: 15m
parallel: false
depends_on: [01, 02, 03]
---

# Phase 04: Validation and Regression Testing

## Context

Final validation to ensure all fixes work correctly and no regressions introduced.

## Validation Checklist

### 1. Markdown Generator Validation

```bash
# Generate markdown
python3 src/recurdyn-doc-parser.py \
    -i knowledge \
    -o output/processnet-knowledge-v6-test.json \
    -m output/markdown-v6-test

# Check output
cat output/markdown-v6-test/ProcessNet.md | head -50
```

**Expected:**
- `**Classes:** 51`
- `**Methods:** 2244`
- `**Examples:** 887`
- Classes section with methods grouped by class

### 2. Query Interface Validation

```bash
# Test search
python3 src/processnet-query-interface.py \
    --kb output/processnet-knowledge-v6.json \
    --search "CreateBody"

# Expected: Results found

# Test find
python3 src/processnet-query-interface.py \
    --kb output/processnet-knowledge-v6.json \
    --find "NewModelDocumentWithUnitSystem"

# Expected: Method found with signature
```

### 3. API Server Validation

```bash
# Start server
python3 src/processnet-api-server.py --kb output/processnet-knowledge-v6.json &

# Wait for startup
sleep 3

# Test stats endpoint
curl -s http://127.0.0.1:8000/api/stats | jq .

# Expected: methods: 2244

# Test search endpoint
curl -s "http://127.0.0.1:8000/api/search?q=Create&limit=5" | jq .

# Expected: Results with methods

# Stop server
pkill -f processnet-api-server
```

### 4. Test Suite Validation

```bash
# Run all tests
pytest tests/ -v --tb=short 2>&1 | tail -30

# Expected: All tests pass
```

### 5. Statistics Verification Script

```python
#!/usr/bin/env python3
"""Validate v6 KB compatibility fixes."""

import json
import sys
sys.path.insert(0, 'src')

from pathlib import Path

# Load KB
kb_path = Path('output/processnet-knowledge-v6.json')
with open(kb_path) as f:
    kb = json.load(f)

# Count methods from classes
ns = kb['namespaces']['ProcessNet']
total_methods = sum(len(c.get('methods', [])) for c in ns.get('classes', []))

print(f"Classes: {len(ns.get('classes', []))}")
print(f"Methods in classes: {total_methods}")
print(f"Standalone methods: {len(ns.get('standalone_methods', []))}")
print(f"Examples: {len(ns.get('examples', []))}")

# Verify
assert len(ns.get('classes', [])) == 51, "Expected 51 classes"
assert total_methods == 2244, f"Expected 2244 methods, got {total_methods}"
assert len(ns.get('standalone_methods', [])) == 0, "standalone_methods should be empty"

print("\n[OK] All validations passed!")
```

## Success Criteria

| Criterion | Status |
|-----------|--------|
| Markdown shows 2,244 methods | [ ] |
| Markdown groups methods by class | [ ] |
| Query interface returns search results | [ ] |
| API server /stats shows 2,244 methods | [ ] |
| All tests pass | [ ] |
| No regressions in existing functionality | [ ] |

## Rollback Plan

If validation fails:

```bash
# Revert all changes
git checkout src/recurdyn-doc-parser.py
git checkout src/processnet-query-interface.py
git checkout tests/
```

## Next Steps After Validation

1. Commit changes with message: "fix(parser): update markdown generator and query interface for v6 KB compatibility"
2. Update documentation if needed
3. Close related issues
