---
title: "Phase 02 - REST API Endpoints Implementation"
description: "Implement all 6 REST API endpoints: search, find, examples, namespaces, namespace detail, and statistics"
status: pending
priority: P1
effort: 3h
tags: [fastapi, endpoints, implementation, routes]
---

# Phase 02 - REST API Endpoints Implementation

## Context Links

- [Plan Overview](./plan.md)
- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Existing ProcessNetKnowledge Class](../../../src/processnet-query-interface.py)
- [Code Standards](../../../docs/code-standards.md)

## Overview

**Priority:** P1 (High)
**Current Status:** Pending
**Estimated Effort:** 3 hours

Implement all 6 REST API endpoints wrapping existing ProcessNetKnowledge class methods. Each endpoint handles input validation, queries the knowledge base, and returns JSON responses with proper HTTP status codes.

## Key Insights

1. **Reuse Existing Logic:** ProcessNetKnowledge already has all query methods implemented
2. **Thin Wrappers:** API endpoints are thin wrappers around existing code
3. **Pydantic Validation:** Use query parameters and path parameters with type validation
4. **Error Mapping:** Map Python exceptions to HTTP status codes (404, 400, 500)

## Requirements

### Functional Requirements

**FR-02-01: Search Endpoint (`GET /api/v1/search`)**
- Query parameter: `q` (search query string)
- Optional: `threshold` (fuzzy match threshold, default 60.0)
- Optional: `limit` (max results, default 10)
- Returns: List of matching methods with scores
- Handles empty results gracefully

**FR-02-02: Find Method Endpoint (`GET /api/v1/methods/{method_name}`)**
- Path parameter: `method_name` (exact method name)
- Optional query: `namespace` (filter by namespace)
- Returns: Exact method matches or 404 if not found
- Case-insensitive matching

**FR-02-03: Examples Endpoint (`GET /api/v1/examples`)**
- Optional query: `keyword` (filter examples by keyword)
- Optional query: `limit` (max results, default 10)
- Returns: List of code examples with namespace info
- Returns all examples if no keyword provided

**FR-02-04: List Namespaces Endpoint (`GET /api/v1/namespaces`)**
- No parameters required
- Returns: List of all namespace names
- Sorted alphabetically

**FR-02-05: Namespace Detail Endpoint (`GET /api/v1/namespaces/{name}`)**
- Path parameter: `name` (namespace name)
- Returns: Detailed namespace contents (classes, methods, examples)
- Returns 404 if namespace not found

**FR-02-06: Statistics Endpoint (`GET /api/v1/statistics`)**
- No parameters required
- Returns: Knowledge base metadata (counts, extraction date)
- Cached response (KB doesn't change)

### Non-Functional Requirements

**NFR-02-01: Response Time**
- All endpoints must respond within 100ms (p50)
- Measure and include timing in response metadata

**NFR-02-02: Error Handling**
- 400 Bad Request for invalid parameters
- 404 Not Found for missing resources
- 500 Internal Server Error for unexpected failures
- Error responses follow standard format

**NFR-02-03: OpenAPI Documentation**
- All endpoints have proper docstrings
- Request/response models documented
- Example requests in Swagger UI

## Architecture

### Endpoint Routes

```
/api/v1/
├── GET /search?q={query}&threshold={60}&limit={10}
│   └── Fuzzy search methods/interfaces
├── GET /methods/{method_name}?namespace={ns}
│   └── Exact method lookup
├── GET /examples?keyword={kw}&limit={10}
│   └── Find code examples
├── GET /namespaces
│   └── List all namespaces
├── GET /namespaces/{name}
│   └── Get namespace details
└── GET /statistics
    └── Knowledge base statistics
```

### Request/Response Flow

```
Client Request
    ↓
FastAPI Route (Pydantic Validation)
    ↓
Dependency Injection (KB Instance)
    ↓
ProcessNetKnowledge Method
    ↓
Response Builder (Pydantic Model)
    ↓
JSON Response + HTTP Status
```

## Related Code Files

### Files to Create

**src/api/routes/search.py** (100 lines)
```python
"""Search endpoints for fuzzy and description search."""

from fastapi import APIRouter, HTTPException, Query
from typing import List
import time

from api.dependencies import get_knowledge_base
from api.models import SearchResponse, SearchResult

router = APIRouter()


@router.get("/search", response_model=SearchResponse)
async def search_methods(
    q: str = Query(..., min_length=1, description="Search query"),
    threshold: float = Query(60.0, ge=0, le=100, description="Fuzzy match threshold"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results")
) -> SearchResponse:
    """
    Fuzzy search for methods and interfaces.

    Uses RapidFuzz for approximate string matching.
    Returns methods with similarity scores above threshold.
    """
    if not q or len(q.strip()) == 0:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")

    start_time = time.time()
    kb = get_knowledge_base()

    try:
        results = kb.search_method_fuzzy(q, threshold=threshold, limit=limit)
        duration_ms = (time.time() - start_time) * 1000

        return SearchResponse(
            query=q,
            count=len(results),
            results=[
                SearchResult(
                    name=r.name,
                    type=r.type,
                    namespace=r.namespace,
                    signature=r.signature,
                    description=r.description,
                    score=r.score
                ) for r in results
            ],
            timing_ms=round(duration_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
```

**src/api/routes/methods.py** (80 lines)
```python
"""Method lookup endpoints."""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
import time

from api.dependencies import get_knowledge_base
from api.models import SearchResponse, SearchResult

router = APIRouter()


@router.get("/methods/{method_name}", response_model=SearchResponse)
async def find_method(
    method_name: str,
    namespace: Optional[str] = Query(None, description="Filter by namespace")
) -> SearchResponse:
    """
    Find method by exact name (case-insensitive).

    Returns all matches across namespaces or filtered by specific namespace.
    Returns 404 if no matches found.
    """
    start_time = time.time()
    kb = get_knowledge_base()

    try:
        results = kb.find_method(method_name, namespace=namespace)
        duration_ms = (time.time() - start_time) * 1000

        if not results:
            raise HTTPException(
                status_code=404,
                detail=f"Method '{method_name}' not found"
            )

        return SearchResponse(
            query=method_name,
            count=len(results),
            results=[
                SearchResult(
                    name=r.name,
                    type=r.type,
                    namespace=r.namespace,
                    signature=r.signature,
                    description=r.description,
                    score=100.0  # Exact match = 100%
                ) for r in results
            ],
            timing_ms=round(duration_ms, 2)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Method lookup failed: {str(e)}")
```

**src/api/routes/examples.py** (90 lines)
```python
"""Code example endpoints."""

from fastapi import APIRouter, Query
from typing import List, Optional
import time

from api.dependencies import get_knowledge_base
from api.models import BaseModel

router = APIRouter()


class CodeExample(BaseModel):
    """Single code example."""

    namespace: str
    code: str
    language: str
    source_file: str


class ExamplesResponse(BaseModel):
    """Examples endpoint response."""

    count: int
    keyword: Optional[str]
    results: List[CodeExample]
    timing_ms: float


@router.get("/examples", response_model=ExamplesResponse)
async def find_examples(
    keyword: Optional[str] = Query(None, description="Filter by keyword"),
    limit: int = Query(10, ge=1, le=100, description="Maximum results")
) -> ExamplesResponse:
    """
    Find code examples.

    Returns all examples or filtered by keyword.
    Code examples include namespace and source file information.
    """
    start_time = time.time()
    kb = get_knowledge_base()

    try:
        results = kb.find_examples(keyword=keyword, limit=limit)
        duration_ms = (time.time() - start_time) * 1000

        return ExamplesResponse(
            count=len(results),
            keyword=keyword,
            results=[
                CodeExample(
                    namespace=r['namespace'],
                    code=r['code'],
                    language=r['language'],
                    source_file=r['source_file']
                ) for r in results
            ],
            timing_ms=round(duration_ms, 2)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Examples lookup failed: {str(e)}")
```

**src/api/routes/namespaces.py** (100 lines)
```python
"""Namespace endpoints."""

from fastapi import APIRouter, HTTPException
from typing import List
import time

from api.dependencies import get_knowledge_base
from api.models import NamespaceContents

router = APIRouter()


class NamespaceListResponse(BaseModel):
    """Namespace list response."""

    count: int
    namespaces: List[str]


@router.get("/namespaces", response_model=NamespaceListResponse)
async def list_namespaces() -> NamespaceListResponse:
    """
    List all available namespaces.

    Returns sorted list of namespace names.
    Use namespace detail endpoint for full contents.
    """
    start_time = time.time()
    kb = get_knowledge_base()

    try:
        namespaces = kb.list_namespaces()
        duration_ms = (time.time() - start_time) * 1000

        return NamespaceListResponse(
            count=len(namespaces),
            namespaces=sorted(namespaces)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Namespace list failed: {str(e)}")


@router.get("/namespaces/{name}", response_model=NamespaceContents)
async def get_namespace(name: str) -> NamespaceContents:
    """
    Get namespace contents.

    Returns detailed information about namespace including
    classes, methods, and example count.
    Returns 404 if namespace not found.
    """
    start_time = time.time()
    kb = get_knowledge_base()

    try:
        contents = kb.list_namespace_contents(name)
        duration_ms = (time.time() - start_time) * 1000

        # Check if namespace exists (empty dict = not found)
        if not contents.get('name') or contents['name'] != name:
            raise HTTPException(
                status_code=404,
                detail=f"Namespace '{name}' not found"
            )

        return NamespaceContents(**contents)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Namespace lookup failed: {str(e)}")
```

**src/api/routes/statistics.py** (50 lines)
```python
"""Statistics endpoint."""

from fastapi import APIRouter, HTTPException
import time

from api.dependencies import get_knowledge_base
from api.models import StatisticsResponse

router = APIRouter()


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics() -> StatisticsResponse:
    """
    Get knowledge base statistics.

    Returns metadata about the knowledge base including
    method counts, extraction date, and file processing stats.
    """
    start_time = time.time()
    kb = get_knowledge_base()

    try:
        stats = kb.get_statistics()
        duration_ms = (time.time() - start_time) * 1000

        return StatisticsResponse(
            namespaces=stats['namespaces'],
            methods=stats['methods'],
            classes=stats['classes'],
            examples=stats['examples'],
            interfaces=stats['interfaces'],
            extraction_date=stats['extraction_date'],
            files_processed=stats['files_processed']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics retrieval failed: {str(e)}")
```

### Files to Modify

**src/processnet-api-server.py** - Update to include new routers
```python
# Include routers (add these lines)
from api.routes import health, search, methods, namespaces, statistics, examples
app.include_router(health.router, tags=["Health"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(methods.router, prefix="/api/v1", tags=["Methods"])
app.include_router(examples.router, prefix="/api/v1", tags=["Examples"])
app.include_router(namespaces.router, prefix="/api/v1", tags=["Namespaces"])
app.include_router(statistics.router, prefix="/api/v1", tags=["Statistics"])
```

## Implementation Steps

### Step 1: Create Search Endpoint

1. Create `src/api/routes/search.py`
2. Implement `/search` endpoint with query validation
3. Add fuzzy threshold and limit parameters
4. Test with various queries

### Step 2: Create Method Lookup Endpoint

1. Create `src/api/routes/methods.py`
2. Implement `/methods/{method_name}` endpoint
3. Add optional namespace filter
4. Return 404 for not found methods

### Step 3: Create Examples Endpoint

1. Create `src/api/routes/examples.py`
2. Implement `/examples` endpoint
3. Add optional keyword filter
4. Return code examples with metadata

### Step 4: Create Namespace Endpoints

1. Create `src/api/routes/namespaces.py`
2. Implement `/namespaces` list endpoint
3. Implement `/namespaces/{name}` detail endpoint
4. Handle 404 for missing namespaces

### Step 5: Create Statistics Endpoint

1. Create `src/api/routes/statistics.py`
2. Implement `/statistics` endpoint
3. Return KB metadata

### Step 6: Update Main Application

1. Update `src/processnet-api-server.py`
2. Include all new routers
3. Update root endpoint with new URLs

### Step 7: Test All Endpoints

```bash
# Test each endpoint
curl "http://127.0.0.1:8000/api/v1/search?q=CreateArc"
curl "http://127.0.0.1:8000/api/v1/methods/GetAllBodies"
curl "http://127.0.0.1:8000/api/v1/examples"
curl "http://127.0.0.1:8000/api/v1/namespaces"
curl "http://127.0.0.1:8000/api/v1/namespaces/ProcessNet.Model"
curl "http://127.0.0.1:8000/api/v1/statistics"
```

### Step 8: Verify OpenAPI Docs

1. Navigate to http://127.0.0.1:8000/docs
2. Verify all endpoints documented
3. Test endpoints from Swagger UI
4. Verify request/response schemas

## Todo List

- [ ] Create search.py with /search endpoint
- [ ] Create methods.py with /methods/{name} endpoint
- [ ] Create examples.py with /examples endpoint
- [ ] Create namespaces.py with list and detail endpoints
- [ ] Create statistics.py with /statistics endpoint
- [ ] Update main app to include all routers
- [ ] Test all endpoints with curl
- [ ] Verify OpenAPI documentation
- [ ] Test error cases (404, 400)
- [ ] Measure response times

## Success Criteria

**Functional:**
- [ ] All 6 endpoints return correct responses
- [ ] Search returns fuzzy matches with scores
- [ ] Find method returns exact matches or 404
- [ ] Examples filter by keyword correctly
- [ ] Namespace list returns sorted names
- [ ] Namespace detail returns full contents
- [ ] Statistics returns KB metadata

**Technical:**
- [ ] Response time <100ms for all endpoints
- [ ] Proper HTTP status codes (200, 404, 400, 500)
- [ ] CORS headers present
- [ ] OpenAPI docs complete and accurate

**Error Handling:**
- [ ] 404 for missing methods/namespaces
- [ ] 400 for invalid parameters
- [ ] 500 for unexpected errors with details

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| KB load failure | High | Graceful 503 error, clear message |
| Slow queries | Medium | Add caching, monitor performance |
| Parameter validation | Low | Pydantic handles validation |
| Case sensitivity issues | Low | Normalize to lowercase in search |

## Security Considerations

**Input Validation:**
- Pydantic validates all inputs
- Length limits on string parameters
- Range limits on numeric parameters

**Rate Limiting (Future):**
- Not needed for local development
- Consider for production deployment

**CORS:**
- Already configured in Phase 01
- Allows browser access for development

## Next Steps

After completing Phase 02:
1. **Phase 03:** Write comprehensive test suite for 3 use cases
2. **Phase 04:** Update documentation with usage examples

## Related Files

- [Phase 01: Framework Setup](./phase-01-api-server-framework-setup.md)
- [Phase 03: Test Suite](./phase-03-test-suite.md)
- [Existing ProcessNetKnowledge](../../../src/processnet-query-interface.py)
