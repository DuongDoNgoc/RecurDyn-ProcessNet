# Phase 3: User Guide Sphinx HTML Extractor

## Context

- **Plan:** [v7 KB: C#/VB API + User Guide Extraction](plan.md)
- **Date:** 2026-02-01
- **Status:** Pending
- **Effort:** 1h

## Overview

Extract user guide content from 27 Sphinx ReadTheDocs HTML files in `knowledge/RecurDynHelp/ProcessNet/`. These files use toctree navigation with hierarchical chapter/section structure (43 > 43.1 > 43.1.1).

## Key Insights

### File Naming Convention

```
ProcessNet_ch00_index.html        # Chapter 43 (main index)
ProcessNet_ch01_s05_00_index.html # Section 43.1.5
ProcessNet_ch01_s05_01.html       # Subsection 43.1.5.1
ProcessNet_ch02_s00_index.html    # Section 43.2
ProcessNet_ch03_s06_01.html       # Subsection 43.3.6.1
```

Pattern: `ProcessNet_ch{chapter}_s{section}_{subsection}.html`

### Sphinx ReadTheDocs Structure

```html
<html class="writer-html5">
<body class="wy-body-for-nav">
  <div class="wy-grid-for-nav">
    <!-- Sidebar navigation -->
    <nav class="wy-nav-side">
      <div class="wy-menu wy-menu-vertical">
        <ul class="current">
          <li class="toctree-l1"><a>43. ProcessNet</a>
            <ul>
              <li class="toctree-l2"><a>43.1 ProcessNet Python</a></li>
              <li class="toctree-l2 current"><a>43.2 ProcessNet Gadget</a>
                <ul>
                  <li class="toctree-l3"><a>43.2.1 Clone Body</a></li>
                </ul>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Main content -->
    <section class="wy-nav-content-wrap">
      <div class="wy-nav-content">
        <div class="rst-content">
          <div role="main" class="document">
            <section id="processnet-gadget">
              <h1>43.2.10. ProcessNet Gadget</h1>
              <p>Content here...</p>
            </section>
          </div>
        </div>
      </div>
    </section>
  </div>

  <!-- Navigation links -->
  <link rel="prev" href="ProcessNet_ch01_s05_00_index.html">
  <link rel="next" href="ProcessNet_ch02_s01_00_index.html">
</body>
</html>
```

### Navigation Elements

- **Toctree:** `<li class="toctree-l{N}">` where N is depth (1-4)
- **Current page:** `<li class="toctree-l{N} current">`
- **Prev/Next:** `<link rel="prev/next" href="...">`
- **Section ID:** `<section id="section-slug">`

## Requirements

1. Parse all 27 HTML files in `knowledge/RecurDynHelp/ProcessNet/`
2. Extract toctree hierarchy for navigation structure
3. Extract main content from `<div role="main">`
4. Parse section numbers from headings (43.2.10 format)
5. Build parent-child relationships between sections
6. Output: Included in `output/processnet-userguide.json`

## Architecture

### Dataclasses

```python
@dataclass
class SphinxSection:
    """Section from Sphinx user guide."""
    number: str       # "43.2.10"
    title: str        # "ProcessNet Gadget"
    full_title: str   # "43.2.10. ProcessNet Gadget"
    level: int        # Depth in hierarchy (1, 2, 3, 4)
    content: str      # Main prose content
    parent_number: str  # "43.2" for "43.2.10"
    children: list = field(default_factory=list)  # Child section numbers
    prev_href: str = ""
    next_href: str = ""
    source_file: str = ""
    section_id: str = ""  # HTML id attribute

@dataclass
class SphinxTocTree:
    """Navigation structure from toctree."""
    root_number: str
    items: list = field(default_factory=list)  # Flat list of (number, title, href, level)
```

### SphinxGuideExtractor Class

```python
class SphinxGuideExtractor:
    """Extract user guide from Sphinx ReadTheDocs HTML."""

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.sections = {}  # number -> SphinxSection
        self.toctree = None

    def discover_files(self) -> list[Path]:
        """Find ProcessNet_ch*.html files."""

    def parse_section_number(self, title: str) -> tuple[str, str]:
        """Extract number and title from '43.2.10. ProcessNet Gadget'."""

    def determine_level(self, number: str) -> int:
        """Count dots in number to determine hierarchy level."""

    def extract_toctree(self, soup: BeautifulSoup) -> SphinxTocTree:
        """Parse toctree navigation from sidebar."""

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """Extract prose from <div role='main'>."""

    def extract_nav_links(self, soup: BeautifulSoup) -> tuple[str, str]:
        """Get prev/next hrefs from <link> tags."""

    def parse_section(self, file_path: Path) -> SphinxSection:
        """Parse single file into SphinxSection."""

    def build_hierarchy(self):
        """Link parent-child relationships after all sections parsed."""

    def build_guide_knowledge(self):
        """Process all files and build hierarchy."""

    def save_output(self):
        """Save to JSON."""
```

## Implementation Steps

### Step 1: Create extractor skeleton (15 min)

```python
# src/userguide-sphinx-extractor.py
#!/usr/bin/env python3
"""
User Guide Sphinx HTML Extractor

Extracts tutorial content from Sphinx ReadTheDocs HTML files.
"""
```

### Step 2: Implement section number parsing (10 min)

```python
def parse_section_number(self, title: str) -> tuple[str, str]:
    """Extract number and title from heading."""
    # Pattern: "43.2.10. ProcessNet Gadget"
    match = re.match(r'^([\d.]+)\.\s*(.+)$', title.strip())
    if match:
        return match.group(1), match.group(2)
    return "", title

def determine_level(self, number: str) -> int:
    """Count dots to get hierarchy level."""
    if not number:
        return 0
    return number.count('.') + 1  # "43" = 1, "43.2" = 2, "43.2.10" = 3
```

### Step 3: Implement toctree extraction (15 min)

```python
def extract_toctree(self, soup: BeautifulSoup) -> list[tuple]:
    """Parse toctree from sidebar navigation."""
    items = []
    toctree = soup.find('div', class_='wy-menu')
    if not toctree:
        return items

    for li in toctree.find_all('li', class_=re.compile(r'toctree-l\d')):
        # Get level from class
        classes = li.get('class', [])
        level = 1
        for cls in classes:
            if cls.startswith('toctree-l'):
                level = int(cls[-1])
                break

        # Get link
        a = li.find('a', recursive=False)
        if a:
            href = a.get('href', '')
            title = a.get_text(strip=True)
            number, name = self.parse_section_number(title)
            items.append((number, name, href, level))

    return items
```

### Step 4: Implement content extraction (10 min)

```python
def extract_main_content(self, soup: BeautifulSoup) -> str:
    """Extract main document content."""
    main = soup.find('div', role='main')
    if not main:
        main = soup.find('div', class_='document')
    if not main:
        return ""

    # Remove navigation elements
    for nav in main.find_all(['nav', 'div'], class_=['toctree-wrapper']):
        nav.decompose()

    # Get text content
    return main.get_text(separator='\n', strip=True)
```

### Step 5: Build hierarchy and save (10 min)

```python
def build_hierarchy(self):
    """Link parent-child relationships."""
    for number, section in self.sections.items():
        # Find parent by removing last segment
        parts = number.rsplit('.', 1)
        if len(parts) == 2:
            parent_number = parts[0]
            if parent_number in self.sections:
                section.parent_number = parent_number
                self.sections[parent_number].children.append(number)
```

## Output Schema

```json
{
  "sphinx_guides": {
    "toctree": [
      {"number": "43", "title": "ProcessNet", "href": "ProcessNet_ch00_index.html", "level": 1},
      {"number": "43.1", "title": "ProcessNet Python", "href": "...", "level": 2},
      {"number": "43.2", "title": "ProcessNet Gadget", "href": "...", "level": 2}
    ],
    "sections": {
      "43": {
        "number": "43",
        "title": "ProcessNet",
        "full_title": "43. ProcessNet",
        "level": 1,
        "content": "ProcessNet is the automation framework...",
        "parent_number": "",
        "children": ["43.1", "43.2", "43.3"],
        "prev_href": "",
        "next_href": "ProcessNet_ch01_s05_00_index.html",
        "source_file": "ProcessNet_ch00_index.html",
        "section_id": "processnet"
      }
    }
  },
  "statistics": {
    "total_sections": 27,
    "max_depth": 4,
    "total_words": 15000
  }
}
```

## Todo List

- [ ] Create `src/userguide-sphinx-extractor.py`
- [ ] Implement `discover_files()` for ProcessNet_ch*.html
- [ ] Implement `parse_section_number()` regex
- [ ] Implement `determine_level()` helper
- [ ] Implement `extract_toctree()` navigation parser
- [ ] Implement `extract_main_content()` prose extractor
- [ ] Implement `extract_nav_links()` prev/next
- [ ] Implement `parse_section()` file parser
- [ ] Implement `build_hierarchy()` parent-child linking
- [ ] Implement `save_output()` JSON writer
- [ ] Test on all 27 files

## Success Criteria

1. All 27 files parsed without errors
2. Toctree hierarchy correctly extracted
3. Section numbers parsed (43.X.Y format)
4. Parent-child relationships established
5. Prev/next navigation captured
6. Output JSON well-structured

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Inconsistent numbering | Low | Low | Fallback to filename |
| Deep nesting | Low | Low | Support 4+ levels |
| Missing content div | Low | Medium | Multiple fallback selectors |

## Related Code

- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/knowledge/RecurDynHelp/ProcessNet/` - Input
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py` - Sphinx patterns
