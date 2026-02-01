# CHM Extraction Methods Research

**Date:** 2026-01-31
**Researcher:** Agent researcher-01
**Topic:** CHM file extraction tools and methods for Windows/Linux

---

## CHM Format Overview

CHM = **Microsoft Compiled HTML Help** - proprietary format containing:
- Compiled HTML pages
- Hyperlinked table of contents
- Index system
- Used for Windows software documentation

---

## Windows Extraction Tools

### 1. 7-Zip (Recommended)
- **Free, open-source**
- Command-line extraction: `7z x file.chm -ooutput_dir -y`
- Automated extraction support
- [Download: 7-Zip](https://www.7-zip.org/)

### 2. HTML Help Workshop
- Official Microsoft tool
- Can decompile CHM files
- GUI-based, less automation-friendly

### 3. CHM Decoder
- Dedicated CHM extraction tool
- Simple interface

---

## Linux Extraction Tools

### 1. 7-Zip (p7zip-full)
```bash
sudo apt install p7zip-full
7z x file.chm -o/path/to/output -y
```

### 2. chm2pdf
- Direct CHM → PDF conversion
- Available in package managers
- Good for documentation archiving

### 3. arCHMage
- CHM reader/decompiler v0.2.4
- Extract pages individually
- Combine with wkhtmltopdf for PDF output

### 4. xCHM
- Cross-platform viewer (Windows/Mac/Linux)
- GitHub: [github.com/rzncj/xCHM](https://github.com/rzncj/xCHM)
- Good for viewing, limited extraction

### 5. KchmViewer
- KDE-based CHM viewer
- Excellent language support
- Available in most distro repos

---

## Python Libraries

### PyCHM (Primary)
- **PyPI:** [pypi.org/project/pychm/](https://pypi.org/project/pychm/)
- **GitHub:** [github.com/dottedmag/pychm](https://github.com/dottedmag/pychm)
- Python 3.6+ support
- Bindings for CHMLIB

```bash
pip install pychm
```

**Usage:**
```python
from chm import chm
from chm import chmlib

# Extract HTML content
# Combine with BeautifulSoup for parsing
```

**Maintenance:** Bug fixes only (stable)

---

## Automated Extraction Procedures

### Windows (7-Zip CLI)
```batch
"C:\Program Files\7-Zip\7z.exe" x "C:\path\to\file.chm" -o"C:\output" -y
```

### Linux (7-Zip)
```bash
7z x file.chm -o/path/to/output -y
```

### Python (PyCHM)
```python
from chm import chm
# Extract and parse HTML files programmatically
```

### Batch Processing
```bash
for file in *.chm; do
    7z x "$file" -o"${file%.chm}" -y
done
```

---

## Output Formats

- **HTML:** Native output (best for API docs)
- **PDF:** Via chm2pdf or wkhtmltopdf
- **Plain text:** Via PyCHM + BeautifulSoup
- **XML:** Requires post-processing

---

## File Transfer: WSL ↔ Windows

### WSL Access to Windows
```bash
# Access Windows C: drive from WSL
cd /mnt/c/path/to/chm/files
```

### Windows Access to WSL
```cmd
# From Windows PowerShell/Explorer
\\wsl$\Ubuntu\mnt\...
```

### Git LFS (Large Files)
- For CHM files in version control
- `.gitattributes`: `*.chm filter=lfs diff=lfs merge=lfs -text`

---

## API Documentation Structure

Extracted CHM content typically contains:

### HTML Help Structure
- Table of Contents (TOC)
- Index files
- HTML topic files
- Navigation metadata

### API Reference Patterns
- **Method signatures:** Function/class documentation
- **Parameter descriptions:** Type info, defaults
- **Code examples:** Usage snippets
- **Namespace organization:** Class hierarchies

### Identifying API Docs
- Look for HTML files with:
  - "API", "Reference", "Class" in titles
  - Code blocks with syntax highlighting
  - Method signature formatting
  - Namespace/module hierarchy

---

## Key Findings & Recommendations

### ✅ Recommended Approach
1. **Use 7-Zip** for extraction (cross-platform, automated)
2. **Python + PyCHM** for programmatic parsing
3. **Process on Windows** if possible (native CHM support)
4. **Extract to HTML** (preserves structure & formatting)

### ⚠️ Considerations
- CHM is proprietary - extraction may be restricted
- Some CHM files use encoding (UTF-8 vs system encoding)
- Output HTML may have internal references requiring cleanup
- Large CHM files may require significant disk space

### 🎯 Next Steps
1. Test extraction on sample RecurDyn CHM file
2. Verify encoding handling
3. Identify API doc patterns in output
4. Design parser for extracted HTML content

---

## Sources
- [e7z.org - CHM Extraction](http://www.e7z.org/open-chm.htm)
- [AskUbuntu - CHM Extraction](https://askubuntu.com/questions/28136/how-to-open-and-convert-chm-documents)
- [HelpCreator - CHM Decompilation](https://helpcreator.net/en/index.php/2019/07/28/decompile-extract-chm-files/)
- [xCHM GitHub](https://github.com/rzncj/xCHM)
- [PyCHM on PyPI](https://pypi.org/project/pychm/)
- [PyCHM GitHub](https://github.com/dottedmag/pychm)
- [Microsoft HTML Help API](https://learn.microsoft.com/en-us/previous-versions/windows/desktop/htmlhelp/html-help-api-reference)
- [GOV.UK - API Documentation](https://www.gov.uk/guidance/writing-api-reference-documentation)
- [Zoho - API Documentation Guide](https://www.zoho.com/learn/focalpoint/api-documentation-guide.html)

---

## Unresolved Questions

1. What is the typical size of RecurDyn CHM documentation files?
2. Does RecurDyn use any proprietary CHM extensions?
3. Are there licensing restrictions on extracting RecurDyn docs?
4. What encoding does RecurDyn CHM files use?
5. Does RecurDyn CHM contain embedded binaries (images, code samples)?
