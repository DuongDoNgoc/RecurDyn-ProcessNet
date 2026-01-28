# CHM Extraction on Linux/WSL: Research Report

**Date:** 2026-01-28 | **File:** ProcessNetHelp.chm (31MB)

## Executive Summary

Three viable approaches exist for CHM extraction on Linux/WSL, each with distinct trade-offs. **Recommended:** Extract_chmLib (simplest) for initial exploration, PyCHM (programmatic) for post-processing, 7zip (fallback) if library issues arise.

---

## 1. Available Tools for CHM Extraction

### Primary Options

| Tool | Type | Install | Best For | Notes |
|------|------|---------|----------|-------|
| **extract_chmLib** | CLI | `apt install libchm-bin` | Direct extraction | Zero config, bundled with chmlib |
| **PyCHM** | Python lib | `pip install pychm` (requires chmlib) | Programmatic access | Maintenance mode, Python 3.6+ |
| **7zip** | CLI/lib | `apt install p7zip-full` | Archive extraction | Universal, handles CHM as archive |
| **arCHMage** | Python CLI | `pip install archmage` | Format conversion | Converts to HTML/PDF, builds on PyCHM |

### Secondary Options
- **KchmViewer / xCHM**: GUI viewers (not extraction-focused)
- **GnoCHM**: Linux-specific viewer with basic extraction

---

## 2. Recommended Approach: Multi-Stage Strategy

### Stage 1: Extract with extract_chmLib (Fastest)
```bash
apt install libchm-bin
extract_chmLib ProcessNetHelp.chm ./output
```
**Pros:** Simple, no encoding conversion, preserves internal structure
**Cons:** Extracts raw format, may include system files

### Stage 2: Parse/Validate with PyCHM (Optional)
```python
from chm.chm import CHMFile

chm = CHMFile('ProcessNetHelp.chm')
for entry in chm.entries:
    print(entry)  # Process metadata, encoding info
```
**Pros:** Programmatic access to metadata, encoding detection
**Cons:** Requires C lib dependency, hobby-level maintenance

### Stage 3: Fallback - 7zip
```bash
7z x ProcessNetHelp.chm -o./output
```
**Pros:** Universal, no external dependencies beyond p7zip
**Cons:** Treats CHM as generic archive, may miss metadata

---

## 3. Handling Encoding Issues

### Root Cause
CHM files often store content as **Windows-1252 (ANSI)** instead of UTF-8, causing character corruption:
- Legacy: MS HTML Help 1.x compiler tied to ANSI encodings
- Mixed: Table of Contents/Index use MBCS; content pane supports UTF-8
- Multiple encodings: URLs (MBCS), page content (UTF-8), display (page-specific)

### Solutions

**During Extraction:**
1. Use PyCHM's `chm.extra` module for encoding detection:
   ```python
   from chm.extra import detect_encoding
   encoding = detect_encoding(chm)
   ```

2. Post-process HTML: Inject UTF-8 meta tag or convert via iconv:
   ```bash
   iconv -f WINDOWS-1252 -t UTF-8 input.html > output.html
   ```

**For Parsed Content:**
- Extract to memory, detect encoding, convert during parsing
- Consider encoding fallback chains: UTF-8 → Windows-1252 → Latin-1

### Special Cases
- CJK files (Chinese/Japanese/Korean): Verify encoding metadata before conversion
- Complex characters: Test with sample files before batch processing

---

## 4. Large File Handling (31MB)

### Performance Considerations
- **Memory:** CHM containers are compressed; full extraction safe for 31MB
- **I/O:** extract_chmLib streams efficiently; PyCHM loads selectively
- **Processing:** Iterate over entries rather than loading entire tree:
  ```python
  for entry in chm.entries:
      content = chm.retrieve_object(entry)  # Load only accessed entries
  ```

### Recommended Workflow
1. Extract once with `extract_chmLib` → disk cache
2. Process in chunks: read HTML files in batches, parse with BeautifulSoup
3. Store results incrementally (avoid in-memory aggregation)

---

## 5. Installation Stack (Minimal WSL Setup)

```bash
# Core dependencies
apt update && apt install -y libchm-bin p7zip-full

# Python support (optional)
pip install pychm beautifulsoup4

# Conversion tools (optional)
pip install archmage  # Requires htmldoc, lynx/elinks for PDF
```

---

## 6. Quick Reference Commands

| Task | Command |
|------|---------|
| Extract all files | `extract_chmLib file.chm ./output` |
| Extract with 7z | `7z x file.chm -o./output` |
| List contents | `7z l file.chm` |
| Convert to HTML (via archmage) | `archmage file.chm ./output_dir` |
| Run as HTTP server | `archmage -p 8080 file.chm` |

---

## 7. Implementation Checklist

- [ ] Install libchm-bin + p7zip-full
- [ ] Test extraction: `extract_chmLib ProcessNetHelp.chm ./test_output`
- [ ] Validate HTML files created (count, encoding)
- [ ] Sample encoding detection: check for Windows-1252 vs UTF-8 content
- [ ] Process samples with BeautifulSoup for parsing validation
- [ ] Plan post-processing (encoding conversion if needed)
- [ ] Implement incremental processing (avoid full in-memory load)

---

## Citations & Sources

- [PyCHM · PyPI](https://pypi.org/project/pychm/)
- [PyCHM GitHub](https://github.com/dottedmag/pychm)
- [extract_chmLib Ubuntu Manual](https://manpages.ubuntu.com/manpages/bionic/man1/extract_chmLib.1.html)
- [arCHMage GitHub](https://github.com/dottedmag/archmage)
- [7-Zip Command Line](https://7-zip.opensource.jp/chm/cmdline/commands/extract.html)
- [CHM Encoding Issues - DITA-OT](https://github.com/dita-ot/dita-ot/issues/2020)
- [HelpNDoc: International Character Encoding in CHM](https://www.helpndoc.com/news-and-articles/2025-05-14-why-international-characters-break-in-chm-files-and-how-helpndoc-solves-it/)

---

## Unresolved Questions

1. **Exact encoding of ProcessNetHelp.chm:** Requires sample inspection to determine Windows-1252 vs mixed encoding profile
2. **Internal structure complexity:** Unknown if CHM contains custom ITSS metadata requiring special parsing
3. **Performance baseline:** No benchmark data for 31MB CHM extraction speed (estimate: 5-30 seconds depending on disk I/O)
