# Missing C#/VB API Extraction - Scope Gap

**Date:** 2026-02-01
**Severity:** High
**Impact:** Incomplete knowledge base coverage

---

## Discovery

User manually verified ProcessNetHelp.CHM contains C# and Visual Basic API documentation, but v6 extraction only processed Python API.

**Evidence:**
- User Guide references: "ProcessNet CSharp", "Visual Basic Project.zip"
- Current extraction: 40,625 files from `Python/` directory only
- Missing: C#/VSTA API documentation entirely

---

## Current v6 Extraction Scope

**Included:**
- Python API: 40,625 HTML files
- 1,803 classes, 9,478 methods, 27,132 properties
- 887 code examples (all Python)
- 23 namespaces

**Missing:**
- C# API documentation
- Visual Basic API documentation
- VSTA (Visual Studio Tools for Applications) examples
- User Guide code samples in C#/VB

---

## Impact Analysis

**Knowledge Base Gaps:**
1. No C# method signatures
2. No VB.NET examples
3. Incomplete for users using .NET languages
4. User Guide tutorials not extracted

**Use Cases Affected:**
- .NET developers using RecurDyn ProcessNet
- VSTA automation scripting
- Multi-language API reference

---

## Root Cause

Parser configured to extract from `output/extracted_chm` which only contains:
- `Python/` directory structure
- `Content/UserGuideFiles/` (HTML format, not processed)
- No separate C# or VSTA API directory

**Possible reasons:**
1. CHM extraction only unpacked Python section
2. C#/VB API in separate CHM file not extracted
3. User Guide mixed content not parsed
4. Parser hardcoded for Python structure only

---

## Recommendations

### Option 1: Extract User Guide Content
- Parse `Content/UserGuideFiles/*.htm`
- Extract C#/VB code blocks
- Add as separate examples in KB

### Option 2: Find C# API CHM
- Check for separate ProcessNetHelp_CSharp.chm
- Extract and process if exists
- Merge with v6 KB

### Option 3: Dual-Language KB
- Maintain separate Python KB (v6)
- Create C#/VB KB (v7)
- API can query both

### Option 4: Enhanced Parser
- Update parser to handle User Guide format
- Extract multi-language examples
- Tag by language (python/csharp/vb)

---

## Next Steps

**Immediate:**
1. Check original CHM files for C# API sections
2. Determine if User Guide is only C# source
3. Estimate C# API size/complexity

**Short-term:**
4. Create v7 plan for C#/VB extraction
5. Update parser to support User Guide format
6. Add language tagging to examples

**Long-term:**
7. Multi-language KB with query filtering
8. Cross-reference Python↔C# APIs
9. Unified documentation generation

---

## Lessons Learned

1. **Scope validation:** Should have verified CHM contents before claiming "100% extraction"
2. **Multi-language support:** RecurDyn supports Python, C#, VB - need all three
3. **User testing:** User caught gap by manual inspection
4. **Documentation completeness:** Can't declare complete without all languages

---

## Unresolved Questions

1. Is there a separate C# API CHM file?
2. How much C# content is in User Guide vs dedicated API docs?
3. Are C# and Python APIs identical or have differences?
4. What percentage of users use C#/VB vs Python?
5. Should we block v6 deployment until C# included?
