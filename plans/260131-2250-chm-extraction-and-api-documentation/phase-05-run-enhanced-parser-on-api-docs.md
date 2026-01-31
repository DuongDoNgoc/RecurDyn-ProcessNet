# Phase 05: Run Enhanced Parser on API Documentation

## Context
- **Parent Plan:** [plan.md](plan.md)
- **Prerequisite:** Phase 04 complete (parser enhanced)
- **Baseline:** Previous run: 0 methods extracted from tutorial

## Overview
**Date:** 2026-01-31
**Description:** Execute enhanced parser on extracted CHM HTML to build complete ProcessNet knowledge base
**Priority:** P1 (Main extraction output)
**Status:** pending
**Review Status:** Not started

## Key Insights
- Tutorial HTML contained 0 methods (not API documentation)
- CHM extraction should contain actual API docs
- Target: Extract 100+ methods with full signatures
- Expected file count: 50-500 HTML files

## Requirements

### Functional
- Process all HTML files from extracted CHM
- Extract methods with parameters and return types
- Extract class definitions and properties
- Extract code examples
- Generate JSON knowledge base
- Generate markdown documentation

### Non-Functional
- Processing time <10 minutes for 500 files
- Memory usage <1 GB
- Parse success rate >80%
- No crashes on malformed HTML

## Architecture

```
Input:
  knowledge/extracted_chm/*.html
    ├── ProcessNet.Model.Body.html
    ├── ProcessNet.Geometry.Arc.html
    └── ...

Parser:
  src/recurdyn-doc-parser.py (enhanced)
    ├── discover_files() → find all HTML
    ├── parse_html_file() → extract content
    │   ├── extract_method_signatures() → methods + params + returns
    │   ├── extract_classes() → class definitions
    │   ├── extract_properties() → properties
    │   └── extract_code_blocks() → examples
    └── build_knowledge_base() → aggregate

Output:
  output/processnet-knowledge.json
    ├── namespaces (ProcessNet.Model, ProcessNet.Geometry, ...)
    ├── method_index
    ├── class_index
    └── interface_index
  output/markdown/*.md
```

## Related Code Files

### Files to Use
- `src/recurdyn-doc-parser.py` - Enhanced parser
- `knowledge/extracted_chm/` - Input HTML files

### Files to Create
- `output/processnet-knowledge.json` - Knowledge base
- `output/markdown/` - Markdown documentation
- `reports/extraction-results.md` - Results summary

## Implementation Steps

1. **Verify input files**
   ```bash
   # Count HTML files
   find knowledge/extracted_chm -name "*.html" | wc -l

   # List sample files
   find knowledge/extracted_chm -name "*.html" | head -20

   # Check file sizes
   du -sh knowledge/extracted_chm/
   ```

2. **Backup existing output (if any)**
   ```bash
   mv output/processnet-knowledge.json output/processnet-knowledge.json.bak 2>/dev/null || true
   ```

3. **Run parser with verbose logging**
   ```bash
   cd /mnt/d/Vibecoding/RecurDyn-ProcessNet
   python src/recurdyn-doc-parser.py \
       --input knowledge/extracted_chm \
       --output output/processnet-knowledge.json \
       --markdown output/markdown \
       --verbose
   ```

4. **Monitor extraction progress**
   - Watch for errors in logs
   - Note file processing percentage
   - Check for encoding warnings

5. **Verify output quality**
   ```bash
   # Check JSON validity
   python -m json.tool output/processnet-knowledge.json > /dev/null

   # Check statistics
   cat output/processnet-knowledge.json | jq '.metadata'
   cat output/processnet-knowledge.json | jq '.namespaces.ProcessNet | {methods: (.standalone_methods | length), examples: (.examples | length)}'

   # Sample a method entry
   cat output/processnet-knowledge.json | jq '.namespaces.ProcessNet.standalone_methods[0]'
   ```

6. **Verify markdown generation**
   ```bash
   # List generated markdown files
   ls -la output/markdown/

   # Check a sample markdown file
   head -50 output/markdown/ProcessNet.md
   ```

7. **Generate extraction report**
   Create `reports/extraction-results.md` with:
   - Total files processed
   - Methods extracted (count)
   - Classes extracted (count)
   - Properties extracted (count)
   - Code examples extracted (count)
   - Parse success rate
   - Processing time
   - Sample output (5-10 method examples)
   - Issues encountered

8. **Query interface verification**
   ```bash
   # Test query interface
   python src/processnet-query-interface.py --search "Body"
   python src/processnet-query-interface.py --find "CreateArc"
   python src/processnet-query-interface.py --examples
   python src/processnet-query-interface.py --stats
   ```

## Todo List

- [ ] Verify input HTML files exist
- [ ] Backup existing output
- [ ] Run enhanced parser with verbose logging
- [ ] Monitor extraction for errors
- [ ] Verify JSON output validity
- [ ] Check extraction statistics
- [ ] Verify markdown generation
- [ ] Test query interface
- [ ] Generate extraction results report

## Success Criteria

### Minimum Viable
- >50 methods extracted
- >60% methods have parameter info
- JSON output is valid
- Query interface returns results
- No crashes during extraction

### Optimal
- >100 methods extracted
- >80% methods have full parameter info
- >70% methods have return types
- All code examples extracted
- Markdown documentation complete
- Query interface accurate

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| No API docs in CHM | Low | Critical | Verify content before running |
| Parser crashes on malformed HTML | Medium | High | Add try/except, continue on error |
| Memory exhaustion | Low | Medium | Monitor RAM, process in chunks if needed |
| JSON output invalid | Low | High | Validate JSON, fix serialization issues |
| Zero methods extracted | Medium | Critical | Check HTML structure matches patterns |

## Security Considerations
- No external network access
- Read-only input processing
- Output to local filesystem
- Validate JSON before loading

## Next Steps
- Proceed to [Phase 06: Validation](phase-06-validation-and-verification.md)
- Verify extraction quality and accuracy

## Expected Output Comparison

| Metric | Previous (Tutorial) | Target (API Docs) |
|--------|---------------------|-------------------|
| Files processed | ~10 | 50-500 |
| Methods extracted | 0 | 100+ |
| Parameters extracted | N/A | 80%+ |
| Return types | N/A | 70%+ |
| Code examples | 0 | 20+ |
| Namespaces | 1 | 5-10 |
