# API Documentation Structure & Parser Requirements Research

**Date:** 2026-01-31
**Researcher:** researcher agent
**Topic:** ProcessNet API documentation HTML patterns and validation strategies

---

## Executive Summary

Current parser targets Sphinx-generated HTML with definition list (DL/DT/DD) structure. Needs enhancement for:
- Method signature parameter extraction
- Return type parsing
- Class property documentation
- Cross-reference resolution

---

## 1. Current Parser Capabilities

### HTML Structure Recognition

**Supported Patterns:**

| Pattern | HTML Structure | Extraction Method |
|---------|---------------|-------------------|
| Title | `<title>`, `<h1>` | `extract_title()` |
| Methods | `<dl><dt class="sig">` | `extract_method_signatures()` |
| Code Examples | `<div class="highlight"><pre>` | `extract_code_blocks()` |
| Interfaces | Text matching KNOWN_INTERFACES | `extract_interfaces_from_code()` |

### Current Extraction Logic

```python
# Method signature extraction (lines 227-250)
def extract_method_signatures(self, soup: BeautifulSoup) -> list:
    for dl in soup.find_all('dl'):
        for dt in dl.find_all('dt', recursive=False):
            sig_text = dt.get_text(strip=True)
            if '(' in sig_text and ')' in sig_text:
                # Extract method name only: r'(\w+)\s*\('
                # Description: next sibling <dd>
```

**Limitations:**
- Only extracts method name (not parameters)
- No return type parsing
- No parameter type/name extraction
- Assumes simple signature format

### Known Interfaces List

```python
KNOWN_INTERFACES = [
    'IApplication', 'IModelDocument', 'IPlotDocument', 'ISubSystem',
    'IBody', 'IReferenceFrame', 'IMarker', 'IJoint', 'IForce',
    'IGeometry', 'IRequest', 'IResult', 'IContact', 'IConstraint',
    'ISpring', 'IDamper', 'IMotion', 'ISensor', 'IExpression',
    'IRecurDynApp', 'RDApplication'
]
```

**Gap:** Missing comprehensive ProcessNet interface catalog

---

## 2. Expected HTML Patterns for C#/.NET API Docs

### Common Sphinx HTML Structure for API Documentation

```
Documentation Structure:
├── Index: <div class="toctree-wrapper">
├── Namespace: <h1>ProcessNet.Model</h1>
├── Class: <span class="sig-prename">ProcessNet.Model</span><span class="sig-name">Body</span>
├── Methods: <dl class="method">
│   ├── <dt class="sig sig-object">MethodName(paramType paramName)</dt>
│   └── <dd>Method description</dd>
└── Examples: <div class="highlight-csharp"><pre>code</pre></div>
```

### Expected C# Method Signature Patterns

**Pattern 1: Simple Method**
```html
<dt class="sig sig-object py">
    <span class="sig-prename">ReturnType</span>
    <span class="sig-name">MethodName</span>
    <span class="sig-paren">(</span>
    <span class="sig-param">ParamType paramName</span>
    <span class="sig-paren">)</span>
</dt>
<dd>Method description</dd>
```

**Pattern 2: Property**
```html
<dt class="sig sig-object">
    <span class="sig-name">PropertyName</span>
    <span class="sig-type">: PropertyType</span>
</dt>
<dd>Property description, read-only status</dd>
```

**Pattern 3: Class Definition**
```html
<dl class="class">
    <dt class="sig sig-object py">
        <span class="sig-prename">class</span>
        <span class="sig-name">ClassName</span>
        <span class="sig-paren">(</span>
        <em class="sig-param">BaseClass</em>
        <span class="sig-paren">)</span>
    </dt>
    <dd>Class description</dd>
</dl>
```

### Parameter Extraction Requirements

**Target Data:**
- Parameter name: `paramName`
- Parameter type: `ParamType`
- Default value: `= defaultValue`
- Description: from `<dd>` or inline comments

**Regex Pattern:**
```python
# Match: TypeName paramName, TypeName paramName = defaultValue
param_pattern = r'(\w+(?:<[\w\s,]+>)?)\s+(\w+)(?:\s*=\s*([^,)]+))?'
```

### Return Type Extraction

**Strategies:**
1. Parse from `<span class="sig-prename">` before method name
2. Extract from signature text before first space
3. Look for "Returns:" in description `<dd>`

---

## 3. Validation Methods

### Extraction Accuracy Validation

**Metrics:**
```
1. Parse Success Rate: % files processed without errors
2. Method Detection Rate: % expected methods found
3. Parameter Completeness: % methods with full parameter info
4. Code Example Coverage: % methods with examples
5. Namespace Accuracy: % correctly classified
```

### Test Strategy (from existing test suite)

**Sample File Types:**
```python
sample_types = {
    "index": "Overview/TOC structure",
    "namespace": "Namespace-level documentation",
    "class": "Class definition with methods",
    "methods": "Detailed method documentation",
    "examples": "Tutorial/example documentation"
}
```

**Validation Approaches:**

1. **Count-Based Validation** (±20% tolerance)
   - Method count per file
   - Parameter count per method
   - Code block count per example file

2. **Format Validation**
   - Signature contains parentheses: `r'\([^)]*\)'`
   - Signature pattern matching: `r'\w+\s*\([^)]*\)'`
   - Code blocks have `<pre>` tag

3. **Content Validation**
   - Title extraction accuracy
   - Namespace detection (ProcessNet.Model, ProcessNet.Geometry)
   - Interface reference presence

### Coverage Metrics

**Target Coverage:**
```
Minimum Viable:
- 80% files parsed successfully
- 90% method signatures extracted
- 60% parameter information extracted
- 50% code examples extracted

Optimal:
- 95% files parsed successfully
- 98% method signatures extracted
- 90% parameter information extracted
- 80% code examples extracted
- 100% namespace classification accuracy
```

---

## 4. Enhanced Parser Requirements

### Priority Enhancements

**High Priority:**
1. Parameter extraction from signatures
2. Return type parsing
3. Class/namespace structure preservation
4. Property documentation extraction

**Medium Priority:**
5. Cross-reference link resolution
6. Exception documentation
7. Enum value extraction
8. Event handler documentation

**Low Priority:**
9. Inheritance hierarchy mapping
10. Interface implementation tracking
11. Extension method detection
12. Attribute documentation

### New Data Structure Requirements

```python
@dataclass
class Parameter:
    name: str
    type: str = ""              # ENHANCE: Currently empty
    description: str = ""        # ENHANCE: Currently empty
    default: Optional[str] = None # ENHANCE: Currently unused
    is_optional: bool = False    # NEW
    is_out: bool = False         # NEW

@dataclass
class Method:
    name: str
    signature: str = ""
    description: str = ""
    parameters: list = field(default_factory=list) # ENHANCE: Populate
    returns: str = ""            # ENHANCE: Currently empty
    return_description: str = "" # NEW
    exceptions: list = field(default_factory=list) # NEW
    is_static: bool = False      # NEW
    is_async: bool = False       # NEW
    access_modifier: str = ""    # NEW (public/private/protected)
```

---

## 5. Testing Recommendations

### Unit Test Enhancements

**New Test Cases:**
```python
def test_parameter_extraction():
    """Verify parameter names and types extracted correctly."""

def test_return_type_extraction():
    """Verify return type parsed from signature."""

def test_optional_parameters():
    """Verify optional parameters detected (default values)."""

def test_property_read_only_detection():
    """Verify property read-only status from description."""

def test_namespace_hierarchy():
    """Verify parent-child namespace relationships."""
```

### Integration Test Enhancements

**End-to-End Validation:**
```python
def test_full_extraction_workflow():
    """Run complete extraction and validate JSON structure."""

def test_query_interface_accuracy():
    """Test search returns correct methods/classes."""

def test_markdown_generation():
    """Validate markdown output completeness."""
```

### Regression Tests

**Parser Adjustment Protection:**
- Baseline extraction fixtures
- Signature format regression tests
- Parameter count regression tests
- Code example regression tests

---

## 6. Unresolved Questions

1. **CHM Internal Format:** What's the actual HTML structure inside ProcessNetHelp.chm?
   - Needs: Extract CHM and analyze 5-10 sample files

2. **Signature Format:** Are method signatures in Sphinx format or custom Microsoft format?
   - Needs: Examine actual `<dt>` class attributes

3. **Parameter Documentation:** Are parameters documented inline or in separate `<dd>` blocks?
   - Needs: Check for nested `<dl>` within method descriptions

4. **Cross-References:** How are type links represented (relative paths, anchors)?
   - Needs: Examine `href` patterns in documentation

5. **Code Examples:** Are code examples language-tagged (class="highlight-csharp")?
   - Needs: Verify language detection logic matches actual HTML

6. **Property Syntax:** How are read-only properties indicated in the HTML?
   - Needs: Check for `{ get; }` patterns or "read-only" text

7. **Namespace Structure:** Are namespaces organized as separate HTML files or sections?
   - Needs: Map file hierarchy to namespace hierarchy

---

## 7. Recommended Next Steps

### Immediate Actions

1. **Extract Sample CHM** (5-10 representative files)
2. **Analyze HTML Structure** (document actual class/ID patterns)
3. **Create Test Fixtures** (baseline HTML for regression tests)
4. **Enhance Parser** (add parameter/return type extraction)
5. **Expand Test Suite** (new test cases for enhanced features)

### Research Sources

- [MDN Web Docs - Description List Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dl)
- [Microsoft Docs - C# XML Documentation Tags](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags)
- [Sphinx Documentation - Configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html)
- [Stack Overflow - Sphinx Method Signatures](https://stackoverflow.com/questions/56026941/customizing-methods-signature-in-sphinx)

---

**Report End**
