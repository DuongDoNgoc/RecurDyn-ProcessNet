# Phase 2: User Guide Word HTML Extractor

## Context

- **Plan:** [v7 KB: C#/VB API + User Guide Extraction](plan.md)
- **Date:** 2026-02-01
- **Status:** Pending
- **Effort:** 1.5h

## Overview

Extract user guide content from 7 Microsoft Word HTML export files in `output/extracted_chm/Content/UserGuideFiles/`. These files contain tutorials, workflows, and UI guidance with heavy MSO-specific markup that needs cleanup.

## Key Insights

### File Inventory

| File | Size | Content (estimated) |
|------|------|---------------------|
| ProcessNet User Guide1.htm | 215 KB | Getting started, overview |
| ProcessNet User Guide2.htm | 47 KB | Basic concepts |
| ProcessNet User Guide3.htm | 101 KB | Intermediate topics |
| ProcessNet User Guide4.htm | 277 KB | Major feature section |
| ProcessNet User Guide5.htm | 67 KB | Advanced topics |
| ProcessNet User Guide6.htm | 28 KB | Reference |
| ProcessNet User Guide7.htm | 14 KB | Appendix |

### Word HTML Structure

```html
<html xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns:m="http://schemas.microsoft.com/office/2004/12/omml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ks_c_5601-1987">
    <meta name="Generator" content="Microsoft Word 15">
    <style>
      /* MSO-specific CSS: mso-style-*, mso-font-*, mso-pagination-* */
      @font-face { font-family: "Malgun Gothic"; ... }
    </style>
  </head>
  <body>
    <div class="WordSection1">
      <h1>Chapter Title</h1>
      <p class="MsoNormal">Content with MSO styling...</p>
      <p class="MsoListParagraph">List item...</p>
      <!-- Images reference .files/ subdirectory -->
      <img src="ProcessNet User Guide1.files/image001.png">
    </div>
  </body>
</html>
```

### MSO Artifacts to Strip

- XML namespaces: `xmlns:v`, `xmlns:o`, `xmlns:w`, `xmlns:m`
- CSS properties: `mso-*` (mso-style-name, mso-font-charset, etc.)
- Conditional comments: `<!--[if gte mso 9]>...<![endif]-->`
- Office elements: `<o:*>`, `<w:*>`, `<v:*>`
- Class names: `MsoNormal`, `MsoListParagraph`, `MsoToc*`

## Requirements

1. Parse all 7 HTM files in `Content/UserGuideFiles/`
2. Strip MSO-specific markup while preserving content
3. Extract heading hierarchy (h1-h6) for TOC
4. Preserve paragraph text and lists
5. Handle KS_C_5601-1987 (Korean) encoding
6. Reference images in `.files/` directories
7. Output: Included in `output/processnet-userguide.json`

## Architecture

### Dataclasses

```python
@dataclass
class GuideSection:
    """Section within user guide."""
    title: str
    level: int  # 1-6 based on heading
    content: str  # Cleaned prose text
    images: list = field(default_factory=list)
    source_file: str = ""
    section_id: str = ""  # Generated from title

@dataclass
class UserGuide:
    """Complete user guide document."""
    title: str
    source_file: str
    sections: list = field(default_factory=list)
    word_count: int = 0
    image_count: int = 0
```

### WordGuideExtractor Class

```python
class WordGuideExtractor:
    """Extract user guide content from Word HTML exports."""

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = input_path
        self.output_path = output_path
        self.guides = []

    def discover_files(self) -> list[Path]:
        """Find ProcessNet User Guide*.htm files."""

    def detect_encoding(self, file_path: Path) -> str:
        """Detect encoding (expect ks_c_5601-1987)."""

    def strip_mso_markup(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Remove MSO namespaces, comments, and styles."""

    def extract_headings(self, soup: BeautifulSoup) -> list[tuple]:
        """Extract (level, title, content_after) tuples."""

    def extract_images(self, soup: BeautifulSoup, source_file: str) -> list[str]:
        """Find image references in .files/ directories."""

    def clean_text(self, element) -> str:
        """Extract clean text from element, strip MSO classes."""

    def parse_guide(self, file_path: Path) -> UserGuide:
        """Parse single guide file into UserGuide."""

    def build_guide_knowledge(self):
        """Process all guide files."""

    def save_output(self):
        """Save to JSON."""
```

## Implementation Steps

### Step 1: Create extractor skeleton (20 min)

```python
# src/userguide-word-extractor.py
#!/usr/bin/env python3
"""
User Guide Word HTML Extractor

Extracts tutorial content from Microsoft Word HTML exports.
"""
```

### Step 2: Implement MSO cleanup (30 min)

```python
def strip_mso_markup(self, soup: BeautifulSoup) -> BeautifulSoup:
    """Remove MSO namespaces, comments, and styles."""
    # Remove conditional comments
    for comment in soup.find_all(string=lambda t: isinstance(t, Comment)):
        if 'mso' in str(comment).lower() or 'office' in str(comment).lower():
            comment.extract()

    # Remove office namespace elements
    for tag in soup.find_all(re.compile(r'^(o|w|v|m):')):
        tag.decompose()

    # Strip mso-* CSS properties from style attributes
    for tag in soup.find_all(style=True):
        style = tag['style']
        # Remove mso-* properties
        cleaned = re.sub(r'mso-[^;]+;?\s*', '', style)
        if cleaned.strip():
            tag['style'] = cleaned
        else:
            del tag['style']

    # Strip MSO class names
    for tag in soup.find_all(class_=True):
        classes = tag.get('class', [])
        cleaned = [c for c in classes if not c.startswith('Mso')]
        if cleaned:
            tag['class'] = cleaned
        else:
            del tag['class']

    return soup
```

### Step 3: Implement heading extraction (20 min)

```python
def extract_headings(self, soup: BeautifulSoup) -> list[GuideSection]:
    """Extract heading hierarchy with content."""
    sections = []
    current_section = None

    for element in soup.body.descendants:
        if element.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            level = int(element.name[1])
            title = element.get_text(strip=True)

            if current_section:
                sections.append(current_section)

            current_section = GuideSection(
                title=title,
                level=level,
                content="",
                section_id=self._slugify(title)
            )
        elif current_section and element.name == 'p':
            text = self.clean_text(element)
            if text:
                current_section.content += text + "\n\n"

    if current_section:
        sections.append(current_section)

    return sections
```

### Step 4: Implement image extraction (15 min)

```python
def extract_images(self, soup: BeautifulSoup, source_file: str) -> list[str]:
    """Find image references."""
    images = []
    base_name = Path(source_file).stem

    for img in soup.find_all('img'):
        src = img.get('src', '')
        if f'{base_name}.files/' in src:
            images.append(src)

    return images
```

### Step 5: Build and save output (15 min)

## Output Schema

```json
{
  "word_guides": [
    {
      "title": "ProcessNet User Guide",
      "source_file": "ProcessNet User Guide1.htm",
      "sections": [
        {
          "title": "Introduction",
          "level": 1,
          "content": "ProcessNet is a powerful automation...",
          "images": ["ProcessNet User Guide1.files/image001.png"],
          "section_id": "introduction"
        },
        {
          "title": "Getting Started",
          "level": 2,
          "content": "To begin using ProcessNet...",
          "images": [],
          "section_id": "getting-started"
        }
      ],
      "word_count": 5000,
      "image_count": 15
    }
  ],
  "statistics": {
    "total_guides": 7,
    "total_sections": 50,
    "total_words": 25000,
    "total_images": 100
  }
}
```

## Todo List

- [ ] Create `src/userguide-word-extractor.py`
- [ ] Implement `detect_encoding()` for Korean encoding
- [ ] Implement `strip_mso_markup()` cleanup
- [ ] Implement `extract_headings()` for TOC
- [ ] Implement `extract_images()` for asset refs
- [ ] Implement `clean_text()` helper
- [ ] Implement `parse_guide()` main parser
- [ ] Implement `build_guide_knowledge()` batch
- [ ] Implement `save_output()` JSON writer
- [ ] Test on all 7 guide files
- [ ] Verify encoding handling

## Success Criteria

1. All 7 guide files parsed without errors
2. MSO markup fully stripped
3. Heading hierarchy preserved
4. Korean text decoded correctly
5. Image references captured
6. Output JSON <5 MB

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Encoding issues | Medium | Medium | Use chardet fallback |
| Complex MSO nesting | Medium | Low | Iterative cleanup |
| Missing content | Low | Medium | Validate word count |

## Related Code

- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/extracted_chm/Content/UserGuideFiles/` - Input
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/recurdyn-doc-parser.py` - Encoding patterns
