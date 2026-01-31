# Phase 01: CHM Extraction on Windows

## Context
- **Parent Plan:** [plan.md](plan.md)
- **Research:** [researcher-01-chm-extraction-methods.md](research/researcher-01-chm-extraction-methods.md)
- **Dependencies:** 7-Zip installed on Windows

## Overview
**Date:** 2026-01-31
**Description:** Extract ProcessNetHelp.chm file using 7-Zip on Windows to HTML format
**Priority:** P1 (Critical - blocks all subsequent phases)
**Status:** pending
**Review Status:** Not started

## Key Insights
From research report:
- 7-Zip is recommended (free, open-source, automated)
- Command: `7z x file.chm -ooutput_dir -y`
- CHM contains compiled HTML with TOC, index, topic files
- Output preserves structure and formatting

## Requirements

### Functional
- Locate ProcessNetHelp.chm on Windows filesystem
- Extract all HTML content to output directory
- Preserve directory structure from CHM
- Verify extraction completeness (file count)

### Non-Functional
- Extraction time <5 minutes
- Handle UTF-8 and Windows-1252 encodings
- No data loss (all HTML files extracted)

## Architecture

```
Windows:
  C:\path\to\RecurDyn\Help\ProcessNetHelp.chm
  ↓ 7z x command
  C:\temp\extracted_chm\
    ├── html/
    │   ├── ProcessNet.Model.Body.html
    │   ├── ProcessNet.Geometry.Arc.html
    │   └── ...
    ├── [Content_Types].xml
    └── index.html
```

## Related Code Files

### Files to Use
- None (manual extraction step)

### Files to Create
- `output/extracted_chm/` - Extraction target (via WSL mount)

## Implementation Steps

1. **Locate CHM file**
   - Check RecurDyn installation directory
   - Common paths:
     - `C:\Program Files\FunctionBay\RecurDyn\Help\ProcessNetHelp.chm`
     - `C:\Program Files (x86)\FunctionBay\RecurDyn\Help\ProcessNetHelp.chm`
   - Document actual location found

2. **Verify 7-Zip installation**
   - Check: `"C:\Program Files\7-Zip\7z.exe"` exists
   - If missing: Download from https://www.7-zip.org/
   - Verify 7-Zip in PATH or use full path

3. **Create extraction directory**
   ```batch
   mkdir C:\temp\extracted_chm
   ```

4. **Run extraction command**
   ```batch
   "C:\Program Files\7-Zip\7z.exe" x "C:\path\to\ProcessNetHelp.chm" -o"C:\temp\extracted_chm" -y
   ```
   - `x` = extract with full paths
   - `-o` = output directory
   - `-y` = assume yes to all prompts

5. **Verify extraction**
   - Count HTML files: `dir /s /b C:\temp\extracted_chm\*.html | find /c /v ""`
   - Check key files exist (index.html, TOC structure)
   - Document file count and structure

6. **Document results**
   - Record actual CHM path
   - Record output directory
   - Record file count
   - Note any anomalies (encoding warnings, errors)

## Todo List

- [ ] Locate ProcessNetHelp.chm file on Windows
- [ ] Verify 7-Zip installed (or install)
- [ ] Create extraction directory
- [ ] Run 7-Zip extraction command
- [ ] Verify extraction completeness (file count)
- [ ] Document extraction results in report

## Success Criteria
- CHM file successfully extracted
- HTML files present in output directory
- File count >50 (expected for API docs)
- No extraction errors in 7-Zip output

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| CHM file not found | Medium | High | Check multiple install paths, use search |
| 7-Zip not installed | Low | Low | Download/install (free, 2MB) |
| Extraction fails | Low | High | Try alternative tools (HTML Help Workshop) |
| Encrypted CHM | Very Low | High | Contact FunctionBay support |

## Security Considerations
- CHM extraction is read-only (no modification)
- No credentials required
- Extracted HTML may contain proprietary documentation - handle per license

## Next Steps
- Proceed to [Phase 02: File Transfer](phase-02-file-transfer-to-wsl.md)
- Transfer extracted files from Windows to WSL workspace
