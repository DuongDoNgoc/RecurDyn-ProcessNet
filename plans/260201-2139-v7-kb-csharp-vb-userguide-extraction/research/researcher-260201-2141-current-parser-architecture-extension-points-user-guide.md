# Parser Architecture Analysis: Extension Points for User Guide Extraction

**Date:** 2026-02-01 | **Status:** Research Complete

## Executive Summary

Parser successfully extracts API docs from Sphinx/HTML. User Guide extraction requires different strategy—guides use Sphinx ReadTheDocs HTML structure (toctree, sections) rather than definition lists. Recommend extending parser with separate `UserGuideExtractor` class following existing patterns (KISS, DRY).

---

## 1. Current Parser Architecture

**Location:** `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py` (1344 lines)

**Main Class:** `ProcessNetDocParser`

### Flow:
1. **File Discovery** (`discover_files()`) → Find HTML files, exclude `_static`, `_images`, `mathjax`
2. **HTML Reading** (`read_html_file()`) → BeautifulSoup + encoding detection (chardet)
3. **Parse** (`parse_html_file()`) → Extract content from single file
4. **Build KB** (`build_knowledge_base()`) → Aggregate all files into JSON
5. **Save** (`save_knowledge_base()`) → Output JSON + error log
6. **Markdown** (`generate_markdown()`) → Optional markdown export

### Key Statistics (v6 KB):
- **Files:** 40,625 processed (23 namespaces)
- **Classes:** 1,830 extracted
- **Methods:** 6,773 with ~0.3 params/method (extraction gaps)
- **Examples:** 887 code blocks
- **Duration:** 247 seconds

---

## 2. HTML Patterns Recognized by Parser

### API Documentation (Sphinx-formatted)
**Source:** `RecurDynHelp/Python/Professional/*.html`

```
Patterns extracted:
- dl.py.class → Classes (dt.sig + dd content)
- dl.py.method → Methods (parameters, returns, description)
- dl.py.property → Properties (type, description)
- Autosummary tables (for class member lists)
- Code blocks (div.highlight → CodeExample)
```

**CSS Classes Used:**
```python
dl class="py" + class="class|method|property|function"
dt class="sig"
dd elements (descriptions)
div class="highlight" (code blocks)
dl class="field-list" (parameters/returns)
p class="rubric" (section headers)
table.autosummary (member summaries)
```

---

## 3. User Guide HTML Structure

**Source:** `RecurDynHelp/ProcessNet/*.html` (27 files)

**Template:** Sphinx ReadTheDocs (same framework as API docs, different content)

```html
<html class="writer-html5">
  <body class="wy-body-for-nav">
    <div class="wy-grid-for-nav">
      <nav class="wy-nav-side">
        <div class="wy-menu wy-menu-vertical">
          <ul class="current">
            <!-- Toctree structure -->
            <li class="toctree-l1"><a>Chapter Title</a>
              <ul>
                <li class="toctree-l2"><a>Section</a>
                <li class="toctree-l3"><a>Subsection</a>
```

**Key Differences from API Docs:**
1. **Navigation via toctree** (nested `<li class="toctree-lN">`) instead of method lists
2. **Hierarchical structure** (Ch 43 > 43.1 > 43.1.1) vs flat namespaces
3. **Prose content** (descriptions, tutorials, usage patterns) vs API signatures
4. **Few code examples** embedded (mostly in inline divs, not autosummary tables)
5. **No method/property definitions** — just references/usage

**Example from ProcessNet_ch01_s05_00_index.html:**
```
Title: 43.2.10. ProcessNet Gadget
Navigation: 43 > 43.2 > 43.2.10
Next: 43.2.10.1. Clone Body Change Tool
Prev: 43.2.9. Converting a ProcessNet...
```

---

## 4. Knowledge Base JSON Structure

**Root Schema:**
```json
{
  "metadata": {
    "source": "RecurDyn ProcessNet API",
    "version": "extracted",
    "extraction_date": "ISO timestamp",
    "total_files_processed": int,
    "extraction_duration_seconds": float
  },
  "namespaces": {
    "ProcessNet": {
      "full_name": "FunctionBay.RecurDyn.ProcessNet",
      "description": "...",
      "classes": [
        {
          "name": "ClassName",
          "description": "...",
          "inheritance": "BaseClass",
          "methods": [
            {
              "name": "MethodName",
              "signature": "Type MethodName(params)",
              "description": "...",
              "parameters": [
                {"name": "param1", "type": "string", "description": "..."}
              ],
              "returns": "Type",
              "return_description": "...",
              "source_file": "path.html"
            }
          ],
          "properties": [...],
          "source_file": "path.html"
        }
      ],
      "examples": [
        {
          "title": "...",
          "code": "...",
          "language": "csharp|python",
          "source_file": "path.html"
        }
      ],
      "files": ["path1.html", "path2.html", ...],
      "orphaned_members": [...]  // Tracking only, not in output
    }
  },
  "method_index": {"method_name": ["namespace1", ...]},
  "class_index": {"classname": ["namespace"]},
  "interface_index": {"IInterfaceName": [...]}
}
```

**For User Guide:**
```json
{
  "metadata": {...},
  "guides": {
    "ProcessNet User Guide": {
      "description": "...",
      "chapters": [
        {
          "number": "43",
          "title": "ProcessNet",
          "sections": [
            {
              "number": "43.1",
              "title": "ProcessNet Python",
              "subsections": [
                {
                  "number": "43.1.1",
                  "title": "...",
                  "description": "...",
                  "source_file": "ProcessNet_ch03_s00_index.html"
                }
              ]
            }
          ]
        }
      ]
    }
  },
  "guide_index": {"term": ["chapter", "section"], ...},
  "file_manifest": [...]
}
```

---

## 5. Extension Points & Reusable Components

### Existing Infrastructure to Leverage:

| Component | Reusable | Notes |
|-----------|----------|-------|
| `BeautifulSoup` parsing | YES | Already used, works for User Guide |
| `detect_encoding()` | YES | HTML files have same encoding |
| `extract_title()` | YES | Works on all Sphinx HTML |
| `discover_files()` | YES | Simple glob-based discovery |
| `asdict()` conversion | YES | For JSON serialization |
| `logging` setup | YES | Already configured |
| `chardet` detection | YES | Handles encoding |

### Required New Methods:

```python
class UserGuideExtractor:
    """Extract hierarchy from Sphinx ReadTheDocs toctree navigation."""

    def extract_toctree_structure(soup: BeautifulSoup) -> dict:
        """Parse nested <li class="toctree-lN"> into chapter/section hierarchy."""

    def extract_section_metadata(soup: BeautifulSoup) -> dict:
        """Get section number, title, prev/next navigation links."""

    def extract_prose_content(soup: BeautifulSoup) -> str:
        """Main documentation content (excluding nav, sidebars)."""

    def extract_code_snippets(soup: BeautifulSoup) -> list:
        """Find inline code blocks (highlight divs) in guide content."""
```

---

## 6. HTML Parsing Specifics for User Guides

### Content Selectors:
```python
# Main content
main_content = soup.find('div', role='main') or \
               soup.find('article') or \
               soup.find('div', class_='document')

# Navigation
toctree = soup.find('div', class_='wy-menu wy-menu-vertical')
nav_items = toctree.find_all('li', class_=lambda x: x and 'toctree-l' in x)

# Section metadata (for breadcrumb)
title = soup.find('h1') or soup.find('title')
breadcrumb = soup.find_all('li', class_='toctree-l1')

# Navigation links
prev_link = soup.find('link', rel='prev')  # <link rel="prev" href="...">
next_link = soup.find('link', rel='next')  # <link rel="next" href="...">
```

### Extraction Gaps (API Parser):
- Low parameter extraction (0.3 params/method avg) — users may have custom parsing for Sphinx
- Orphaned members (16-10 per namespace) — member files without parent classes
- **Missing:** Multi-language variant detection (User Guide not multi-lang, so N/A)

---

## 7. Dataclass Definitions for User Guides

```python
@dataclass
class GuideSection:
    number: str          # "43.1.1"
    title: str
    description: str     # First paragraph of content
    level: int          # Depth in hierarchy (1,2,3,...)
    parent_id: str      # Section number of parent
    children_ids: list  # Section numbers of subsections
    source_file: str
    content_hash: str   # To detect changes

@dataclass
class UserGuide:
    name: str           # "ProcessNet User Guide"
    description: str
    chapters: list      # List of GuideSection
    nav_structure: dict # Flattened toctree
    files: list         # All HTML files processed
```

---

## 8. Recommended Implementation Strategy

**Phase 1: Separate Extractor Class**
- Create `UserGuideExtractor(input_path, output_path)` parallel to existing parser
- Reuse: file discovery, encoding detection, logging, JSON output
- New: toctree parsing, hierarchy building

**Phase 2: JSON Output**
- Output: `processnet-guides-v1.json` (separate from API KB)
- Structure: 3 top-level keys: `guides`, `sections_index`, `metadata`
- Enable: full-text search by storing section content + code snippets

**Phase 3: Query Interface**
- Update query API to handle both `processnet-knowledge-v6.json` (API) and guides
- Endpoint: `GET /guides?q=...` for guide search
- Return: section hierarchy + matching content snippets

---

## 9. Known Constraints

| Constraint | Impact | Mitigation |
|-----------|--------|-----------|
| 27 User Guide HTML files (small corpus) | Extraction easy but limited depth | Focus on robust hierarchy building |
| No C#/VB API refs in guides (prose only) | Can't auto-link to API docs | Manual cross-reference index later |
| Toctree navigation rebuilt on every parse | Inefficient; no incremental | Cache toctree as static JSON |
| ReadTheDocs style may change | Risk if docs regenerated | Version check in parser metadata |

---

## 10. Unresolved Questions

1. **Should User Guide KB be merged with API KB or separate file?**
   - Current: Recommend separate (`processnet-guides.json`) for clarity
   - Alternative: Nest under `knowledge_base['guides']` namespace

2. **How to handle cross-references (e.g., "See IApplication" in User Guide)?**
   - Option A: Extract as tags for linking in UI
   - Option B: Full graph-based linking to API classes

3. **What depth of section extraction is needed?**
   - Current: toctree goes to 4-5 levels deep; feasible to extract all
   - Trade-off: More granular = larger JSON, better searchability

---

## Conclusion

**Current parser is well-architected for API extraction.** User Guide extraction requires ~300 LOC in new `UserGuideExtractor` class. Leverage existing infrastructure: BeautifulSoup, encoding detection, file I/O, logging. Output separate KB JSON to avoid mixing API and guide content types.

**Effort estimate:** 1-2 days for Phase 1 (basic extraction) + tests.

---

## Appendix: File Locations

| File | Purpose |
|------|---------|
| `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py` | Main API parser |
| `/mnt/d/Vibecoding/RecurDyn-ProcessNet/knowledge/RecurDynHelp/ProcessNet/` | User Guide HTML (27 files) |
| `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v6.json` | Current API KB (21 MB) |
| `/mnt/d/Vibecoding/RecurDyn-ProcessNet/docs/` | Documentation |

