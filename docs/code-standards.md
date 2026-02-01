# RecurDyn ProcessNet - Code Standards and Conventions

**Date:** 2026-02-01
**Version:** 2.0
**Status:** Active

## Overview

This document defines the coding standards and conventions for the RecurDyn ProcessNet Knowledge Base Extraction project. All contributors must follow these standards to maintain code quality, consistency, and maintainability.

## General Principles

### Core Values

1. **YAGNI** (You Aren't Gonna Need It) - Only implement what's needed now
2. **KISS** (Keep It Simple, Stupid) - Simple solutions over clever ones
3. **DRY** (Don't Repeat Yourself) - Avoid code duplication

### Code Quality Goals

- **Readability**: Code should be self-documenting
- **Maintainability**: Easy to modify and extend
- **Testability**: Easy to test individual components
- **Performance**: Meet defined performance targets
- **Reliability**: Handle errors gracefully

## REST API Standards

### API Endpoint Design

**Naming Convention:** RESTful resource-based naming

```
✓ GOOD:
GET  /api/health
GET  /api/stats
GET  /api/namespaces
GET  /api/namespaces/{name}
GET  /api/search?q={query}
GET  /api/find/{name}
GET  /api/examples?keyword={kw}

✗ BAD:
GET  /getNamespaces
POST /searchMethod
GET  /method-details
```

**HTTP Methods:**
- `GET` - Retrieve resources (no side effects)
- `POST` - Create resources (not used in current API)
- `PUT` - Update resources (not used in current API)
- `DELETE` - Delete resources (not used in current API)

### Response Format

**Success Responses:**
- `200 OK` - Successful GET request
- `201 Created` - Successful POST (when implemented)

**Error Responses:**
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `500 Internal Server Error` - Server error

**Response Structure:**
```python
# GOOD - Consistent response structure
{
    "count": 5,
    "results": [
        {
            "name": "CreateArc",
            "type": "method",
            "namespace": "ProcessNet.Geometry",
            "signature": "CreateArc(center, radius, start_angle, end_angle)",
            "description": "Creates circular arc",
            "score": 95.0
        }
    ]
}

# GOOD - Error response
{
    "detail": "Method 'NonExistent' not found in knowledge base"
}
```

### Async/Await Patterns

**Requirement:** Use async/await for all route handlers

```python
# GOOD - Async route handler
from fastapi import FastAPI, HTTPException

@app.get("/api/find/{name}")
async def find_method(name: str, namespace: Optional[str] = None):
    """Find method by exact name match."""
    try:
        results = app.state.kb.find_method(name, namespace)
        if not results:
            raise HTTPException(status_code=404, detail=f"Method '{name}' not found")
        return {"count": len(results), "results": [asdict(r) for r in results]}
    except Exception as e:
        logger.error(f"Error finding method '{name}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

# BAD - Synchronous handler (works but not recommended)
@app.get("/api/find/{name}")
def find_method(name: str):
    # This works but doesn't leverage FastAPI's async capabilities
    results = app.state.kb.find_method(name)
    return results
```

### Pydantic Models

**Requirement:** Use Pydantic for request/response validation

```python
# GOOD - Pydantic models
from pydantic import BaseModel, Field

class MethodResponse(BaseModel):
    """Method response model."""
    name: str = Field(..., description="Method name")
    type: str = Field(..., description="Type: method, class, or example")
    namespace: str = Field(..., description="Namespace containing the method")
    signature: str = Field(default="", description="Method signature")
    description: str = Field(default="", description="Method description")
    score: float = Field(default=100.0, description="Fuzzy match score")

class SearchResponse(BaseModel):
    """Search response model."""
    count: int = Field(..., description="Number of results")
    query: str = Field(..., description="Search query")
    results: list[MethodResponse] = Field(default_factory=list)

# Use in endpoint
@app.get("/api/search", response_model=SearchResponse)
async def search_methods(q: str = Query(..., min_length=1), limit: int = Query(10, ge=1, le=100)):
    """Search for methods using fuzzy matching."""
    results = kb.search_method_fuzzy(q, limit=limit)
    return SearchResponse(count=len(results), query=q, results=results)
```

### CORS Configuration

**Best Practice:** Configure CORS for appropriate origins

```python
# GOOD - Configured CORS
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

### Error Handling

**Pattern:** Use HTTPException for API errors

```python
# GOOD - HTTPException with status codes
from fastapi import HTTPException

@app.get("/api/namespaces/{name}")
async def get_namespace(name: str):
    """Get namespace details."""
    ns_data = app.state.kb.list_namespace_contents(name)
    if not ns_data:
        raise HTTPException(
            status_code=404,
            detail=f"Namespace '{name}' not found"
        )
    return ns_data

# GOOD - Try-except with logging
@app.get("/api/search")
async def search(q: str):
    try:
        results = app.state.kb.search_method_fuzzy(q)
        return {"results": results}
    except Exception as e:
        logger.error(f"Search error for '{q}': {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

### API Documentation

**Automatic Docs:** FastAPI provides automatic OpenAPI docs

```python
# GOOD - Descriptive docstrings
@app.get("/api/stats", response_model=StatsResponse)
async def get_statistics():
    """
    Get knowledge base statistics.

    Returns counts of namespaces, classes, methods, properties,
    and extraction metadata.
    """
    stats = app.state.kb.get_statistics()
    return stats

# Access docs at:
# - http://localhost:8000/docs (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)
```

### Server Lifecycle

**Best Practice:** Use lifespan context manager for startup/shutdown

```python
# GOOD - Lifespan management
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage server lifecycle with singleton KB."""
    # Startup: Load knowledge base
    logger.info("Starting API server...")
    kb_instance = ProcessNetKnowledge(args.kb_path)
    app.state.kb = kb_instance
    logger.info("Knowledge base loaded successfully")
    yield
    # Shutdown: Cleanup
    logger.info("Shutting down API server...")

app = FastAPI(
    title="ProcessNet Knowledge Base API",
    description="REST API for querying RecurDyn ProcessNet API documentation",
    version="1.0.0",
    lifespan=lifespan
)
```

### Integration Testing

**Pattern:** Use httpx for async API testing

```python
# GOOD - Async test with httpx
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_endpoint():
    """Test search endpoint returns results."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/search", params={"q": "save"})
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert len(data["results"]) > 0

@pytest.mark.asyncio
async def test_find_not_found():
    """Test find endpoint returns 404 for non-existent method."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/find/NonExistentMethod")
        assert response.status_code == 404
```

## Python Code Standards

### File Naming

**Convention:** kebab-case with descriptive names

**Examples:**
```
✓ GOOD:
recurdyn-doc-parser.py
processnet-query-interface.py
test-extraction-validation.py

✗ BAD:
parser.py
query.py
test.py
```

**Rationale:** Long, descriptive file names help LLMs understand file purpose without reading content.

### Line Length

**Maximum:** 100 characters (soft limit), 120 characters (hard limit)

**Rationale:** Balances readability with modern screen widths.

```python
# GOOD - Under 100 characters
def extract_method_signatures(self, soup: BeautifulSoup) -> list[Method]:
    """Extract method signatures from definition lists."""
    pass

# ACCEPTABLE - Under 120 characters
def extract_method_signatures_with_parameters(self, soup: BeautifulSoup) -> list[Method]:
    """Extract method signatures from definition lists with parameter parsing."""
    pass

# BAD - Too long
def extract_method_signatures_from_definition_lists_in_html_document_with_full_parameter_parsing(self, soup: BeautifulSoup) -> list[Method]:
    pass
```

### Imports

**Order:** Standard library → Third-party → Local imports

**Style:** One import per line, sorted alphabetically

```python
# GOOD
import argparse
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup
import chardet

from my_module import MyClass

# BAD
import argparse, json, logging
from bs4 import BeautifulSoup
import chardet
from my_module import MyClass
```

### Type Hints

**Requirement:** All function signatures must have type hints

**Rationale:** Improves IDE support and documentation

```python
# GOOD
def find_method(self, method_name: str, namespace: Optional[str] = None) -> list[SearchResult]:
    """Find method by exact name match (case-insensitive)."""
    pass

# BAD
def find_method(self, method_name, namespace=None):
    pass
```

### Docstrings

**Requirement:** All public functions and classes must have docstrings

**Style:** Google-style docstrings

```python
# GOOD
def find_method(self, method_name: str, namespace: Optional[str] = None) -> list[SearchResult]:
    """Find method by exact name match (case-insensitive).

    Args:
        method_name: Method name to search for
        namespace: Optional namespace filter

    Returns:
        List of matching SearchResult objects

    Example:
        >>> kb = ProcessNetKnowledge()
        >>> results = kb.find_method("CreateArc", namespace="Geometry")
        >>> len(results)
        2
    """
    pass

# BAD
def find_method(self, method_name, namespace=None):
    # Find a method
    pass
```

### Dataclass Usage

**Preference:** Use `@dataclass` for data structures

**Rationale:** Automatic `__init__`, `__repr__`, `__eq__` methods

```python
# GOOD
from dataclasses import dataclass

@dataclass
class SearchResult:
    """Represents a search result."""
    name: str
    type: str  # 'method', 'class', 'interface', 'example'
    namespace: str
    signature: str = ""
    description: str = ""
    score: float = 100.0

# BAD
class SearchResult:
    def __init__(self, name, type, namespace, signature="", description="", score=100.0):
        self.name = name
        self.type = type
        self.namespace = namespace
        self.signature = signature
        self.description = description
        self.score = score
```

### Constants

**Naming:** UPPER_SNAKE_CASE

**Location:** Module-level or class-level

```python
# GOOD
class ProcessNetDocParser:
    KNOWN_INTERFACES = [
        'IApplication', 'IModelDocument', 'IPlotDocument', 'ISubSystem',
        'IBody', 'IReferenceFrame', 'IMarker', 'IJoint', 'IForce',
    ]

    EXCLUDE_PATTERNS = [
        '_static', '_images', 'assets', 'css', 'js', '_sources',
        '.git', '__pycache__', 'mathjax'
    ]

# BAD
class ProcessNetDocParser:
    knownInterfaces = ['IApplication', ...]
    excludePatterns = ['_static', ...]
```

### Error Handling

**Strategy:** Log errors and continue processing (fail gracefully)

**Pattern:** Try-except with logging

```python
# GOOD
try:
    content = self.parse_html_file(file_path)
    # Process content
except Exception as e:
    logger.error(f"Failed to process {file_path}: {e}")
    self.errors.append({'file': str(file_path), 'error': str(e)})
    self.stats['files_failed'] += 1
    # Continue to next file

# BAD - Stops entire process
try:
    content = self.parse_html_file(file_path)
except Exception as e:
    raise  # Stops processing
```

### Logging

**Configuration:** Use standard logging module

**Format:** Timestamp, level, message

```python
# GOOD
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

# Usage
logger.info(f"Processing {file_path.name}")
logger.warning(f"No methods found in {file_path.name}")
logger.error(f"Failed to parse {file_path}: {e}")
```

### Progress Feedback

**Requirement:** Show progress for long operations

**Pattern:** Percentage with current/total

```python
# GOOD
for idx, file_path in enumerate(files, 1):
    progress = (idx / len(files)) * 100
    logger.info(f"[{progress:5.1f}%] ({idx}/{len(files)}) {file_path.name}")

# BAD - No progress indication
for file_path in files:
    logger.info(f"Processing {file_path.name}")
```

## Naming Conventions

### Variables and Functions

**Convention:** snake_case

**Descriptive:** Use full words, avoid abbreviations

```python
# GOOD
def find_method_by_name(method_name: str) -> list:
    pass

search_results = []
extraction_duration_seconds = 0

# BAD
def findMeth(mn: str) -> list:
    pass

res = []
dur = 0
```

### Classes

**Convention:** PascalCase

**Descriptive:** Noun or noun phrase

```python
# GOOD
class ProcessNetDocParser:
    pass

class SearchResult:
    pass

# BAD
class parser:
    pass

class result:
    pass
```

### Constants

**Convention:** UPPER_SNAKE_CASE

```python
# GOOD
MAX_FILE_SIZE = 10_000_000
DEFAULT_ENCODING = 'utf-8'

# BAD
maxFileSize = 10_000_000
defaultEncoding = 'utf-8'
```

### Private Members

**Convention:** Leading underscore

```python
# GOOD
class MyClass:
    def __init__(self):
        self._private_var = 0
        self.public_var = 1

    def _private_method(self):
        pass

    def public_method(self):
        pass
```

## Code Organization

### File Structure

**Maximum Size:** 200 lines per file (split if larger)

**Rationale:** Improves context management and readability

```python
# GOOD - Small, focused files
# recurdyn-doc-parser.py (475 lines)
#   - ProcessNetDocParser class
#   - Dataclass definitions
#   - Main execution

# processnet-query-interface.py (581 lines)
#   - ProcessNetKnowledge class
#   - SearchResult dataclass
#   - Interactive CLI
#   - Main execution

# BAD - Large monolithic file
# everything.py (2000+ lines)
```

### Class Organization

**Order:**
1. Docstring
2. Class variables (constants, configs)
3. `__init__` method
4. Public methods
5. Private methods (leading underscore)
6. Special methods (`__str__`, `__repr__`)

```python
# GOOD
class ProcessNetDocParser:
    """Parser for RecurDyn ProcessNet documentation."""

    KNOWN_INTERFACES = [...]
    EXCLUDE_PATTERNS = [...]

    def __init__(self, input_path: Path, output_path: Path):
        """Initialize parser with input and output paths."""
        pass

    def discover_files(self) -> list:
        """Discover all documentation files recursively."""
        pass

    def _detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding (private method)."""
        pass
```

## Documentation Standards

### README.md

**Sections Required:**
1. Project title and brief description
2. Quick start guide
3. Project structure
4. Key features
5. Usage examples
6. Installation instructions
7. Links to detailed documentation

### Code Comments

**When to Comment:**
- Complex algorithms or logic
- Non-obvious implementation details
- Workarounds or known issues
- API documentation (docstrings)

**When NOT to Comment:**
- Obvious code (self-documenting)
- Outdated information
- Redundant information

```python
# GOOD - Explains non-obvious regex
# Match method name at start of signature
# Example: "CreateArc(center, radius)" → "CreateArc"
match = re.match(r'(\w+)\s*\(', sig_text)

# BAD - Obvious comment
# Increment counter
count += 1

# GOOD - Explains workaround
# Workaround: BeautifulSoup doesn't handle nested dl elements correctly
# So we manually extract dt/dd pairs
for dt in dl.find_all('dt', recursive=False):
    pass
```

### Inline Documentation

**Requirement:** Docstrings for all public APIs

**Format:** Google-style

```python
def extract_method_signatures(self, soup: BeautifulSoup) -> list[Method]:
    """Extract method signatures from definition lists.

    Scans the HTML for definition list (<dl>) elements and extracts
    method signatures from definition term (<dt>) elements. Descriptions
    are extracted from the corresponding definition description (<dd>).

    Args:
        soup: BeautifulSoup object containing parsed HTML

    Returns:
        List of Method objects with name, signature, and description

    Example:
        >>> parser = ProcessNetDocParser()
        >>> soup = BeautifulSoup(html, 'lxml')
        >>> methods = parser.extract_method_signatures(soup)
        >>> len(methods)
        15
    """
```

## Error Handling Standards

### Exception Handling

**Strategy:** Catch specific exceptions when possible

```python
# GOOD - Specific exception
try:
    with open(file_path, 'r', encoding=encoding) as f:
        content = f.read()
except FileNotFoundError:
    logger.error(f"File not found: {file_path}")
    return None
except UnicodeDecodeError:
    logger.warning(f"Encoding error: {file_path}, trying fallback")
    # Try fallback encoding

# BAD - Catch-all exception
try:
    with open(file_path, 'r') as f:
        content = f.read()
except Exception:
    pass
```

### Error Messages

**Format:** Specific, actionable, includes context

```python
# GOOD
logger.error(f"Failed to read {file_path}: {e}")
logger.error(f"File {file_path} has invalid encoding: {encoding}")

# BAD
logger.error("Error reading file")
logger.error("Something went wrong")
```

### Validation

**Input Validation:** Validate before processing

```python
# GOOD
def __init__(self, input_path: Path, output_path: Path):
    if not input_path.exists():
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    if input_path.suffix.lower() not in ['.html', '.htm']:
        raise ValueError(f"Input must be HTML file: {input_path}")
    # Continue processing

# BAD - No validation
def __init__(self, input_path: Path, output_path: Path):
    # Assumes input is valid
    pass
```

## Testing Standards

### Test Framework

**Framework:** pytest 7.0+

**Configuration:** `pytest.ini` in project root
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: unit tests
    integration: integration tests
    browser: browser-based tests (MCP Playwright)
    slow: slow tests
    phase_1: test infrastructure phase
    phase_2: browser verification phase
    phase_3: sample extraction phase
    phase_4: regression tests phase
    phase_5: spot-check validation phase
```

### Unit Tests

**Coverage:** Aim for >80% code coverage

**Naming:** `test_` prefix for test functions

**Markers:** Use pytest markers for test organization

```python
# GOOD - Unit test with fixtures
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

@pytest.mark.unit
def test_extract_method_signatures(parser_fixture):
    """Test method signature extraction from definition lists."""
    html = '<dl><dt>CreateArc(x, y)</dt><dd>Creates arc</dd></dl>'
    soup = BeautifulSoup(html, 'lxml')
    methods = parser_fixture.extract_method_signatures(soup)
    assert len(methods) == 1
    assert methods[0].name == "CreateArc"
    assert methods[0].signature == "CreateArc(x, y)"

@pytest.mark.unit
def test_fuzzy_search_with_typo(kb_fixture):
    """Test fuzzy search handles typos."""
    results = kb_fixture.search_method_fuzzy("CreateArk")  # Typo
    assert len(results) > 0
    assert results[0].name == "CreateArc"
    assert results[0].score >= 80  # 80%+ similarity threshold
```

### Pytest Fixtures

**Location:** `tests/conftest.py`

**Pattern:** Reusable fixtures for common test setup

```python
# conftest.py - Shared test fixtures
import pytest
from pathlib import Path
from src.recurdyn_doc_parser import ProcessNetDocParser
from src.processnet_query_interface import ProcessNetKnowledge

@pytest.fixture
def test_data_dir():
    """Provide test data directory."""
    return Path(__file__).parent / "test_data"

@pytest.fixture
def sample_html(test_data_dir):
    """Provide sample HTML for testing."""
    return test_data_dir / "sample.html"

@pytest.fixture
def parser_fixture(test_data_dir):
    """Provide initialized parser for tests."""
    parser = ProcessNetDocParser(
        input_path=test_data_dir / "html",
        output_path=test_data_dir / "output"
    )
    return parser

@pytest.fixture
def kb_fixture(test_data_dir):
    """Provide loaded knowledge base for tests."""
    kb = ProcessNetKnowledge(
        kb_path=test_data_dir / "output" / "processnet_knowledge.json"
    )
    return kb

@pytest.fixture(scope="session")
def browser_fixture():
    """Provide MCP Playwright browser for integration tests."""
    # Initialize browser for Phase 2 browser verification tests
    from mcp_playwright import Browser
    browser = Browser()
    yield browser
    browser.close()
```

### Test Markers and Phases

**Phase 1: Test Infrastructure**
```python
@pytest.mark.phase_1
@pytest.mark.unit
def test_fixture_setup(parser_fixture):
    """Test fixtures initialize correctly."""
    assert parser_fixture is not None
```

**Phase 2: MCP Playwright Browser Verification**
```python
@pytest.mark.phase_2
@pytest.mark.browser
async def test_visual_method_count(browser_fixture):
    """Test browser can count methods visually on HTML page."""
    # Use MCP Playwright for browser automation
    page = await browser_fixture.new_page()
    await page.goto("file:///path/to/html")
    method_count = await page.locator("dl dt").count()
    assert method_count > 0
```

**Phase 3: Sample Extraction Validation**
```python
@pytest.mark.phase_3
@pytest.mark.integration
def test_extract_5_file_types(parser_fixture):
    """Test extraction works for 5 file type samples."""
    file_types = [
        "geometry.html",
        "model.html",
        "body.html",
        "joint.html",
        "force.html"
    ]
    for file_type in file_types:
        methods = parser_fixture.extract_from_file(file_type)
        assert len(methods) > 0
```

**Phase 4: Regression Tests**
```python
@pytest.mark.phase_4
@pytest.mark.integration
def test_table_extraction_regression(parser_fixture):
    """Test parser handles table-based method extraction."""
    html = '''
    <table class="methods">
        <tr><th>Method</th><th>Description</th></tr>
        <tr><td>GetAllBodies()</td><td>Get all bodies</td></tr>
    </table>
    '''
    soup = BeautifulSoup(html, 'lxml')
    methods = parser_fixture.extract_from_tables(soup)
    assert len(methods) == 1
    assert methods[0].name == "GetAllBodies"
```

**Phase 5: Spot-Check Validation**
```python
@pytest.mark.phase_5
@pytest.mark.browser
async def test_spot_check_accuracy_98_percent(browser_fixture, kb_fixture):
    """Test 98% accuracy on random spot-checks."""
    # Random sample of 10 methods from knowledge base
    # Verify each via browser visual inspection
    sample_count = 10
    verified_count = 0

    for method in kb_fixture.get_random_methods(sample_count):
        # Use browser to verify method exists in original HTML
        is_valid = await browser_fixture.verify_method_exists(method)
        if is_valid:
            verified_count += 1

    accuracy = verified_count / sample_count * 100
    assert accuracy >= 98, f"Accuracy {accuracy}% below 98% threshold"
```

### Parametrized Testing

**Pattern:** Use pytest parametrize for multiple scenarios

```python
import pytest

@pytest.mark.unit
@pytest.mark.parametrize("encoding,content", [
    ("utf-8", "UTF-8 content ñ é"),
    ("windows-1252", "Windows content"),
    ("latin-1", "Latin content"),
])
def test_encoding_detection(encoding, content):
    """Test encoding detection works for multiple formats."""
    detected = detect_encoding_from_content(content.encode(encoding))
    assert detected.lower() in [encoding.lower(), 'utf-8']  # UTF-8 acceptable fallback
```

### HTML Fixture Management

**Pattern:** Sample HTML files for testing

```
tests/
├── conftest.py
├── test_data/
│   ├── fixtures/
│   │   ├── definition_list.html
│   │   ├── table_based.html
│   │   ├── heading_based.html
│   │   └── code_example.html
│   └── sample_files/
│       ├── geometry.html
│       ├── model.html
│       └── body.html
├── test_parser.py
├── test_query_interface.py
└── test_integration.py
```

### Integration Tests

**Scope:** Test full workflows with real data

**Success Metrics:**
- Execution time <2 minutes
- Browser verification <5 seconds per file
- Coverage >80%
- Accuracy 90%+

```python
@pytest.mark.integration
def test_full_extraction_workflow(parser_fixture, test_data_dir):
    """Test complete extraction from HTML to JSON."""
    output_json = test_data_dir / "output" / "processnet_knowledge.json"

    # Run extraction
    parser_fixture.build_knowledge_base()
    parser_fixture.save_knowledge_base()

    # Verify output
    assert output_json.exists()
    kb = json.loads(output_json.read_text())
    assert 'namespaces' in kb
    assert len(kb['namespaces']) > 0
    assert 'method_index' in kb
    assert len(kb['method_index']) > 0

@pytest.mark.integration
def test_query_workflow_accuracy(kb_fixture):
    """Test query interface returns accurate results."""
    # Test exact lookup
    results = kb_fixture.find_method("CreateArc")
    assert len(results) > 0
    assert results[0].name == "CreateArc"

    # Test fuzzy search
    fuzzy_results = kb_fixture.search_method_fuzzy("CreateArk")
    assert len(fuzzy_results) > 0
    assert fuzzy_results[0].name == "CreateArc"

    # Test description search
    desc_results = kb_fixture.search_by_description("arc geometry")
    assert len(desc_results) > 0
```

### Test Organization

**Structure:** Mirror source structure

```
tests/
├── conftest.py                           # Shared fixtures
├── test_parser.py                        # Unit tests for parser
├── test_query_interface.py               # Unit tests for query interface
├── test_integration.py                   # Full workflow tests
├── test_mcp_playwright_verification.py   # Phase 2 browser tests
├── test_data/
│   ├── fixtures/
│   │   ├── definition_list.html
│   │   ├── table_based.html
│   │   ├── heading_based.html
│   │   ├── multi_encoding.html
│   │   └── code_example.html
│   └── sample_files/
│       ├── geometry.html
│       ├── model.html
│       ├── body.html
│       ├── joint.html
│       └── force.html
└── test_samples/                         # Phase 3-5 sample files
    └── extracted_methods.json            # Baseline for regression tests
```

### Test Execution

**Local Testing:**
```bash
# Run all tests
pytest

# Run specific phase
pytest -m phase_2

# Run with coverage
pytest --cov=src --cov-report=html

# Run slow tests
pytest -m slow -v
```

**CI/CD Pipeline:**
- All phases must pass before merge
- Coverage >80% required
- Browser tests require MCP Playwright availability

### Success Criteria

**Phase 1 (Test Infrastructure):**
- Fixtures initialize correctly
- Markers work as expected
- >80% code coverage achieved

**Phase 2 (Browser Verification):**
- MCP Playwright tests execute successfully
- Visual verification matches extraction
- Browser test execution <5 seconds per file

**Phase 3 (Sample Extraction):**
- All 5 file types extract without errors
- Method count accuracy >90%
- Code examples found in samples

**Phase 4 (Regression Tests):**
- Table extraction works correctly
- Highlight/formatting preserved
- Parser adjustments don't break existing tests

**Phase 5 (Spot-Check Validation):**
- 98% accuracy on random sampling
- 90%+ method signature accuracy
- All 3 use cases have coverage

## Performance Standards

### Profiling

**Requirement:** Profile before optimizing

```python
# GOOD - Measure before optimizing
import time

start = time.time()
result = slow_operation()
duration = time.time() - start
logger.info(f"Operation took {duration:.2f} seconds")

if duration > 1.0:
    logger.warning("Operation took >1 second, consider optimization")

# BAD - Optimize without measuring
result = optimized_operation()  # Is it actually faster?
```

### Memory Management

**Strategy:** Process files sequentially, not all at once

```python
# GOOD - Sequential processing
for file_path in files:
    content = parse_file(file_path)
    process(content)
    del content  # Free memory

# BAD - Load all files at once
all_content = [parse_file(f) for f in files]  # High memory usage
```

### Caching

**Use Case:** Expensive operations with repeated calls

```python
# GOOD - Cache encoding detection
@functools.lru_cache(maxsize=128)
def detect_encoding(self, file_path: Path) -> str:
    """Detect file encoding with caching."""
    pass
```

## Git Standards

### Commit Messages

**Format:** Conventional Commits

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

**Examples:**
```
feat(parser): add table-based method extraction

Implement extraction of method signatures from HTML tables.
Handles both standard and variant table formats used in
RecurDyn documentation.

Fixes #42

docs(readme): update installation instructions

Clarify system package requirements for Ubuntu/Debian.
Add troubleshooting section for CHM extraction errors.

fix(query): handle missing rapidfuzz gracefully

Add fallback to substring search when rapidfuzz is not
installed. Warning message now shown to user.
```

### Branch Naming

**Format:** `<type>/<short-description>`

```
feature/add-fuzzy-search
fix/encoding-detection
docs/update-readme
refactor/parser-class
```

## Code Review Standards

### Review Checklist

**Functionality:**
- [ ] Code works as intended
- [ ] Edge cases handled
- [ ] Error handling appropriate

**Quality:**
- [ ] Follows coding standards
- [ ] Type hints present
- [ ] Docstrings present
- [ ] No obvious bugs

**Performance:**
- [ ] No performance regressions
- [ ] Memory usage acceptable
- [ ] No unnecessary optimizations

**Testing:**
- [ ] Tests added/updated
- [ ] Tests pass
- [ ] Coverage acceptable

### Review Process

1. **Self-Review:** Review your own code before submitting
2. **Automated Checks:** Ensure linting and tests pass
3. **Peer Review:** Get review from team member
4. **Address Feedback:** Make requested changes
5. **Approval:** Merge after approval

## Documentation Standards

### Code Documentation

**Requirements:**
- All public APIs have docstrings
- Complex algorithms explained
- Non-obvious code commented
- Examples provided for key functions

### Project Documentation

**Required Files:**
- README.md - Project overview
- docs/project-overview-pdr.md - Product requirements
- docs/code-standards.md - This file
- docs/codebase-summary.md - Code structure
- docs/system-architecture/index.md - Architecture details
- docs/project-roadmap.md - Development timeline

### API Documentation

**Format:** Markdown with code examples

```markdown
## find_method()

Find method by exact name match (case-insensitive).

**Parameters:**
- `method_name` (str): Method name to search for
- `namespace` (Optional[str]): Namespace filter

**Returns:**
- `list[SearchResult]`: Matching methods

**Example:**
```python
kb = ProcessNetKnowledge()
results = kb.find_method("CreateArc", namespace="Geometry")
for r in results:
    print(f"{r.namespace}.{r.name}: {r.signature}")
```
```

## Security Standards

### Input Validation

**Requirement:** Validate all external inputs

```python
# GOOD
def parse_html_file(self, file_path: Path) -> dict:
    """Parse HTML file with validation."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    if file_path.stat().st_size > 10_000_000:  # 10MB limit
        raise ValueError(f"File too large: {file_path}")
    # Process file

# BAD - No validation
def parse_html_file(self, file_path: Path) -> dict:
    # Assumes file is valid and safe
    pass
```

### Path Handling

**Security:** Use `pathlib.Path` for path operations

```python
# GOOD - Safe path handling
from pathlib import Path

input_path = Path(input_path).resolve()
if not input_path.is_relative_to(base_path):
    raise ValueError("Path outside base directory")

# BAD - String manipulation (unsafe)
input_path = os.path.abspath(input_path)
if not input_path.startswith(base_path):  # Can be bypassed
    raise ValueError("Invalid path")
```

### Dependency Management

**Requirements:**
- Pin dependency versions in requirements.txt
- Regular security audits
- No unnecessary dependencies

```
# GOOD - Pinned versions
beautifulsoup4==4.12.0
lxml==5.0.0
rapidfuzz==3.0.0
chardet==5.0.0

# BAD - Unpinned versions
beautifulsoup4
lxml
rapidfuzz
```

## Compliance and Enforcement

### Automated Checks

**Pre-commit Hooks:**
- Linting (flake8, pylint)
- Type checking (mypy)
- Formatting (black, isort)

**CI/CD:**
- All tests pass
- Code coverage threshold
- Security vulnerability scan

### Manual Review

**Process:**
- Code review before merge
- Documentation review
- Architecture review for significant changes

## Related Documents

- [README.md](../README.md) - Project overview
- [docs/project-overview-pdr.md](project-overview-pdr.md) - Product requirements
- [docs/codebase-summary.md](codebase-summary.md) - Code structure
- [docs/system-architecture/index.md](system-architecture/index.md) - Architecture details

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial code standards document |

---

**Status:** Active
**Next Review:** Quarterly or when standards need updating
**Maintainer:** Development Team
