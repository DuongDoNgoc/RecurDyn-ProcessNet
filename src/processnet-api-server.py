#!/usr/bin/env python3
"""
ProcessNet Knowledge Base REST API Server

Provides HTTP REST API for querying the ProcessNet API knowledge base.

Usage:
    python processnet-api-server.py [--port PORT] [--host HOST] [--kb PATH]

Endpoints:
    GET /api/health          - Health check
    GET /api/stats           - Knowledge base statistics
    GET /api/namespaces      - List all namespaces
    GET /api/namespaces/{name} - Get namespace contents
    GET /api/search?q={query} - Fuzzy search for methods
    GET /api/find/{name}     - Exact method lookup
    GET /api/examples        - Find code examples
"""

import json
import sys
import importlib.util
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Handle kebab-case module import for processnet-query-interface
_current_dir = Path(__file__).parent
_spec_qi = importlib.util.spec_from_file_location(
    "processnet_query_interface",
    _current_dir / "processnet-query-interface.py"
)
_qi_module = importlib.util.module_from_spec(_spec_qi)
sys.modules["processnet_query_interface"] = _qi_module
_spec_qi.loader.exec_module(_qi_module)

ProcessNetKnowledge = _qi_module.ProcessNetKnowledge


# ============================================================================
# Configuration
# ============================================================================

class APIConfig:
    """API server configuration."""
    DEFAULT_KB_PATH = "output/processnet-knowledge-v5.json"
    DEFAULT_HOST = "127.0.0.1"
    DEFAULT_PORT = 8000

    def __init__(self, kb_path: Optional[str] = None):
        self.kb_path = kb_path or self.DEFAULT_KB_PATH
        self.host = self.DEFAULT_HOST
        self.port = self.DEFAULT_PORT


# ============================================================================
# Singleton Knowledge Base
# ============================================================================

_kb_instance: Optional[ProcessNetKnowledge] = None
_kb_path: Optional[str] = None


def get_knowledge_base(kb_path: str = APIConfig.DEFAULT_KB_PATH) -> ProcessNetKnowledge:
    """Get or create singleton knowledge base instance."""
    global _kb_instance, _kb_path

    if _kb_instance is None or _kb_path != kb_path:
        kb_file = Path(kb_path)
        if not kb_file.exists():
            raise FileNotFoundError(f"Knowledge base not found: {kb_path}")
        _kb_instance = ProcessNetKnowledge(kb_path)
        _kb_path = kb_path

    return _kb_instance


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    config = app.state.config
    try:
        get_knowledge_base(config.kb_path)
        print(f"Knowledge base loaded from: {config.kb_path}")
    except FileNotFoundError as e:
        print(f"Warning: {e}")
    yield
    # Shutdown
    global _kb_instance
    _kb_instance = None


# ============================================================================
# Pydantic Models
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field(description="Server status")
    kb_loaded: bool = Field(description="Whether knowledge base is loaded")
    kb_path: str = Field(description="Path to knowledge base file")


class StatsResponse(BaseModel):
    """Statistics response."""
    namespaces: int = Field(description="Number of namespaces")
    methods: int = Field(description="Number of methods")
    classes: int = Field(description="Number of classes")
    examples: int = Field(description="Number of code examples")
    interfaces: int = Field(description="Number of interfaces")
    extraction_date: str = Field(description="When the knowledge base was extracted")
    files_processed: int = Field(description="Number of HTML files processed")


class NamespaceListResponse(BaseModel):
    """Namespace list response."""
    namespaces: list[str] = Field(description="List of namespace names")
    count: int = Field(description="Total number of namespaces")


class NamespaceDetailResponse(BaseModel):
    """Namespace detail response."""
    name: str = Field(description="Namespace name")
    full_name: str = Field(description="Full qualified name")
    description: str = Field(description="Namespace description")
    classes: list[str] = Field(description="Class names in namespace")
    methods: list[str] = Field(description="Method names in namespace")
    examples_count: int = Field(description="Number of code examples")
    files: list[str] = Field(description="Source files")


class SearchResult(BaseModel):
    """Search result item."""
    name: str = Field(description="Method/class/interface name")
    type: str = Field(description="Type: method, class, interface, or example")
    namespace: str = Field(description="Namespace name")
    signature: str = Field(default="", description="Method signature")
    description: str = Field(default="", description="Description")
    score: float = Field(default=100.0, description="Match score (0-100)")


class SearchResponse(BaseModel):
    """Search response."""
    query: str = Field(description="Search query")
    count: int = Field(description="Number of results")
    results: list[SearchResult] = Field(description="Search results")


class ExampleResult(BaseModel):
    """Code example result."""
    namespace: str = Field(description="Namespace")
    code: str = Field(description="Example code")
    language: str = Field(description="Programming language")
    source_file: str = Field(description="Source HTML file")


class ExamplesResponse(BaseModel):
    """Examples response."""
    count: int = Field(description="Number of examples")
    results: list[ExampleResult] = Field(description="Code examples")


class ErrorResponse(BaseModel):
    """Error response."""
    error: str = Field(description="Error message")
    detail: str = Field(default="", description="Detailed error information")


# ============================================================================
# FastAPI Application
# ============================================================================

def register_routes(app: FastAPI):
    """Register all API routes to the FastAPI application."""

    @app.get("/api/health", response_model=HealthResponse, tags=["Health"])
    async def health_check():
        """Health check endpoint."""
        config = app.state.config
        kb_loaded = Path(config.kb_path).exists()

        return HealthResponse(
            status="healthy" if kb_loaded else "degraded",
            kb_loaded=kb_loaded,
            kb_path=config.kb_path
        )

    @app.get("/api/stats", response_model=StatsResponse, tags=["Statistics"])
    async def get_statistics():
        """Get knowledge base statistics."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            stats = kb.get_statistics()
            return StatsResponse(**stats)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/namespaces", response_model=NamespaceListResponse, tags=["Namespaces"])
    async def list_namespaces():
        """List all available namespaces."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            namespaces = kb.list_namespaces()
            return NamespaceListResponse(namespaces=namespaces, count=len(namespaces))
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/namespaces/{name}", response_model=NamespaceDetailResponse, tags=["Namespaces"])
    async def get_namespace(name: str):
        """Get namespace contents and details."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            contents = kb.list_namespace_contents(name)
            if not contents.get('name'):
                raise HTTPException(status_code=404, detail=f"Namespace not found: {name}")
            return NamespaceDetailResponse(**contents)
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/search", response_model=SearchResponse, tags=["Search"])
    async def search_methods(
        q: str = Query(..., description="Search query", min_length=1),
        threshold: float = Query(60.0, description="Minimum similarity score (0-100)", ge=0, le=100),
        limit: int = Query(10, description="Maximum number of results", ge=1, le=100)
    ):
        """Fuzzy search for methods, classes, and interfaces."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            results = kb.search_method_fuzzy(q, threshold=threshold, limit=limit)
            return SearchResponse(
                query=q,
                count=len(results),
                results=[
                    SearchResult(
                        name=r.name,
                        type=r.type,
                        namespace=r.namespace,
                        signature=r.signature,
                        description=r.description[:200] if r.description else "",
                        score=r.score
                    )
                    for r in results
                ]
            )
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/find/{name}", response_model=SearchResponse, tags=["Search"])
    async def find_method(name: str, namespace: Optional[str] = None):
        """Find method by exact name."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            results = kb.find_method(name, namespace=namespace)
            if not results:
                raise HTTPException(status_code=404, detail=f"Method not found: {name}")
            return SearchResponse(
                query=name,
                count=len(results),
                results=[
                    SearchResult(
                        name=r.name,
                        type=r.type,
                        namespace=r.namespace,
                        signature=r.signature,
                        description=r.description[:200] if r.description else ""
                    )
                    for r in results
                ]
            )
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))

    @app.get("/api/examples", response_model=ExamplesResponse, tags=["Examples"])
    async def find_examples(
        keyword: Optional[str] = Query(None, description="Filter by keyword"),
        limit: int = Query(10, description="Maximum number of results", ge=1, le=100)
    ):
        """Find code examples."""
        try:
            kb = get_knowledge_base(app.state.config.kb_path)
            results = kb.find_examples(keyword=keyword, limit=limit)
            return ExamplesResponse(
                count=len(results),
                results=[
                    ExampleResult(
                        namespace=r['namespace'],
                        code=r['code'],
                        language=r.get('language', 'csharp'),
                        source_file=r.get('source_file', '')
                    )
                    for r in results
                ]
            )
        except FileNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e))


def create_app(kb_path: Optional[str] = None) -> FastAPI:
    """Create and configure FastAPI application with routes."""
    config = APIConfig(kb_path)

    app = FastAPI(
        title="ProcessNet Knowledge Base API",
        description="REST API for querying RecurDyn ProcessNet API documentation",
        version="1.0.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.state.config = config

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routes
    register_routes(app)

    return app


# Global app instance for CLI usage
app = create_app()


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    """CLI entry point for running the server."""
    import argparse

    parser = argparse.ArgumentParser(
        description='ProcessNet Knowledge Base REST API Server'
    )
    parser.add_argument(
        '--host', '-H',
        type=str,
        default='127.0.0.1',
        help='Host to bind to (default: 127.0.0.1)'
    )
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Port to bind to (default: 8000)'
    )
    parser.add_argument(
        '--kb', '-k',
        type=str,
        default='output/processnet-knowledge-v5.json',
        help='Path to knowledge base JSON file'
    )
    parser.add_argument(
        '--reload',
        action='store_true',
        help='Enable auto-reload for development'
    )

    args = parser.parse_args()

    # Update config
    app.state.config = APIConfig(args.kb)
    app.state.config.host = args.host
    app.state.config.port = args.port

    import uvicorn

    print(f"Starting ProcessNet API Server...")
    print(f"Knowledge base: {args.kb}")
    print(f"Server URL: http://{args.host}:{args.port}")
    print(f"API docs: http://{args.host}:{args.port}/docs")

    uvicorn.run(
        "processnet-api-server:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == '__main__':
    main()
