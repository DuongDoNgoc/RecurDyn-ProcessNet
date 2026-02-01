---
title: "Phase 04 - Documentation Updates and API Usage Guide"
description: "Update README.md with API server usage, document all endpoints with examples, add curl and Python request examples"
status: pending
priority: P1
effort: 1h
tags: [documentation, readme, examples, api-guide]
---

# Phase 04 - Documentation Updates and API Usage Guide

## Context Links

- [Plan Overview](./plan.md)
- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Phase 02: Endpoint Implementation](./phase-02-rest-api-endpoints-implementation.md)
- [Phase 03: Test Suite](./phase-03-test-suite-for-three-automation-use-cases.md)
- [Project README](../../../README.md)
- [Code Standards](../../../docs/code-standards.md)

## Overview

**Priority:** P1 (High)
**Current Status:** Pending
**Estimated Effort:** 1 hour

Update project documentation with comprehensive REST API server usage guide. Document all endpoints with curl and Python examples for the 3 target use cases.

## Key Insights

1. **Developer-Focused Docs:** Provide practical examples for common use cases
2. **Multiple Languages:** Show both curl and Python examples
3. **Use Case Coverage:** Document all 3 automation scenarios
4. **OpenAPI Integration:** Reference auto-generated Swagger UI docs

## Requirements

### Functional Requirements

**FR-04-01: README.md Updates**
- Add "REST API Server" section after "Quick Start"
- Document installation and startup
- List all endpoints with brief descriptions
- Provide quick start examples

**FR-04-02: Endpoint Documentation**
- Document all 6 endpoints with parameters
- Provide curl examples for each endpoint
- Provide Python requests examples
- Include example responses

**FR-04-03: Use Case Examples**
- Document DOE batch execution workflow
- Document model introspection workflow
- Document result processing workflow
- Show API calls for each workflow

**FR-04-04: Configuration Reference**
- Document environment variables
- Explain CORS configuration
- Provide deployment guidance

### Non-Functional Requirements

**NFR-04-01: Documentation Quality**
- Clear, concise examples
- Copy-paste ready code
- Accurate endpoint paths

**NFR-04-02: Discoverability**
- Table of contents for API section
- Links to related docs
- References to OpenAPI/Swagger UI

## Architecture

### Documentation Structure

```
README.md
├── Quick Start (existing)
├── REST API Server (NEW)
│   ├── Installation
│   ├── Starting the Server
│   ├── API Endpoints
│   │   ├── Search
│   │   ├── Method Lookup
│   │   ├── Examples
│   │   ├── Namespaces
│   │   └── Statistics
│   ├── Use Case Workflows
│   │   ├── DOE Batch Execution
│   │   ├── Model Introspection
│   │   └── Result Processing
│   └── Configuration
└── Existing sections...
```

## Related Code Files

### Files to Modify

**README.md** - Add REST API Server section

```markdown
## REST API Server

The ProcessNet Knowledge Base is now available as a REST API server for programmatic access.

### Installation

Install additional dependencies:

```bash
pip install fastapi uvicorn pydantic-settings
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### Starting the Server

Start the API server:

```bash
# Development mode (with auto-reload)
python src/processnet-api-server.py

# Or with uvicorn directly
uvicorn src.processnet-api-server:app --reload --host 127.0.0.1 --port 8000
```

The server will start at http://127.0.0.1:8000

**Important:** Ensure the knowledge base exists at `output/processnet-knowledge.json` before starting.

### API Documentation

Interactive API documentation is available at:
- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

### API Endpoints

#### 1. Search Methods

Fuzzy search for methods and interfaces.

**Endpoint:** `GET /api/v1/search`

**Parameters:**
- `q` (required): Search query
- `threshold` (optional): Fuzzy match threshold 0-100 (default: 60)
- `limit` (optional): Maximum results 1-100 (default: 10)

**Example:**

```bash
# Search for methods matching "CreateArc"
curl "http://127.0.0.1:8000/api/v1/search?q=CreateArc"

# Search with custom threshold
curl "http://127.0.0.1:8000/api/v1/search?q=GetAllBody&threshold=70&limit=5"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/search", params={
    "q": "CreateArc",
    "threshold": 70,
    "limit": 5
})
data = response.json()
print(f"Found {data['count']} results")
for result in data['results']:
    print(f"  - {result['name']}: {result['signature']}")
```

**Response:**
```json
{
  "query": "CreateArc",
  "count": 2,
  "results": [
    {
      "name": "CreateArc",
      "type": "method",
      "namespace": "ProcessNet",
      "signature": "CreateArc(center, radius, start_angle, end_angle)",
      "description": "Creates circular arc",
      "score": 100.0
    }
  ],
  "timing_ms": 12.34
}
```

#### 2. Find Method

Exact method lookup by name.

**Endpoint:** `GET /api/v1/methods/{method_name}`

**Parameters:**
- `method_name` (path): Exact method name
- `namespace` (optional): Filter by namespace

**Example:**

```bash
# Find GetAllBodies method
curl "http://127.0.0.1:8000/api/v1/methods/GetAllBodies"

# Find in specific namespace
curl "http://127.0.0.1:8000/api/v1/methods/Load?namespace=ProcessNet.Result"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/methods/GetAllBodies")
data = response.json()
if data['count'] > 0:
    method = data['results'][0]
    print(f"Method: {method['signature']}")
    print(f"Description: {method['description']}")
```

#### 3. Find Code Examples

Find code examples by keyword.

**Endpoint:** `GET /api/v1/examples`

**Parameters:**
- `keyword` (optional): Filter examples by keyword
- `limit` (optional): Maximum results (default: 10)

**Example:**

```bash
# Get all examples
curl "http://127.0.0.1:8000/api/v1/examples"

# Search geometry examples
curl "http://127.0.0.1:8000/api/v1/examples?keyword=geometry"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/examples", params={
    "keyword": "geometry"
})
data = response.json()
for example in data['results']:
    print(f"Namespace: {example['namespace']}")
    print(f"Code:\n{example['code']}\n")
```

#### 4. List Namespaces

List all available namespaces.

**Endpoint:** `GET /api/v1/namespaces`

**Example:**

```bash
curl "http://127.0.0.1:8000/api/v1/namespaces"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/namespaces")
data = response.json()
print(f"Found {data['count']} namespaces:")
for ns in data['namespaces']:
    print(f"  - {ns}")
```

#### 5. Get Namespace Details

Get detailed namespace contents.

**Endpoint:** `GET /api/v1/namespaces/{name}`

**Example:**

```bash
# Get ProcessNet.Model namespace details
curl "http://127.0.0.1:8000/api/v1/namespaces/ProcessNet.Model"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/namespaces/ProcessNet.Model")
data = response.json()
print(f"Namespace: {data['full_name']}")
print(f"Methods: {len(data['methods'])}")
print(f"Classes: {len(data['classes'])}")
```

#### 6. Get Statistics

Get knowledge base statistics.

**Endpoint:** `GET /api/v1/statistics`

**Example:**

```bash
curl "http://127.0.0.1:8000/api/v1/statistics"
```

```python
import requests

response = requests.get("http://127.0.0.1:8000/api/v1/statistics")
data = response.json()
print(f"Namespaces: {data['namespaces']}")
print(f"Methods: {data['methods']}")
print(f"Examples: {data['examples']}")
```

### Use Case Workflows

#### DOE Batch Execution

Automate Design of Experiments with parameter variation.

```python
import requests

API_BASE = "http://127.0.0.1:8000/api/v1"

# Step 1: Find parameter manipulation methods
methods_needed = ["Clone", "SetParameter", "SaveAs", "GetParameter"]

for method in methods_needed:
    response = requests.get(f"{API_BASE}/methods/{method}")
    data = response.json()
    if data['count'] > 0:
        print(f"{method}: {data['results'][0]['signature']}")

# Output:
# Clone: Clone()
# SetParameter: SetParameter(name, value)
# SaveAs: SaveAs(file_path)
# GetParameter: GetParameter(name)

# Step 2: Find code examples for parameter manipulation
response = requests.get(f"{API_BASE}/examples", params={"keyword": "parameter"})
examples = response.json()
print(f"Found {examples['count']} parameter-related examples")
```

#### Model Introspection

Explore and analyze model structure.

```python
import requests

API_BASE = "http://127.0.0.1:8000/api/v1"

# Step 1: List ProcessNet.Model namespace
response = requests.get(f"{API_BASE}/namespaces/ProcessNet.Model")
ns_data = response.json()

print(f"Namespace: {ns_data['full_name']}")
print(f"Available methods: {len(ns_data['methods'])}")

# Step 2: Find entity enumeration methods
entity_methods = ["GetAllBodies", "GetAllJoints", "GetAllForces"]

for method in entity_methods:
    response = requests.get(f"{API_BASE}/methods/{method}")
    data = response.json()
    if data['count'] > 0:
        result = data['results'][0]
        print(f"{result['name']}: {result['description']}")

# Step 3: Find related examples
response = requests.get(f"{API_BASE}/examples", params={"keyword": "entity"})
examples = response.json()
print(f"Found {examples['count']} entity-related examples")
```

#### Result Processing

Extract and process simulation results.

```python
import requests

API_BASE = "http://127.0.0.1:8000/api/v1"

# Step 1: Find result loading methods
result_methods = ["Load", "GetTimeArray", "GetEntityData"]

for method in result_methods:
    response = requests.get(f"{API_BASE}/methods/{method}")
    data = response.json()
    if data['count'] > 0:
        # Find result-specific methods (filter by namespace if needed)
        for result in data['results']:
            if 'Result' in result['namespace'] or 'result' in result.get('description', '').lower():
                print(f"{result['name']}: {result['signature']}")

# Step 2: Search for result processing examples
response = requests.get(f"{API_BASE}/search?q=result", params={"limit": 10})
data = response.json()
print(f"\nFound {data['count']} result-related items")

# Step 3: Get code examples
response = requests.get(f"{API_BASE}/examples", params={"keyword": "result"})
examples = response.json()
for example in examples['results'][:3]:
    print(f"\nExample from {example['namespace']}:")
    print(example['code'][:200])
```

### Configuration

Configure the API server via environment variables:

```bash
# Server configuration
export API_HOST=127.0.0.1
export API_PORT=8000
export DEBUG=true

# Knowledge base path
export KB_PATH=output/processnet-knowledge.json

# Search defaults
export FUZZY_THRESHOLD=60.0
export SEARCH_LIMIT=10
```

Or create a `.env` file:

```
API_HOST=127.0.0.1
API_PORT=8000
DEBUG=true
KB_PATH=output/processnet-knowledge.json
FUZZY_THRESHOLD=60.0
SEARCH_LIMIT=10
```

### CORS Configuration

For development, CORS is enabled for all origins. For production, modify `src/processnet-api-server.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Troubleshooting

**Server won't start:**
- Ensure knowledge base file exists: `output/processnet-knowledge.json`
- Check port is not already in use
- Verify all dependencies installed

**Empty search results:**
- Try lowering the threshold: `?threshold=50`
- Check query spelling
- Browse namespaces to find correct method names

**404 errors:**
- Verify endpoint path is correct
- Check method/namespace exists via `/api/v1/namespaces`
- Case-insensitive for methods, exact match for namespaces
```

### Files to Create (Optional)

**docs/api-server-usage.md** (if more detailed docs needed)

```markdown
# ProcessNet Knowledge Base REST API - Detailed Usage Guide

Complete reference for REST API server usage.

## Authentication

Currently no authentication required for local development.

## Rate Limiting

No rate limiting for local development.

## Error Codes

| Status | Description | Example |
|--------|-------------|---------|
| 200 | Success | Successful query |
| 400 | Bad Request | Invalid parameter value |
| 404 | Not Found | Method or namespace doesn't exist |
| 422 | Validation Error | Parameter validation failed |
| 500 | Server Error | Unexpected server error |
| 503 | Service Unavailable | Knowledge base not loaded |

## Advanced Usage

### Batch Queries

Process multiple queries efficiently:

```python
import requests
from concurrent.futures import ThreadPoolExecutor

API_BASE = "http://127.0.0.1:8000/api/v1"

methods = ["GetAllBodies", "GetAllJoints", "GetAllForces"]

def get_method(name):
    response = requests.get(f"{API_BASE}/methods/{name}")
    return response.json()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(get_method, methods))

for result in results:
    print(f"{result['query']}: {result['count']} matches")
```

### Response Optimization

Request only needed fields to reduce response size:

```python
import requests

# Note: Current API returns all fields
# Future: Add ?fields=name,signature parameter
response = requests.get("http://127.0.0.1:8000/api/v1/methods/GetAllBodies")
```
```

## Implementation Steps

### Step 1: Update README.md

1. Add new "REST API Server" section after "Quick Start"
2. Include installation instructions
3. Document server startup
4. Link to OpenAPI/Swagger UI

### Step 2: Document Endpoints

1. Document all 6 endpoints
2. Provide curl examples
3. Provide Python requests examples
4. Show example responses

### Step 3: Document Use Cases

1. Write DOE batch execution workflow
2. Write model introspection workflow
3. Write result processing workflow
4. Include complete code examples

### Step 4: Add Configuration Section

1. Document environment variables
2. Explain CORS configuration
3. Provide troubleshooting guide

### Step 5: Create Optional Detailed Guide

1. Create `docs/api-server-usage.md` if needed
2. Add advanced usage examples
3. Document error codes
4. Add best practices

## Todo List

- [ ] Update README.md with API server section
- [ ] Document all 6 endpoints with examples
- [ ] Write DOE batch execution workflow
- [ ] Write model introspection workflow
- [ ] Write result processing workflow
- [ ] Add configuration reference
- [ ] Add troubleshooting section
- [ ] Create optional detailed usage guide
- [ ] Verify all examples work
- [ ] Test curl commands
- [ ] Test Python examples

## Success Criteria

**Documentation Quality:**
- [ ] All endpoints documented with examples
- [ ] All 3 use cases have workflow examples
- [ ] Configuration documented
- [ ] Troubleshooting guide included

**Examples:**
- [ ] All curl commands tested and working
- [ ] All Python examples tested and working
- [ ] Example responses accurate

**Discoverability:**
- [ ] Table of contents updated
- [ ] Links to Swagger UI
- [ ] Cross-references to related docs

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| Outdated examples | Medium | Test all examples before commit |
| Missing endpoints | Low | Verify against Phase 02 implementation |
| Unclear instructions | Low | Review with fresh eyes |

## Next Steps

After completing Phase 04:
1. Review entire plan
2. Verify all phases complete
3. Delegate to implementation agent

## Related Files

- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Phase 02: Endpoint Implementation](./phase-02-rest-api-endpoints-implementation.md)
- [Phase 03: Test Suite](./phase-03-test-suite-for-three-automation-use-cases.md)
- [Project README](../../../README.md)
