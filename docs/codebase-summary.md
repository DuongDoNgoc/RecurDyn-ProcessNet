# RecurDyn ProcessNet - Codebase Summary

**Date:** 2026-01-28
**Version:** 1.0
**Total Files:** 13 files
**Total Tokens:** 34,536 tokens
**Total Characters:** 148,271 characters

## Executive Summary

The RecurDyn ProcessNet Knowledge Base Extraction project is a Python-based documentation extraction and query system. It transforms proprietary RecurDyn API documentation (HTML/CHM format) into a structured, searchable knowledge base with JSON storage, Markdown export, and interactive CLI interface.

**Primary Purpose:** Enable AI-assisted automation development for RecurDyn ProcessNet API by providing accurate, queryable API documentation.

**Code Statistics:**
- Python source files: 2 (1,056 lines total)
- Documentation files: 11
- Main parser: 475 lines
- Query interface: 581 lines

## Project Structure

```
RecurDyn-ProcessNet/
├── README.md                                # Project overview and quick start
├── requirements.txt                         # Python dependencies (13 lines)
│
├── ProcessNet_Extraction_Requirements.md    # Detailed technical requirements (1,136 lines)
├── ProcessNet_Hybrid_Verification_Workflow.md # Verification protocol (741 lines)
│
├── docs/                                    # Project documentation
│   ├── project-overview-pdr.md              # Product Development Requirements
│   ├── code-standards.md                    # Code standards and conventions
│   ├── codebase-summary.md                  # This file
│   ├── system-architecture.md               # Architecture documentation
│   ├── project-roadmap.md                   # Development roadmap
│   └── tech-stack.md                        # Technology stack (97 lines)
│
├── src/                                     # Source code
│   ├── recurdyn-doc-parser.py               # HTML/CHM parser (475 lines)
│   └── processnet-query-interface.py        # Query interface (581 lines)
│
├── knowledge/                               # Source documentation (not in repo)
│   ├── ProcessNetHelp.chm                   # CHM file to extract
│   ├── RecurDynHelp/                        # Sphinx HTML documentation
│   └── Tutorial/                            # Tutorial HTML files
│
└── output/                                  # Generated outputs (not in repo)
    ├── extracted_chm/                       # Extracted CHM contents
    ├── processnet_knowledge.json            # Main knowledge base
    └── markdown/                            # Generated markdown docs
```

## Core Components

### 1. Documentation Parser (`recurdyn-doc-parser.py`)

**Purpose:** Extract API documentation from HTML files and build structured knowledge base.

**Lines of Code:** 475

**Key Classes:**

- **ProcessNetDocParser** - Main parser class
  - `discover_files()` - Recursively find all HTML files
  - `detect_encoding()` - Auto-detect file encoding
  - `parse_html_file()` - Extract content from single file
  - `build_knowledge_base()` - Process all files
  - `save_knowledge_base()` - Export to JSON
  - `generate_markdown()` - Create markdown docs

**Data Structures:**

```python
@dataclass
class Parameter:
    """Method parameter with name, type, description"""
    name: str
    type: str = ""
    description: str = ""
    default: Optional[str] = None

@dataclass
class Method:
    """Method/function with signature, parameters, return type"""
    name: str
    signature: str = ""
    description: str = ""
    parameters: list = field(default_factory=list)
    returns: str = ""
    example_code: str = ""
    source_file: str = ""

@dataclass
class Property:
    """Class property with type and read-only flag"""
    name: str
    type: str = ""
    description: str = ""
    read_only: bool = False
    source_file: str = ""

@dataclass
class ClassDef:
    """Class definition with inheritance, methods, properties"""
    name: str
    description: str = ""
    inheritance: str = ""
    methods: list = field(default_factory=list)
    properties: list = field(default_factory=list)
    source_file: str = ""

@dataclass
class CodeExample:
    """Code example with title, code, language"""
    title: str = ""
    code: str = ""
    language: str = "csharp"
    description: str = ""
    source_file: str = ""

@dataclass
class Namespace:
    """Namespace container for classes and methods"""
    name: str
    full_name: str = ""
    description: str = ""
    classes: list = field(default_factory=list)
    standalone_methods: list = field(default_factory=list)
    examples: list = field(default_factory=list)
    files: list = field(default_factory=list)
```

**Key Constants:**

- `KNOWN_INTERFACES` - List of ProcessNet interfaces to detect
- `EXCLUDE_PATTERNS` - File/directory patterns to skip

**Parsing Strategies:**

1. **Definition Lists** - Extract from `<dl>`, `<dt>`, `<dd>` elements
2. **Table-Based** - Parse API documentation tables
3. **Heading + Paragraph** - Handle heading-based documentation
4. **Code Blocks** - Extract examples from `<div class="highlight">`, `<pre>`, `<code>`

**Output Structure:**

```json
{
  "metadata": {
    "source": "RecurDyn ProcessNet API",
    "version": "extracted",
    "extraction_date": "ISO8601",
    "total_files_processed": 0,
    "extraction_duration_seconds": 0
  },
  "namespaces": {
    "ProcessNet": {
      "full_name": "FunctionBay.RecurDyn.ProcessNet",
      "description": "RecurDyn ProcessNet API for automation",
      "classes": [],
      "standalone_methods": [],
      "examples": [],
      "files": []
    }
  },
  "method_index": {},
  "class_index": {},
  "interface_index": {}
}
```

### 2. Query Interface (`processnet-query-interface.py`)

**Purpose:** Provide search and query functionality for the knowledge base.

**Lines of Code:** 581

**Key Classes:**

- **ProcessNetKnowledge** - Query interface main class
  - `_load_knowledge_base()` - Load JSON and build indices
  - `_build_indices()` - Create search indices
  - `find_method()` - Exact method lookup
  - `search_method_fuzzy()` - Fuzzy search with RapidFuzz
  - `search_by_description()` - Full-text description search
  - `list_namespace_contents()` - Browse namespace
  - `list_namespaces()` - Get all namespaces
  - `find_examples()` - Find code examples
  - `get_statistics()` - Knowledge base stats

- **SearchResult** - Search result dataclass
  ```python
  @dataclass
  class SearchResult:
      name: str
      type: str  # 'method', 'class', 'interface', 'example'
      namespace: str
      signature: str = ""
      description: str = ""
      code: str = ""
      source_file: str = ""
      score: float = 100.0
  ```

**Search Capabilities:**

| Search Type | Method | Description | Performance |
|-------------|--------|-------------|-------------|
| Exact Lookup | `find_method()` | Case-insensitive exact match | O(1) |
| Fuzzy Search | `search_method_fuzzy()` | RapidFuzz approximate matching | O(n log n) |
| Description Search | `search_by_description()` | Full-text in descriptions | O(n) |
| Namespace Browse | `list_namespace_contents()` | List namespace hierarchy | O(1) |
| Example Finder | `find_examples()` | Find code by keyword | O(n) |

**Interactive CLI Commands:**

```
search <query>     - Fuzzy search for methods/interfaces
find <method>      - Exact method lookup
desc <keywords>    - Search by description
list <namespace>   - List namespace contents
namespaces         - List all namespaces
examples [keyword] - Find code examples
stats              - Show statistics
help               - Show help
quit               - Exit
```

**Output Formats:**

- **Console** - Formatted text output
- **JSON** - Machine-readable output (via `--json` flag)

## Technology Stack

### Python Runtime

- **Python 3.10+** - Required runtime version

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| beautifulsoup4 | >=4.12.0 | HTML parsing |
| lxml | >=5.0.0 | Fast parser backend |
| rapidfuzz | >=3.0.0 | Fuzzy string matching |
| chardet | >=5.0.0 | Encoding detection |

### System Tools

| Tool | Purpose |
|------|---------|
| libchm-bin | Primary CHM extraction |
| p7zip-full | Fallback CHM extraction |

See [docs/tech-stack.md](tech-stack.md) for detailed technology stack information.

## Key Design Patterns

### 1. Dataclass-Based Data Structures

All data structures use Python `@dataclass` decorators for:
- Automatic `__init__`, `__repr__`, `__eq__` methods
- Type hints for clarity
- Easy serialization with `asdict()`

### 2. Progressive Parsing

Multiple parsing strategies with fallback:
1. Try definition list parsing
2. Fallback to table-based parsing
3. Fallback to heading + paragraph parsing

### 3. Index-Based Query

Pre-computed indices for fast lookup:
- `method_index` - Method name → namespaces mapping
- `class_index` - Class name → namespaces mapping
- `interface_index` - Interface name → namespaces mapping

### 4. Graceful Degradation

Error handling strategy:
- Individual file errors don't stop processing
- Errors logged with file path and reason
- Processing continues to next file
- Summary report at end

## File Discovery Algorithm

### Recursive Directory Walk

```python
def discover_files(self) -> list:
    """Discover all documentation files recursively."""
    all_files = []
    extensions = ['.html', '.htm']

    for path in self.input_path.rglob('*'):
        if path.suffix.lower() in extensions:
            skip = False
            for pattern in self.EXCLUDE_PATTERNS:
                if pattern in str(path):
                    skip = True
                    break
            if not skip:
                all_files.append(path)

    return sorted(all_files)
```

**Exclusion Patterns:**
- `_static` - Static assets
- `_images` - Image directories
- `assets` - Asset directories
- `css` - Stylesheet directories
- `js` - JavaScript directories
- `_sources` - Sphinx source files
- `.git` - Version control
- `__pycache__` - Python cache

## Encoding Detection Strategy

### Fallback Chain

1. **Primary**: chardet auto-detection
2. **Fallback**: UTF-8
3. **Fallback**: Windows-1252 (common on Windows)
4. **Fallback**: Latin-1 (never fails)

```python
def detect_encoding(self, file_path: Path) -> str:
    """Detect file encoding."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10000)
        result = chardet.detect(raw_data)
        return result.get('encoding', 'utf-8') or 'utf-8'
```

## Content Extraction Logic

### Method Signature Extraction

```python
def extract_method_signatures(self, soup: BeautifulSoup) -> list:
    """Extract method signatures from definition lists."""
    methods = []

    # Look for definition lists (common in Sphinx docs)
    for dl in soup.find_all('dl'):
        for dt in dl.find_all('dt', recursive=False):
            sig_text = dt.get_text(strip=True)
            # Check if it looks like a method signature
            if '(' in sig_text and ')' in sig_text:
                dd = dt.find_next_sibling('dd')
                description = dd.get_text(strip=True) if dd else ""

                # Parse method name
                match = re.match(r'(\w+)\s*\(', sig_text)
                if match:
                    method_name = match.group(1)
                    methods.append(Method(
                        name=method_name,
                        signature=sig_text,
                        description=description[:500]
                    ))

    return methods
```

### Code Example Extraction

```python
def extract_code_blocks(self, soup: BeautifulSoup, source_file: str) -> list:
    """Extract code examples from HTML."""
    examples = []

    # Find code blocks in highlight divs
    for highlight in soup.find_all('div', class_='highlight'):
        pre = highlight.find('pre')
        if pre:
            code = pre.get_text()
            # Detect language from class
            lang = 'csharp'
            for cls in highlight.get('class', []):
                if 'python' in cls.lower():
                    lang = 'python'
                elif 'c#' in cls.lower() or 'csharp' in cls.lower():
                    lang = 'csharp'

            # Check if code contains ProcessNet-related content
            if any(iface in code for iface in self.KNOWN_INTERFACES) or \
               'FunctionBay.RecurDyn' in code or 'ProcessNet' in code:
                examples.append(CodeExample(
                    code=code.strip(),
                    language=lang,
                    source_file=source_file
                ))

    return examples
```

## Query Implementation

### Exact Method Lookup

```python
def find_method(self, method_name: str, namespace: Optional[str] = None) -> list:
    """Find method by exact name match (case-insensitive)."""
    results = []
    method_lower = method_name.lower()

    # Search in method index (O(1) lookup)
    if method_lower in self.kb.get('method_index', {}):
        namespaces = self.kb['method_index'][method_lower]
        for ns in namespaces:
            if namespace and ns.lower() != namespace.lower():
                continue

            # Find the method in namespace data
            ns_data = self.kb['namespaces'].get(ns, {})
            for method in ns_data.get('standalone_methods', []):
                if method['name'].lower() == method_lower:
                    results.append(SearchResult(
                        name=method['name'],
                        type='method',
                        namespace=ns,
                        signature=method.get('signature', ''),
                        description=method.get('description', ''),
                        source_file=method.get('source_file', '')
                    ))

    return results
```

### Fuzzy Search with RapidFuzz

```python
def search_method_fuzzy(self, query: str, threshold: float = 60.0, limit: int = 10) -> list:
    """Search for methods using fuzzy string matching."""
    if not FUZZY_AVAILABLE:
        # Fallback to simple substring matching
        return self._search_substring(query, limit)

    results = []

    # Search in method names
    if self._method_names:
        matches = process.extract(
            query.lower(),
            self._method_names,
            scorer=fuzz.WRatio,
            limit=limit
        )

        for match_name, score, _ in matches:
            if score >= threshold:
                # Get full method info
                method_results = self.find_method(match_name)
                for r in method_results:
                    r.score = score
                    results.append(r)

    # Sort by score and remove duplicates
    seen = set()
    unique_results = []
    for r in sorted(results, key=lambda x: x.score, reverse=True):
        key = (r.name.lower(), r.type)
        if key not in seen:
            seen.add(key)
            unique_results.append(r)

    return unique_results[:limit]
```

## Performance Characteristics

### Extraction Performance

- **Target Speed**: <5 minutes for 500 HTML files
- **Memory Usage**: <500 MB peak
- **Throughput**: ~1-2 files/second

### Query Performance

- **Exact Lookup**: O(1) - <10ms
- **Fuzzy Search**: O(n log n) - <100ms
- **Description Search**: O(n) - <100ms
- **Namespace Browse**: O(1) - <10ms

## Known Limitations

### HTML Structure Assumptions

- Assumes Sphinx/ReadTheDocs documentation format
- Definition list structure for methods
- Code blocks in `<div class="highlight">`
- May fail on non-standard HTML structures

### Encoding Coverage

- Handles common encodings (UTF-8, Windows-1252, Latin-1)
- May fail on rare encodings
- Fallback to Latin-1 may produce incorrect characters

### CHM Extraction

- Requires system tools (libchm-bin, p7zip-full)
- May not work on all platforms
- Some CHM files may be corrupted or password-protected

### JavaScript Content

- Does not execute JavaScript
- Cannot extract dynamically loaded content
- Limited to static HTML extraction

## Integration Points

### For Claude Code / AI Assistants

```python
# Load knowledge base
from processnet_query_interface import ProcessNetKnowledge

kb = ProcessNetKnowledge("output/processnet-knowledge.json")

# Find method
methods = kb.find_method("CreateArc")
print(methods[0].signature)

# Search by description
doe_methods = kb.search_by_description("design of experiments")

# Get namespace contents
geom = kb.list_namespace_contents("ProcessNet.Geometry")
```

### For Automation Scripts

```python
# Query API before writing code
kb = ProcessNetKnowledge("processnet_knowledge.json")

# Find correct method signature
load_method = kb.find_method("Load")
print(load_method[0].signature)  # "Load(filePath: str) -> Model"

# Find examples
examples = kb.find_examples("geometry")
print(examples[0]['code'])
```

## Testing Strategy

### Unit Testing

- Test individual parsing functions
- Validate dataclass serialization
- Test encoding detection

### Integration Testing

- Full extraction workflow
- Query interface accuracy
- Markdown generation

### Use Case Validation

Test all 3 target workflows:
1. **DOE Batch Execution** - Verify parameter manipulation methods
2. **Model Introspection** - Verify entity enumeration methods
3. **Result Processing** - Verify result loading methods

## Future Enhancements

### Potential Improvements

1. **Parallel Processing** - Use multiprocessing for large file sets
2. **Incremental Updates** - Only process changed files
3. **Version Tracking** - Track API changes across RecurDyn versions
4. **Type Inference** - Infer parameter types from usage patterns
5. **Cross-Reference Linking** - Build relationship graph between classes/methods
6. **Web Interface** - Browser-based query interface
7. **API Server** - REST API for knowledge base queries
8. **IDE Integration** - VS Code extension for autocomplete

### Scalability Considerations

- **Large Documentation Sets**: Implement streaming for files >10MB
- **Frequent Updates**: Add incremental extraction mode
- **Multiple Versions**: Support side-by-side API versions
- **Distributed Processing**: Support cluster-based extraction

## Documentation Standards

### Code Documentation

- All functions have docstrings
- Type hints on all function signatures
- Examples in docstrings for complex functions
- Inline comments for non-obvious logic

### File Naming

- Use kebab-case for file names
- Descriptive names that indicate purpose
- No abbreviations (except well-known ones)

### Commit Messages

- Conventional commit format
- Prefix with type: feat, fix, docs, refactor, test
- Clear description of changes

## Related Documents

- [README.md](../README.md) - Project overview
- [docs/project-overview-pdr.md](project-overview-pdr.md) - Product Development Requirements
- [docs/code-standards.md](code-standards.md) - Code standards
- [docs/system-architecture.md](system-architecture.md) - Architecture details
- [docs/tech-stack.md](tech-stack.md) - Technology stack
- [ProcessNet_Extraction_Requirements.md](../ProcessNet_Extraction_Requirements.md) - Technical requirements

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial codebase summary |

---

**Generated from:** repomix-output.xml (34,536 tokens, 148,271 characters)
**Last Updated:** 2026-01-28
**Maintainer:** Development Team
