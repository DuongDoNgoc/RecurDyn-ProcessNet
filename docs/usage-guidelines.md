# RecurDyn ProcessNet - Usage Guidelines

**Version:** 3.0 (v7 Knowledge Base)
**Last Updated:** 2026-02-21
**Project Status:** Production Ready (Python/C#/VB/User Guides)
**Scope:** Python API, C#/VB API, and User Guides extraction complete.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [REST API Server](#rest-api-server)
4. [Querying the Knowledge Base](#querying-the-knowledge-base)
5. [Running Tests](#running-tests)
6. [Extending the Parser](#extending-the-parser)
7. [Common Use Cases](#common-use-cases)
8. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Basic Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the REST API server
python src/processnet-api-server.py --port 8000

# 3. Access API documentation
# Open browser: http://localhost:8000/docs
```

### CLI Query Interface

```bash
# Interactive mode
python src/processnet-query-interface.py

# Direct queries
python src/processnet-query-interface.py --search "CreateArc"
python src/processnet-query-interface.py --find "SaveModel"
python src/processnet-query-interface.py --examples "geometry"
```

---

## Installation

### Prerequisites

**System Requirements:**
- Python 3.10 or higher
- 500 MB free disk space
- 2 GB RAM minimum

**System Dependencies (Ubuntu/Debian/WSL):**
```bash
sudo apt update
sudo apt install -y libchm-bin p7zip-full
```

**Python Dependencies:**
```bash
pip install -r requirements.txt
```

**Dependencies included:**
- `beautifulsoup4>=4.12.0` - HTML parsing
- `lxml>=5.0.0` - Fast parser backend
- `rapidfuzz>=3.0.0` - Fuzzy search
- `chardet>=5.0.0` - Encoding detection
- `fastapi>=0.104.0` - REST API framework
- `uvicorn[standard]>=0.24.0` - ASGI server
- `pydantic-settings>=2.0.0` - Settings management
- `httpx>=0.25.0` - HTTP client testing
- `pytest-cov>=4.1.0` - Test coverage

---

## REST API Server

### Starting the Server

```bash
# Default configuration (port 8000)
python src/processnet-api-server.py

# Custom port
python src/processnet-api-server.py --port 8080

# Custom knowledge base path
python src/processnet-api-server.py --kb /path/to/knowledge.json --port 9000
```

### API Endpoints

#### 1. Health Check

```bash
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "knowledge_base_loaded": true,
  "timestamp": "2026-02-01T12:00:00Z"
}
```

#### 2. Knowledge Base Statistics

```bash
GET /api/stats
```

**Response:**
```json
{
  "total_items": 26106,
  "python_api": {
    "classes": 1808,
    "methods": 4367,
    "namespaces": 23
  },
  "csharp_vb_api": {
    "members": 21274
  },
  "user_guides": {
    "documents": 7,
    "sections": 16
  }
}
```

#### 3. List Namespaces

```bash
GET /api/namespaces
```

**Response:**
```json
{
  "namespaces": [
    "ProcessNet",
    "ProcessNet.AutoDesign",
    "ProcessNet.Geometry",
    "ProcessNet.Model",
    "..."
  ]
}
```

#### 4. Get Namespace Details

```bash
GET /api/namespaces/{namespace_name}
```

**Example:**
```bash
curl "http://localhost:8000/api/namespaces/ProcessNet.Model"
```

**Response:**
```json
{
  "name": "ProcessNet.Model",
  "full_name": "FunctionBay.RecurDyn.ProcessNet.Model",
  "description": "RecurDyn Model API for automation",
  "classes": 45,
  "methods": 234
}
```

#### 5. Fuzzy Search

```bash
GET /api/search?q={query}&limit={limit}
```

**Example:**
```bash
# Search for save-related methods
curl "http://localhost:8000/api/search?q=save&limit=10"

# Search with Python
import requests
response = requests.get("http://localhost:8000/api/search", params={"q": "geometry", "limit": 5})
results = response.json()["results"]
```

**Response:**
```json
{
  "query": "save",
  "results": [
    {
      "name": "SaveModel",
      "type": "method",
      "namespace": "ProcessNet.Model",
      "signature": "SaveModel(filePath: str) -> bool",
      "description": "Save the current model to specified file path",
      "score": 95.0
    }
  ],
  "total": 10
}
```

#### 6. Exact Method Lookup

```bash
GET /api/find/{method_name}
```

**Example:**
```bash
curl "http://localhost:8000/api/find/SaveNewModel"
```

**Response:**
```json
{
  "count": 1,
  "results": [
    {
      "name": "SaveNewModel",
      "signature": "SaveNewModel(filePath: str) -> bool",
      "namespace": "ProcessNet.Model",
      "description": "...",
      "parameters": [...],
      "return_type": "bool"
    }
  ]
}
```

#### 7. Find Code Examples

```bash
GET /api/examples?keyword={keyword}
```

**Example:**
```bash
curl "http://localhost:8000/api/examples?keyword=geometry"
```

**Response:**
```json
{
  "keyword": "geometry",
  "examples": [
    {
      "title": "Creating Geometric Entities",
      "code": "// Example code...",
      "language": "csharp",
      "source_file": "geometry_examples.html"
    }
  ]
}
```

### Interactive API Documentation

**Swagger UI:**
```
http://localhost:8000/docs
```

**ReDoc:**
```
http://localhost:8000/redoc
```

Both provide interactive API exploration with request/response examples.

### Python Client Example

```python
import requests

class ProcessNetClient:
    """Python client for ProcessNet Knowledge Base API"""

    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_base = f"{base_url}/api"

    def search(self, query, limit=10):
        """Fuzzy search for methods"""
        response = requests.get(
            f"{self.api_base}/search",
            params={"q": query, "limit": limit}
        )
        return response.json()["results"]

    def find_method(self, method_name):
        """Exact method lookup"""
        response = requests.get(f"{self.api_base}/find/{method_name}")
        data = response.json()
        if data["count"] > 0:
            return data["results"][0]
        return None

    def get_namespace(self, namespace):
        """Get namespace details"""
        response = requests.get(f"{self.api_base}/namespaces/{namespace}")
        return response.json()

    def find_examples(self, keyword):
        """Find code examples"""
        response = requests.get(
            f"{self.api_base}/examples",
            params={"keyword": keyword}
        )
        return response.json()["examples"]

# Usage
client = ProcessNetClient()

# Search for geometry methods
methods = client.search("geometry")
for method in methods:
    print(f"{method['name']}: {method['signature']}")

# Find specific method
save_method = client.find_method("SaveModel")
if save_method:
    print(f"Parameters: {save_method['parameters']}")

# Get namespace info
model_ns = client.get_namespace("ProcessNet.Model")
print(f"Classes: {model_ns['classes']}, Methods: {model_ns['methods']}")
```

---

## Querying the Knowledge Base

### CLI Interface

#### Interactive Mode

```bash
python src/processnet-query-interface.py
```

**Available Commands:**

| Command | Description | Example |
|---------|-------------|---------|
| `search <query>` | Fuzzy search methods | `search create` |
| `find <method>` | Exact method lookup | `find SaveModel` |
| `desc <keywords>` | Search descriptions | `desc design of experiments` |
| `list <namespace>` | List namespace contents | `list ProcessNet.Geometry` |
| `namespaces` | List all namespaces | `namespaces` |
| `examples [keyword]` | Find code examples | `examples geometry` |
| `stats` | Show statistics | `stats` |
| `help` | Show help | `help` |
| `quit` | Exit | `quit` |

#### Command-Line Usage

```bash
# Search for methods
python src/processnet-query-interface.py --search "CreateArc"

# Find exact method
python src/processnet-query-interface.py --find "GetAllBodies"

# Search by description
python src/processnet-query-interface.py --desc "design of experiments"

# List namespace
python src/processnet-query-interface.py --list "ProcessNet.Model"

# Find examples
python src/processnet-query-interface.py --examples "geometry"

# Get statistics
python src/processnet-query-interface.py --stats

# JSON output for scripting
python src/processnet-query-interface.py --search "save" --json
```

### Python API

```python
from processnet_query_interface import ProcessNetKnowledge

# Load knowledge base
kb = ProcessNetKnowledge("output/processnet-knowledge-v7.json")

# Exact method lookup
methods = kb.find_method("CreateArc")
for method in methods:
    print(f"{method.signature}")
    print(f"{method.description}")

# Fuzzy search
results = kb.search_method_fuzzy("geometry", threshold=70.0, limit=10)
for result in results:
    print(f"{result.name} ({result.score}%)")

# Search by description
doe_methods = kb.search_by_description("design of experiments")

# List namespace contents
geometry = kb.list_namespace_contents("ProcessNet.Geometry")
print(f"Classes: {len(geometry['classes'])}")
print(f"Methods: {len(geometry['standalone_methods'])}")

# Find code examples
examples = kb.find_examples("geometry")
for example in examples:
    print(f"Title: {example['title']}")
    print(f"Code:\n{example['code']}")

# Get statistics
stats = kb.get_statistics()
print(f"Namespaces: {stats['namespaces']}")
print(f"Classes: {stats['classes']}")
print(f"Methods: {stats['methods']}")
```

---

## Running Tests

### Test Suite Overview

The project includes 200+ tests across multiple suites:

| Test Suite | Tests | Purpose |
|------------|-------|---------|
| Parser Enhancements | 8 | Sphinx parsing validation |
| Sample Extraction | 20 | HTML fixture extraction |
| Parser Regression | 19 | Regression testing |
| Use Case Coverage | 18 | Automation workflows |
| Browser Verification | 11 | Visual validation |
| Spot-Check Validation | 16 | Quality metrics |
| Full Extraction | 16 | End-to-end extraction |
| Validation | 12 | Quality assurance |
| API Server Tests | 23 | REST API validation |
| Integration Tests | 51 | Method/param validation |

### Running All Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test-sample-extraction-validation.py

# Run tests by marker
pytest -m "not browser"  # Skip browser tests
pytest -m integration     # Only integration tests
```

### Running Specific Test Categories

```bash
# Parser tests
pytest tests/test-parser-adjustment-regression.py

# Sample extraction tests
pytest tests/test-sample-extraction-validation.py

# Use case tests
pytest tests/test-use-case-coverage-validation.py

# API server tests
pytest tests/test-api-server.py

# Integration tests
pytest tests/integration/test-integration-validation.py
```

### Test Results Interpretation

**Expected Results:**
- Overall pass rate: 95%+ (200+ tests)
- Browser tests: 1 skipped (MCP server config required)
- Parameter type tests: 69% pass (11/16, some types ambiguous)
- All other tests: 100% pass

---

## Extending the Parser

### Parser Architecture

The parser uses a multi-strategy approach:

1. **Sphinx-Specific Parsing** (Phase 04 enhancement)
   - Method signatures from `dl.py.method`
   - Parameters from `dl.py.method > dd > field-list`
   - Return types from `field-list.bodies`
   - Properties from `dl.py.property`
   - Classes from `dl.py.class`

2. **Fallback Strategies**
   - Definition list parsing
   - Table-based extraction
   - Heading + paragraph parsing

3. **Code Example Extraction**
   - `.highlight-default` blocks
   - `<pre><code>` tags
   - Language detection from CSS classes

### Adding New Parsing Strategies

**Example: Adding Table-Based Method Extraction**

```python
# In recurdyn-doc-parser.py

def extract_table_methods(self, soup: BeautifulSoup, source_file: str) -> list:
    """Extract methods from HTML tables"""
    methods = []

    # Find all tables
    for table in soup.find_all('table'):
        rows = table.find_all('tr')

        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Assume first column is method name, second is description
                method_name = cells[0].get_text(strip=True)
                description = cells[1].get_text(strip=True)

                # Check if it looks like a method
                if '(' in method_name and ')' in method_name:
                    methods.append(Method(
                        name=method_name.split('(')[0].strip(),
                        signature=method_name,
                        description=description,
                        source_file=source_file
                    ))

    return methods

# Integrate into main parse flow
def parse_html_file(self, file_path: Path) -> dict:
    # ... existing code ...

    # Try new table-based extraction
    methods.extend(self.extract_table_methods(soup, source_file))

    # ... rest of parsing ...
```

### Handling New Documentation Formats

**Example: Adding Markdown Support**

```python
from markdown import Markdown

def parse_markdown_file(self, file_path: Path) -> dict:
    """Parse ProcessNet documentation in Markdown format"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert Markdown to HTML for existing parsers
    md = Markdown()
    html_content = md.convert(content)

    # Reuse existing HTML parsing logic
    soup = BeautifulSoup(html_content, 'lxml')
    return self._parse_soup(soup, file_path)
```

### Adding Custom Data Extractors

**Example: Extracting Exception Information**

```python
@dataclass
class Method:
    # ... existing fields ...
    exceptions: list = field(default_factory=list)

def extract_exceptions(self, soup: BeautifulSoup) -> list:
    """Extract exception information from documentation"""
    exceptions = []

    # Look for exception sections
    for section in soup.find_all(['div', 'section'], class_='exceptions'):
        for item in section.find_all(['li', 'p']):
            text = item.get_text(strip=True)
            if 'throws' in text.lower() or 'exception' in text.lower():
                exceptions.append(text)

    return exceptions

# Integrate into method extraction
def parse_sphinx_parameters(self, dl, dd, method: Method):
    # ... existing parameter parsing ...

    # Extract exceptions if present
    method.exceptions = self.extract_exceptions(dd)
```

### Testing Custom Extensions

```python
# tests/test-custom-extension.py

import pytest
from recurdyn_doc_parser import ProcessNetDocParser

def test_table_method_extraction():
    """Test new table-based method extraction"""
    parser = ProcessNetDocParser("tests/fixtures")

    # Create test HTML with table
    html = """
    <table>
        <tr><td>MethodA(param1, param2)</td><td>Description A</td></tr>
        <tr><td>MethodB()</td><td>Description B</td></tr>
    </table>
    """

    soup = BeautifulSoup(html, 'lxml')
    methods = parser.extract_table_methods(soup, "test.html")

    assert len(methods) == 2
    assert methods[0].name == "MethodA"
    assert methods[1].name == "MethodB"
```

---

## Common Use Cases

### Use Case 1: DOE Batch Execution

**Scenario:** Automate Design of Experiments with parameter variation.

```python
from processnet_query_interface import ProcessNetKnowledge

# Load knowledge base
kb = ProcessNetKnowledge("output/processnet-knowledge-v7.json")

# Find model loading methods
load_methods = kb.search_method_fuzzy("load", limit=5)
for method in load_methods:
    print(f"{method.name}: {method.signature}")

# Find parameter setting methods
param_methods = kb.search_by_description("parameter")
for method in param_methods[:10]:
    print(f"{method.name}: {method.description}")

# Find save methods
save_methods = kb.search_method_fuzzy("save", limit=5)

# Example automation script structure
print("""
# DOE Automation Example:
model = ProcessNet.Model.Load("base_model.rdyn")

for mass in [100, 150, 200]:
    for stiffness in [1000, 2000, 3000]:
        variant = model.Clone()
        variant.SetParameter("body_mass", mass)
        variant.SetParameter("spring_k", stiffness)
        variant.SaveAs(f"doe_m{mass}_k{stiffness}.rdyn")
        variant.Run()
""")
```

### Use Case 2: Model Introspection

**Scenario:** Explore and analyze model structure.

```python
# Find entity enumeration methods
entity_methods = kb.search_by_description("get all")
for method in entity_methods:
    if any(entity in method.description.lower()
           for entity in ['body', 'joint', 'force']):
        print(f"{method.name}: {method.description}")

# Get Model namespace details
model_ns = kb.list_namespace_contents("ProcessNet.Model")
print(f"\nProcessNet.Model namespace:")
print(f"  Classes: {len(model_ns['classes'])}")
print(f"  Methods: {len(model_ns['standalone_methods'])}")

# Example introspection script
print("""
# Model Introspection Example:
model = ProcessNet.Model.Load("model.rdyn")

entity_map = {
    "bodies": [b.GetID() for b in model.GetAllBodies()],
    "joints": [j.GetID() for j in model.GetAllJoints()],
    "forces": [f.GetID() for f in model.GetAllForces()]
}
""")
```

### Use Case 3: Result Post-Processing

**Scenario:** Extract and process simulation results.

```python
# Find result loading methods
result_methods = kb.search_method_fuzzy("result", limit=10)
for method in result_methods:
    print(f"{method.name}: {method.signature}")

# Find data extraction methods
data_methods = kb.search_by_description("get data")
for method in data_methods[:5]:
    print(f"{method.name}: {method.description}")

# Example result processing script
print("""
# Result Processing Example:
result = ProcessNet.Result.Load("sim_output.rsl")

time = result.GetTimeArray()
force = result.GetEntityData("Force_1", "Magnitude")
disp = result.GetEntityData("Body_2", "Displacement_X")

# Export to CSV
import pandas as pd
df = pd.DataFrame({
    'Time': time,
    'Force': force,
    'Displacement': disp
})
df.to_csv("results.csv", index=False)
""")
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: CHM Extraction Fails

**Symptom:** Error extracting ProcessNetHelp.chm

**Solutions:**
```bash
# Try 7-Zip via WSL
/mnt/c/Program\ Files/7-Zip/7z.exe x ProcessNetHelp.chm -ooutput/extracted_chm/ -y

# Try libchm-bin
sudo apt install libchm-bin
extract_chm ProcessNetHelp.chm output/extracted_chm/

# Check file integrity
ls -lh ProcessNetHelp.chm  # Should be ~32 MB
```

#### Issue 2: Encoding Errors During Parsing

**Symptom:** `UnicodeDecodeError` during extraction

**Solutions:**
- Parser handles encoding auto-detection with fallback
- If errors persist, check file encoding:
```bash
file -i output/extracted_chm/some_file.html
```
- Manually convert problematic files:
```bash
iconv -f WINDOWS-1252 -t UTF-8 input.html -o output.html
```

#### Issue 3: API Server Won't Start

**Symptom:** Server fails to start or port in use

**Solutions:**
```bash
# Check port availability
netstat -tuln | grep 8000

# Use different port
python src/processnet-api-server.py --port 8080

# Check knowledge base file
ls -lh output/processnet-knowledge-v7.json

# Verify dependencies
pip install --upgrade fastapi uvicorn
```

#### Issue 4: Query Returns No Results

**Symptom:** Searches return empty results

**Solutions:**
```bash
# Check knowledge base loaded
curl http://localhost:8000/api/stats

# Verify extraction completed
python src/processnet-query-interface.py --stats

# Try lowercase search
python src/processnet-query-interface.py --search "save"

# Try fuzzy search with lower threshold
kb.search_method_fuzzy("savemodel", threshold=50.0)
```

#### Issue 5: Test Failures

**Symptom:** Tests failing after modifications

**Solutions:**
```bash
# Run specific test to debug
pytest tests/test-sample-extraction-validation.py::test_extract_methods_from_html -v

# Check test fixtures
ls -la tests/fixtures/html-samples/

# Update baseline if extraction improved
python tests/update_baseline.py

# Run with detailed output
pytest -vv --tb=long
```

#### Issue 6: Memory Issues During Extraction

**Symptom:** Out of memory errors on large documentation sets

**Solutions:**
```python
# Process in batches
parser = ProcessNetDocParser(input_path, output_path)

# Limit file count
parser.build_knowledge_base(file_limit=1000)

# Increase system swap
sudo swapon /swapfile

# Use streaming for large files (future enhancement)
```

### Performance Optimization

**Slow Extraction:**
```bash
# Limit processed files
python src/recurdyn-doc-parser.py \
    --input output/extracted_chm \
    --output output/kb.json \
    --file-limit 1000

# Use faster parser backend
export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages
```

**Slow Queries:**
```python
# Use exact lookup instead of fuzzy search
kb.find_method("ExactMethodName")  # O(1)

# Pre-filter by namespace
kb.list_namespace_contents("ProcessNet.Model")

# Increase threshold for fuzzy search
kb.search_method_fuzzy("query", threshold=80.0)  # Fewer matches, faster
```

### Getting Help

**Check Documentation:**
- README.md - Project overview
- docs/codebase-summary.md - Architecture details
- docs/system-architecture/index.md - System design

**View Test Examples:**
```bash
# All test files contain usage examples
ls tests/
cat tests/test-use-case-coverage-validation.py
```

**API Documentation:**
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

---

## Best Practices

1. **Always start the API server** before running queries in production
2. **Use exact method lookup** (`find_method`) when you know the method name
3. **Use fuzzy search** (`search_method_fuzzy`) for discovery and exploration
4. **Filter by namespace** to narrow down search results
5. **Check statistics first** to understand knowledge base coverage
6. **Run tests regularly** to validate extraction quality
7. **Keep knowledge base updated** when RecurDyn version changes

---

## Next Steps

1. Explore the REST API at http://localhost:8000/docs
2. Read the project completion report for detailed statistics
3. Review test files for usage examples
4. Check system architecture documentation for design details

---

**Document Version:** 1.0
**Last Updated:** 2026-02-01
**Maintainer:** Development Team
