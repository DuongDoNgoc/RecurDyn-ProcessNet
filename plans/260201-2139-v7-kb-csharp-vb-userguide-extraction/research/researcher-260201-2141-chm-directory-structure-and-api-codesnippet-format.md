# CHM Structure Analysis: C#/VB Content Organization

**Date:** 2026-02-01
**Extracted CHM Root:** `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/extracted_chm/`

---

## Executive Summary

The extracted CHM contains **two distinct content sources**:

1. **API Documentation (HTML):** 21,274 files in `html/` directory (184 MB) - C#/VB syntax-aware
2. **User Guide (Word-converted HTML):** 7 files in `Content/UserGuideFiles/` (3.2 MB) - MS Office HTML format
3. **Python Examples:** 91 MB in `Python/` directory (out of scope for this task)

---

## Directory Structure

```
/output/extracted_chm/
├── html/                         # 21,274 .htm files (184 MB)
│   ├── 0005763a-dab6-...         # API reference pages (namespaces, classes, enums, interfaces)
│   └── [UUIDs].htm               # Each is a single API entity page
├── Content/UserGuideFiles/       # 7 .htm files (3.2 MB) + 6 .files/ dirs
│   ├── ProcessNet User Guide1.htm # ~215 KB
│   ├── ProcessNet User Guide2.htm # ~47 KB
│   ├── ProcessNet User Guide3.htm # ~101 KB
│   ├── ProcessNet User Guide4.htm # ~277 KB (largest)
│   ├── ProcessNet User Guide5.htm # ~67 KB
│   ├── ProcessNet User Guide6.htm # ~28 KB
│   └── ProcessNet User Guide7.htm # ~14 KB
├── Python/                       # 91 MB (Python-only content)
├── styles/                       # CSS (branding, Help1, HelpViewer, localization)
├── icons/                        # PNG images (alerts, code examples)
├── scripts/                      # branding.js, highlight.js
└── [metadata files]              # #SYSTEM, #STRINGS, #IDXHDR, etc.
```

---

## HTML API Documentation (`html/` directory)

### Structure & Characteristics

- **File Count:** 21,274 unique HTML files
- **Format:** UTF-8 HTML with BOM, CRLF line terminators, very long lines (2410+ chars)
- **Namespace:** `FunctionBay.Post.ProcessNet.*` and `FunctionBay.RecurDyn.ProcessNet.*`
- **Content Types:** Enumerations, interfaces, properties, methods
- **Example:** ContourLegendPosition Enumeration
  - Namespace: `FunctionBay.Post.ProcessNet`
  - Assembly: `FunctionBay.Post.ProcessNet.Interface.dll v10.2.0.0`

### C#/VB Code Samples: Syntax Tab Pattern

API docs use **collapsible syntax tabs** to display C# and VB code side-by-side:

```html
<div class="codeSnippetContainerTabs">
  <div id="[ID]_tab1" class="codeSnippetContainerTab">
    <a href="#" onclick="javascript:ChangeTab('[ID]','cs','1','2');return false;">C#</a>
  </div>
  <div id="[ID]_tab2" class="codeSnippetContainerTab">
    <a href="#" onclick="javascript:ChangeTab('[ID]','vb','2','2');return false;">VB</a>
  </div>
</div>

<!-- C# Code (display: block) -->
<div id="[ID]_code_Div1" class="codeSnippetContainerCode" style="display: block">
  <pre xml:space="preserve">
    <span class="keyword">public</span> <span class="keyword">enum</span> <span class="identifier">ContourLegendPosition</span>
  </pre>
</div>

<!-- VB Code (display: none, shown via JavaScript) -->
<div id="[ID]_code_Div2" class="codeSnippetContainerCode" style="display: none">
  <pre xml:space="preserve">
    <span class="keyword">Public</span> <span class="keyword">Enumeration</span> <span class="identifier">ContourLegendPosition</span>
  </pre>
</div>
```

**Extraction Strategy:**
- Parse `.codeSnippetContainerCode` divs with IDs matching pattern `*_code_Div1` (C#) and `*_code_Div2` (VB)
- Extract `<pre>` content, strip `<span>` tags or preserve semantic markup
- Link code samples to parent namespace/class via metadata `<meta name="container">` or `<meta name="Microsoft.Help.F1">`

---

## User Guide Content (`Content/UserGuideFiles/` directory)

### Structure & Characteristics

- **File Count:** 7 HTML files (segmented document)
- **Format:** Microsoft Word 15 HTML Export (with embedded Office XML namespaces)
- **Encoding:** KS_C_5601-1987 (Korean/CJK)
- **Size Distribution:**
  - Guide1: 215 KB (largest single file)
  - Guide4: 277 KB (largest overall)
  - Guide2, 6, 7: Small files (14-47 KB)
- **Supporting:** 6 `.files/` directories contain images, stylesheets, theme data

### HTML Structure (Word-Converted)

```html
<html xmlns:v="urn:schemas-microsoft-com:vml"
      xmlns:o="urn:schemas-microsoft-com:office:office"
      xmlns:w="urn:schemas-microsoft-com:office:word"
      xmlns:m="http://schemas.microsoft.com/office/2004/12/omml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=ks_c_5601-1987">
    <meta name="Generator" content="Microsoft Word 15">
    <style>
      [Heavy MSO-specific CSS with @font-face definitions for Korean fonts]
    </style>
  </head>
  <body>
    [Content with h1, h2, h3 styles]
  </body>
</html>
```

**Word Export Artifacts:**
- MSO-specific CSS properties (`mso-style-`, `mso-font-`, `mso-pagination-`)
- Office namespaced elements (`v:*, o:*, w:*`)
- Embedded theme/color data in `.files/` subdirectories
- Legacy IE compatibility directives (`<!--[if gte mso 9]>`)

### Content Segmentation

7-file structure suggests **chapter or section-based split**:
- Guide1: Likely intro/getting started (largest content)
- Guide4: Major feature section (277 KB)
- Guide2, 3, 5, 6, 7: Support/reference sections

**No C#/VB code detected** in sample inspection. User Guide appears **language-agnostic** (setup, usage workflows, UI navigation).

---

## Parser Design Implications

### For C#/VB API Extraction (html/):

1. **Parsing Strategy:**
   - Use BeautifulSoup4 or lxml to parse 21K+ files
   - Target `<meta name="container">` for namespace classification
   - Extract both code variants from `*_code_Div1` (C#) and `*_code_Div2` (VB)
   - Use `<meta name="Microsoft.Help.F1">` for cross-reference mapping

2. **Performance:**
   - Parallelize file processing (21K files, 184 MB)
   - Stream parse instead of loading entire DOM
   - Filter to relevant namespaces upfront (skip unrelated content)

3. **Data Model:**
   - Namespace → Classes/Interfaces/Enums
   - Member → C# + VB syntax pair
   - Semantic markup: keyword spans for syntax highlighting

### For User Guide Extraction (Content/UserGuideFiles/):

1. **Parsing Strategy:**
   - Detect and strip MSO-specific CSS/namespaces
   - Extract heading hierarchy (h1-h3) for TOC
   - Preserve body text and images from `.files/` directories
   - Handle Office XML embedded in comments/attributes

2. **Encoding Handling:**
   - Normalize KS_C_5601-1987 encoding upfront
   - May contain CJK characters; preserve unicode

3. **Output:**
   - Structured markdown with sections
   - Asset references to image files in `.files/`

---

## Summary Table

| Aspect | API Docs (html/) | User Guide (Content/) |
|--------|------------------|-----------------------|
| **File Count** | 21,274 | 7 |
| **Total Size** | 184 MB | 3.2 MB |
| **Languages** | C#, VB (tabbed) | N/A (generic) |
| **Format** | XHTML/HTML5 | Word 15 HTML Export |
| **Parser Type** | Semantic HTML + JS tab logic | Word HTML cleanup + markdown |
| **Extraction Focus** | Code + metadata | Structure + text |

---

## Unresolved Questions

1. Are the 7 User Guide files **sequential chapters** or separate documents? (Suggest: inspect TOC/metadata)
2. Does User Guide contain **programmatic references** to API namespaces? (Need: full-text search)
3. What **localization variants** exist? (Styles dir has `branding-*-*.css` for multiple locales)
4. Should **Python directory** (91 MB) be included in v7 KB scope, or Python-only for v6?

