# Research: Best Practices for Parsing Sphinx-Generated HTML Documentation

## Executive Summary
Sphinx HTML output uses standardized semantic structures based on Docutils conventions. Parsing targets definition lists (`<dl>`, `<dt>`, `<dd>`), field lists, and CSS classes for API documentation. BeautifulSoup is the recommended library for extraction.

---

## 1. Sphinx HTML Structure Patterns

### Core Elements
- **Definition Lists**: `<dl>` containers wrap API objects (classes, methods, functions)
  - `<dt>` holds the signature/name
  - `<dd>` contains description and metadata
- **Field Lists**: Store structured metadata (parameters, returns, raises)
  - Rendered as `<dl class="field-list simple">` or `<dl class="simple">`
  - Each field: `<dt>` (field label) + `<dd>` (field value)
- **Code Blocks**: `<pre><code>` for examples, wrapped in parent divs with `highlight` classes

### CSS Classes (Theme-Dependent)
ReadTheDocs theme and modern Sphinx themes use:
- `.descname` / `.descclassname`: Class/method names
- `.sig-param`: Function parameters
- `.highlight`: Code block containers
- `sd-*`: sphinx-design prefixed classes (modern themes)
- `.exception`, `.class`, `.method`, `.property`: Content type indicators
- `dl-simple`, `field-list simple`: Definition list variants

---

## 2. Sphinx autodoc Output Structure

### API Documentation Rendering
`sphinx.ext.autodoc` generates reStructuredText directives (`py:class`, `py:function`) which produce:

```html
<section id="module-name">
  <dl class="py class">
    <dt id="ClassName" class="sig">
      <span class="sig-name">ClassName</span>
      <span class="sig-paren">(</span>
      <span class="sig-param">...</span>
      <span class="sig-paren">)</span>
    </dt>
    <dd>
      <p>Description text</p>
      <dl class="field-list simple">
        <dt class="field-odd">Parameters</dt>
        <dd class="field-body">
          <ul class="simple">
            <li><strong>param_name</strong> (<em>type</em>) – description</li>
          </ul>
        </dd>
        <dt class="field-even">Returns</dt>
        <dd class="field-body">
          <p>return description</p>
        </dd>
      </dl>
    </dd>
  </dl>
</section>
```

---

## 3. BeautifulSoup Selectors for Extraction

### High-Level Approach
```python
from bs4 import BeautifulSoup

# Parse HTML
soup = BeautifulSoup(html_content, 'html.parser')

# Extract API items
for dl in soup.find_all('dl', class_='py'):
    # dl.find('dt') → signature
    # dl.find('dd') → description + metadata
```

### Targeted Selectors
| Target | Selector | Notes |
|--------|----------|-------|
| Classes/functions | `dl.py class`, `dl.py function` | Use class attribute |
| Method signatures | `dt.sig` inside `dd` parent | Contains `<span class="sig-*">` |
| Parameters | `dl.field-list dd` with "Parameters" dt | Parse from `<ul>` or `<li>` |
| Returns | `dd.field-body` after "Returns" dt | Text node extraction |
| Code examples | `div.highlight pre code` | Contains literal code |

### Practical Extraction Pattern
1. Find section by ID: `soup.find('section', id=section_name)`
2. Get definition list: `section.find('dl', class_='py')`
3. Parse signature from `<dt>`: Extract text, spans by class
4. Extract metadata from `<dd>` → field-list `<dl>` children
5. Parse structured lists: Iterate `<li>` for parameters, use regex for type annotations

---

## 4. Definition Lists & Field Lists Parsing

### HTML Structure (Docutils Standard)
```html
<dl class="field-list simple">
  <dt class="field-odd">Parameters:</dt>
  <dd class="field-body">
    <p><strong>name</strong> (<em>str</em>) – Description</p>
  </dd>
  <dt class="field-even">Returns:</dt>
  <dd class="field-body">
    <p>ReturnType – return description</p>
  </dd>
</dl>
```

### Extraction Logic
- **Field labels** (dt): Use `.get_text()` or text_content
- **Field values** (dd): May contain multiple elements (`<p>`, `<ul>`, `<table>`)
- **Alternating rows**: Use CSS `:nth-child(odd/even)` selectors or iterate pairs
- **Nested lists**: Parse `<ul><li>` for parameter lists; regex for `**name** (type) – desc` pattern

### Edge Cases
- Multiple descriptions per field (multiple `<dd>` for one `<dt>`)
- Mixed content: paragraphs + code blocks in single field
- Type annotations: Often in `<em>` tags within parentheses
- Cross-references: Links (`<a href>`) embedded in descriptions

---

## 5. Handling Cross-References & Navigation

### Cross-Reference Elements
- **Internal links**: `<a class="reference internal" href="#target">`
- **External links**: `<a class="reference external" href="url">`
- **Code references**: `<code class="xref py">ClassName</code>`

### Navigation Elements to Skip
- Table of contents (`<nav>`, `<ul class="nav">`)
- Breadcrumbs (`<div class="breadcrumbs">`)
- Sidebar toctree (typically `<div class="toctree">`)
- "Edit on GitHub" / navigation buttons

### Filtering Strategy
```python
# Remove navigation clutter before parsing
for tag in ['nav', 'script', 'link']:
    for elem in soup.find_all(tag):
        elem.decompose()

# For cross-refs, extract href while preserving text
links = soup.find_all('a', class_=['reference internal', 'reference external'])
```

---

## 6. Implementation Best Practices

### Parsing Strategy (KISS)
1. **Use theme-agnostic selectors**: Target semantic tags (`dl`, `dt`, `dd`) over CSS classes when possible
2. **Handle theme variations**: Fallback selectors for Furo, PyData, Alabaster themes
3. **Regex for parsing**: Use regex to extract `**name** (type) – description` patterns from text nodes
4. **Preserve structure**: Map to intermediate dict/dataclass before final output

### Common Patterns to Extract
| Pattern | Regex / Selector |
|---------|------------------|
| Type in parentheses | `\(([^)]+)\)` after param name |
| Description text | Text after " – " separator |
| Code block | `pre > code` inside `div.highlight` |
| Deprecation notice | `<div class="deprecated\|versionadded">` |

### Libraries
- **BeautifulSoup4**: Robust HTML parsing, flexible selectors
- **lxml**: Faster parser backend for BeautifulSoup (optional)
- **cssselect**: CSS selector support (built into BS4)
- **regex**: For complex pattern extraction (not re)

---

## 7. Known Limitations & Workarounds

| Issue | Cause | Workaround |
|-------|-------|-----------|
| Missing type info | Optional in docstring | Extract from inline annotations or accept null |
| Inconsistent structure | Multiple Sphinx versions | Inspect actual HTML; provide version hint |
| Theme-specific classes | Theme variations | Use semantic HTML + fallback selectors |
| Cross-ref resolution | Links only in rendered HTML | Store href separately; resolve post-parse |
| Code block escaping | HTML entities | Use `.get_text()` or `.string` (BS4 auto-decodes) |

---

## Sources & References

- [Sphinx Documentation - Getting Started](https://www.sphinx-doc.org/en/master/usage/quickstart.html)
- [Sphinx autodoc Extension](https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html)
- [Describing Code in Sphinx](https://www.sphinx-doc.org/en/master/tutorial/describing-code.html)
- [Docutils Document Tree](https://docutils.sourceforge.io/docs/ref/doctree.html)
- [BeautifulSoup 4 Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Read the Docs Sphinx Theme - API Demo](https://sphinx-rtd-theme.readthedocs.io/en/stable/demo/api.html)
- [HTML Definition Lists Reference](https://www.w3resource.com/html/definition-lists/HTML-definition-lists-dl-dt-dd-tags-elements.php)
- [Introduction to Sphinx - Write the Docs](https://www.writethedocs.org/guide/tools/sphinx/)

---

## Unresolved Questions

1. How do different Sphinx themes render field-list items variably? (Recommend version pinning)
2. Which Sphinx versions introduce HTML output changes? (Suggest testing against 4.x, 5.x, 7.x)
3. How to extract type hints from type stubs vs. docstring annotations? (Out of scope for HTML parsing)
