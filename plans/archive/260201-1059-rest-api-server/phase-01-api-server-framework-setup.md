---
title: "Phase 01 - API Server Framework Setup"
description: "Setup FastAPI project structure with uvicorn server and basic application skeleton"
status: pending
priority: P1
effort: 2h
tags: [fastapi, setup, framework, infrastructure]
---

# Phase 01 - API Server Framework Setup

## Context Links

- [Plan Overview](./plan.md)
- [Project README](../../../README.md)
- [Code Standards](../../../docs/code-standards.md)
- [System Architecture](../../../docs/system-architecture.md)

## Overview

**Priority:** P1 (High)
**Current Status:** Pending
**Estimated Effort:** 2 hours

Setup FastAPI project structure with uvicorn ASGI server. Create basic application skeleton with health check endpoint, CORS configuration, and ProcessNetKnowledge integration.

## Key Insights

1. **FastAPI Choice:** Native async support, automatic OpenAPI docs, type validation
2. **Minimal Dependencies:** Only need fastapi + uvicorn (use existing rapidfuzz, beautifulsoup4)
3. **Reuse Existing Code:** ProcessNetKnowledge class already has all query methods
4. **Development Experience:** FastAPI provides Swagger UI automatically at /docs

## Requirements

### Functional Requirements

**FR-01-01: FastAPI Application Structure**
- Create FastAPI app instance with proper configuration
- Define API versioning prefix (/api/v1)
- Implement health check endpoint for monitoring
- Configure CORS for browser access

**FR-01-02: ProcessNetKnowledge Integration**
- Import ProcessNetKnowledge class from existing module
- Initialize KB instance at app startup (singleton pattern)
- Handle KB load failures gracefully
- Provide KB reload endpoint (optional)

**FR-01-03: Development Server Configuration**
- Setup uvicorn with auto-reload for development
- Configure host/port via environment variables
- Enable debug mode for development
- Setup logging configuration

**FR-01-04: Error Handling Framework**
- Create exception handlers for common errors
- Define standard error response format
- Implement 404 handler
- Implement 500 handler with logging

### Non-Functional Requirements

**NFR-01-01: Startup Time**
- Application must start within 2 seconds
- KB loading must not block startup (use lifespan)

**NFR-01-02: Code Standards**
- Follow project coding standards (kebab-case files, type hints)
- Maintain <200 lines per file principle
- Use dataclasses for response models

**NFR-01-03: Configuration**
- Use environment variables for configuration
- Provide sensible defaults
- Support local development and production modes

## Architecture

### Application Structure

```
src/
├── processnet-api-server.py           # FastAPI app (main entry)
├── api/
│   ├── __init__.py
│   ├── config.py                      # Configuration management
│   ├── models.py                      # Pydantic response models
│   ├── dependencies.py                # Dependency injection (KB instance)
│   └── routes/
│       ├── __init__.py
│       ├── health.py                  # Health check endpoint
│       ├── search.py                  # Search endpoints
│       ├── methods.py                 # Method lookup endpoints
│       ├── namespaces.py              # Namespace endpoints
│       └── statistics.py              # Statistics endpoint
```

### Component Interaction

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              Lifespan Manager (startup/shutdown)       │ │
│  │  • Load ProcessNetKnowledge                          │ │
│  │  • Initialize search indices                         │ │
│  │  • Setup logging                                     │ │
│  └────────────────────────────────────────────────────────┘ │
│                              │                              │
│                              ▼                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            API Routes (endpoints)                      │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │ │
│  │  │  Health  │  │  Search  │  │ Methods  │  │  Stats │ │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘ │ │
│  └───────┼─────────────┼─────────────┼─────────────┼──────┘ │
│          │             │             │             │        │
│          ▼             ▼             ▼             ▼        │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         ProcessNetKnowledge (singleton)                 │ │
│  │  • find_method()       • search_method_fuzzy()         │ │
│  │  • find_examples()     • list_namespace_contents()     │ │
│  │  • get_statistics()    • list_namespaces()             │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
HTTP Request → FastAPI Route → Dependency Injection (KB)
    → ProcessNetKnowledge Method → Pydantic Model → JSON Response
```

## Related Code Files

### Files to Create

**src/processnet-api-server.py** (150 lines)
```python
#!/usr/bin/env python3
"""
ProcessNet Knowledge Base REST API Server

FastAPI application for querying ProcessNet API documentation.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from api.config import settings
from api.dependencies import get_knowledge_base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - load KB on startup."""
    # Startup
    kb = get_knowledge_base()
    print(f"Knowledge base loaded: {kb.get_statistics()}")
    yield
    # Shutdown
    print("Shutting down API server")


# Create FastAPI app
app = FastAPI(
    title="ProcessNet Knowledge Base API",
    description="REST API for querying RecurDyn ProcessNet API documentation",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
from api.routes import health, search, methods, namespaces, statistics
app.include_router(health.router, tags=["Health"])
app.include_router(search.router, prefix="/api/v1", tags=["Search"])
app.include_router(methods.router, prefix="/api/v1", tags=["Methods"])
app.include_router(namespaces.router, prefix="/api/v1", tags=["Namespaces"])
app.include_router(statistics.router, prefix="/api/v1", tags=["Statistics"])


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "ProcessNet Knowledge Base API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "search": "/api/v1/search?q={query}",
            "find": "/api/v1/methods/{method_name}",
            "examples": "/api/v1/examples",
            "namespaces": "/api/v1/namespaces",
            "statistics": "/api/v1/statistics"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "processnet-api-server:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
```

**src/api/config.py** (40 lines)
```python
"""API configuration management."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings from environment variables."""

    # API Server
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = True

    # Knowledge Base
    KB_PATH: str = "output/processnet-knowledge.json"

    # Search Configuration
    FUZZY_THRESHOLD: float = 60.0
    SEARCH_LIMIT: int = 10

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
```

**src/api/dependencies.py** (50 lines)
```python
"""Dependency injection for FastAPI routes."""

from functools import lru_cache
from pathlib import Path

from sys import path
path.insert(0, str(Path(__file__).parent.parent))

from processnet_query_interface import ProcessNetKnowledge
from api.config import settings


@lru_cache()
def get_knowledge_base() -> ProcessNetKnowledge:
    """
    Get ProcessNetKnowledge singleton instance.

    Cached to avoid reloading KB on each request.
    Raises FileNotFoundError if KB file missing.

    Returns:
        ProcessNetKnowledge: Loaded knowledge base instance
    """
    kb_path = settings.KB_PATH
    kb = ProcessNetKnowledge(kb_path)
    return kb


def reload_knowledge_base() -> ProcessNetKnowledge:
    """
    Force reload knowledge base (clears cache).

    Use after updating knowledge base file.

    Returns:
        ProcessNetKnowledge: Reloaded knowledge base instance
    """
    get_knowledge_base.cache_clear()
    return get_knowledge_base()
```

**src/api/models.py** (80 lines)
```python
"""Pydantic models for API responses."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Server status")
    timestamp: datetime = Field(default_factory=datetime.now)
    kb_loaded: bool = Field(..., description="Knowledge base loaded successfully")


class SearchResult(BaseModel):
    """Single search result."""

    name: str = Field(..., description="Method/interface name")
    type: str = Field(..., description="Result type: method, class, interface, example")
    namespace: str = Field(..., description="Namespace containing the result")
    signature: Optional[str] = Field(None, description="Method signature")
    description: Optional[str] = Field(None, description="Method description")
    score: Optional[float] = Field(None, description="Fuzzy match score (0-100)")


class SearchResponse(BaseModel):
    """Search endpoint response."""

    query: str = Field(..., description="Search query used")
    count: int = Field(..., description="Number of results returned")
    results: List[SearchResult] = Field(..., description="Search results")
    timing_ms: float = Field(..., description="Query execution time in milliseconds")


class NamespaceContents(BaseModel):
    """Namespace contents response."""

    name: str = Field(..., description="Namespace name")
    full_name: str = Field(..., description="Full namespace name")
    description: str = Field(..., description="Namespace description")
    classes: List[str] = Field(default_factory=list, description="Class names")
    methods: List[str] = Field(default_factory=list, description="Method names")
    examples_count: int = Field(..., description="Number of code examples")


class StatisticsResponse(BaseModel):
    """Knowledge base statistics response."""

    namespaces: int = Field(..., description="Number of namespaces")
    methods: int = Field(..., description="Total methods")
    classes: int = Field(..., description="Total classes")
    examples: int = Field(..., description="Total code examples")
    interfaces: int = Field(..., description="Total interfaces")
    extraction_date: str = Field(..., description="Knowledge base extraction date")
    files_processed: int = Field(..., description="Number of files processed")


class ErrorResponse(BaseModel):
    """Error response."""

    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
```

**src/api/routes/health.py** (30 lines)
```python
"""Health check endpoint."""

from fastapi import APIRouter, HTTPException
from api.dependencies import get_knowledge_base
from api.models import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns server status and knowledge base load status.
    Use for monitoring and readiness probes.
    """
    try:
        kb = get_knowledge_base()
        stats = kb.get_statistics()
        return HealthResponse(
            status="healthy",
            kb_loaded=stats['namespaces'] > 0
        )
    except FileNotFoundError:
        raise HTTPException(status_code=503, detail="Knowledge base not loaded")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")
```

### Files to Modify

**requirements.txt** - Add FastAPI dependencies
```
# HTML Parsing
beautifulsoup4>=4.12.0
lxml>=5.0.0

# Fuzzy Search
rapidfuzz>=3.0.0

# Encoding Detection
chardet>=5.0.0

# REST API Server
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic-settings>=2.0.0

# Testing
pytest>=7.4.0
httpx>=0.25.0
pytest-cov>=4.1.0
```

## Implementation Steps

### Step 1: Create Directory Structure

```bash
mkdir -p src/api/routes
touch src/api/__init__.py
touch src/api/routes/__init__.py
```

### Step 2: Install Dependencies

```bash
pip install fastapi uvicorn pydantic-settings pytest httpx pytest-cov
```

### Step 3: Create Configuration Module

1. Create `src/api/config.py`
2. Define Settings class with environment variables
3. Add default values for local development
4. Create .env.example file

### Step 4: Create Dependency Injection

1. Create `src/api/dependencies.py`
2. Implement get_knowledge_base() with lru_cache
3. Handle FileNotFoundError gracefully
4. Add reload function for development

### Step 5: Create Response Models

1. Create `src/api/models.py`
2. Define Pydantic models for all responses
3. Add Field descriptions for OpenAPI docs
4. Include typing for all fields

### Step 6: Create Health Check Route

1. Create `src/api/routes/health.py`
2. Implement /health endpoint
3. Test KB loading
4. Return proper status codes

### Step 7: Create Main Application

1. Create `src/processnet-api-server.py`
2. Setup FastAPI app with lifespan
3. Configure CORS middleware
4. Add root endpoint
5. Include routers (placeholder for now)

### Step 8: Test Basic Server

```bash
# Start development server
python src/processnet-api-server.py

# Test endpoints
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/docs
```

## Todo List

- [ ] Create directory structure (src/api/routes)
- [ ] Update requirements.txt with FastAPI dependencies
- [ ] Create config.py with Settings class
- [ ] Create dependencies.py with KB singleton
- [ ] Create models.py with Pydantic response models
- [ ] Create routes/health.py with health check endpoint
- [ ] Create processnet-api-server.py main application
- [ ] Test server startup and health check
- [ ] Verify OpenAPI docs at /docs
- [ ] Test CORS with browser request

## Success Criteria

**Functional:**
- [ ] Server starts without errors
- [ ] Health check endpoint returns 200 OK
- [ ] Knowledge base loads successfully
- [ ] Root endpoint returns API information
- [ ] OpenAPI docs accessible at /docs

**Technical:**
- [ ] Startup time <2 seconds
- [ ] No blocking KB load (uses lifespan)
- [ ] CORS headers present in response
- [ ] Proper error handling on KB load failure

**Code Quality:**
- [ ] All files follow code standards
- [ ] Type hints on all functions
- [ ] Docstrings on all public functions
- [ ] File sizes <200 lines

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| KB load time >2s | Low | Cache KB instance, show loading message |
| Path issues (KB not found) | Medium | Validate path on startup, clear error message |
| CORS blocking browser requests | Low | Allow all origins for development |
| Port already in use | Low | Configurable via env variable |

## Security Considerations

**For Local Development:**
- Allow all origins (CORS)
- No authentication required
- Bind to 127.0.0.1 (localhost only)

**For Production (Future):**
- Restrict CORS origins
- Add API key authentication
- Use HTTPS
- Bind to specific interface
- Rate limiting

## Next Steps

After completing Phase 01:
1. **Phase 02:** Implement all 6 REST API endpoints
2. **Phase 03:** Write comprehensive test suite
3. **Phase 04:** Update documentation

## Related Files

- [Phase 02: Endpoint Implementation](./phase-02-endpoint-implementation.md)
- [Code Standards](../../../docs/code-standards.md)
- [System Architecture](../../../docs/system-architecture.md)
