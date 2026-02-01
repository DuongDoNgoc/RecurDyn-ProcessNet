# REST API Layer - Detailed Architecture

**Date:** 2026-02-01
**Version:** 1.0

## Overview

The REST API Layer provides HTTP REST API endpoints for programmatic access to the ProcessNet knowledge base. Built with FastAPI, it offers async/await support, automatic OpenAPI documentation, and CORS-enabled browser access.

## FastAPI Server Architecture

### Server Lifecycle Management

```python
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

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

## API Endpoints

### 1. Health Check

**Endpoint:** `GET /api/health`

**Purpose:** Verify server is running

**Response:**
```json
{
    "status": "healthy"
}
```

**Implementation:**
```python
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
```

### 2. Statistics

**Endpoint:** `GET /api/stats`

**Purpose:** Get knowledge base statistics

**Response:**
```json
{
    "total_namespaces": 23,
    "total_classes": 1803,
    "total_methods": 5606,
    "total_properties": 13377,
    "total_parameters": 6035,
    "extraction_date": "2026-02-01T12:00:00"
}
```

### 3. List Namespaces

**Endpoint:** `GET /api/namespaces`

**Purpose:** List all available namespaces

**Response:**
```json
{
    "namespaces": [
        "ProcessNet",
        "ProcessNet.Model",
        "ProcessNet.Geometry",
        "ProcessNet.GUI"
    ],
    "count": 23
}
```

### 4. Get Namespace Details

**Endpoint:** `GET /api/namespaces/{name}`

**Purpose:** Get detailed information about a namespace

**Parameters:**
- `name` (path) - Namespace name

**Response:**
```json
{
    "name": "ProcessNet.Model",
    "full_name": "FunctionBay.RecurDyn.ProcessNet.Model",
    "description": "ProcessNet Model API",
    "classes": ["Body", "Joint", "Force"],
    "methods": ["GetAllBodies", "GetAllJoints"],
    "files": ["model.html"]
}
```

### 5. Fuzzy Search

**Endpoint:** `GET /api/search?q={query}`

**Purpose:** Search for methods using fuzzy matching

**Parameters:**
- `q` (query) - Search query
- `limit` (optional) - Max results (default: 10)
- `threshold` (optional) - Similarity threshold (default: 60.0)

**Response:**
```json
{
    "count": 5,
    "query": "save",
    "results": [
        {
            "name": "Save",
            "type": "method",
            "namespace": "ProcessNet.Model",
            "signature": "Save(filePath: str)",
            "description": "Save model to file",
            "score": 100.0
        }
    ]
}
```

### 6. Exact Method Lookup

**Endpoint:** `GET /api/find/{name}`

**Purpose:** Find method by exact name

**Parameters:**
- `name` (path) - Method name
- `namespace` (optional query) - Filter by namespace

**Response:**
```json
{
    "count": 1,
    "results": [
        {
            "name": "CreateArc",
            "type": "method",
            "namespace": "ProcessNet.Geometry",
            "signature": "CreateArc(center, radius, start_angle, end_angle)",
            "description": "Creates circular arc"
        }
    ]
}
```

### 7. Find Code Examples

**Endpoint:** `GET /api/examples?keyword={keyword}`

**Purpose:** Find code examples by keyword

**Parameters:**
- `keyword` (query) - Search keyword
- `limit` (optional) - Max results (default: 10)

**Response:**
```json
{
    "count": 3,
    "results": [
        {
            "title": "Creating Geometry",
            "code": "arc = CreateArc([0,0,0], 50, 0, 90)",
            "language": "csharp",
            "description": "Example of creating arc",
            "source_file": "examples.html"
        }
    ]
}
```

## Pydantic Models

### Method Response Model

```python
from pydantic import BaseModel, Field

class MethodResponse(BaseModel):
    """Method response model."""
    name: str = Field(..., description="Method name")
    type: str = Field(..., description="Type: method, class, or example")
    namespace: str = Field(..., description="Namespace containing the method")
    signature: str = Field(default="", description="Method signature")
    description: str = Field(default="", description="Method description")
    score: float = Field(default=100.0, description="Fuzzy match score")
```

### Search Response Model

```python
class SearchResponse(BaseModel):
    """Search response model."""
    count: int = Field(..., description="Number of results")
    query: str = Field(..., description="Search query")
    results: list[MethodResponse] = Field(default_factory=list)
```

### Statistics Response Model

```python
class StatsResponse(BaseModel):
    """Statistics response model."""
    total_namespaces: int
    total_classes: int
    total_methods: int
    total_properties: int
    total_parameters: int
    extraction_date: str
```

## Error Handling

### HTTPException Pattern

```python
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
```

### Error Response Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error |

## OpenAPI Documentation

### Automatic Documentation

FastAPI automatically generates OpenAPI documentation:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

### Custom Documentation

```python
@app.get("/api/search", response_model=SearchResponse)
async def search_methods(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Max results"),
    threshold: float = Query(60.0, ge=0, le=100, description="Similarity threshold")
):
    """
    Search for methods using fuzzy matching.

    Returns methods with names similar to the query string.
    Uses RapidFuzz for similarity scoring.
    """
    results = app.state.kb.search_method_fuzzy(q, threshold=threshold, limit=limit)
    return SearchResponse(count=len(results), query=q, results=[asdict(r) for r in results])
```

## Server Deployment

### Development Server

```bash
# Start with default settings
python src/processnet-api-server.py

# Custom port
python src/processnet-api-server.py --port 8080

# Custom knowledge base path
python src/processnet-api-server.py --kb /path/to/knowledge.json
```

### Production Server

```bash
# Use uvicorn with multiple workers
uvicorn processnet-api-server:app --host 0.0.0.0 --port 8000 --workers 4

# With SSL
uvicorn processnet-api-server:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

## Integration Testing

### Test Pattern

```python
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

## Performance Characteristics

| Operation | Target | Actual |
|-----------|--------|--------|
| Health check | <10ms | <5ms |
| Statistics | <50ms | <20ms |
| Namespace list | <50ms | <30ms |
| Namespace details | <100ms | <50ms |
| Fuzzy search | <200ms | <100ms |
| Exact lookup | <50ms | <20ms |
| Code examples | <100ms | <50ms |

## Related Documents

- [System Architecture Index](./index.md) - Overview
- [Extraction Layer](./extraction-layer-details.md) - How data is extracted
- [Query Layer](./query-layer-details.md) - Query interface implementation
- [Code Standards](../code-standards.md) - REST API coding standards

---

**Last Updated:** 2026-02-01
**Maintainer:** Development Team
