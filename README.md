# RecurDyn ProcessNet Knowledge Base Extraction

**Objective:** Extract complete ProcessNet API documentation from RecurDyn installation and build structured knowledge base for automation workflows.

## Overview

This project extracts API documentation from RecurDyn ProcessNet HTML/CHM files and creates a queryable knowledge base for developing automation scripts. It enables Claude Code and other AI assistants to accurately reference ProcessNet APIs when writing automation code.

## Quick Start

### Prerequisites

```bash
# System dependencies (Ubuntu/Debian/WSL)
sudo apt update && sudo apt install -y libchm-bin p7zip-full

# Python dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Extract documentation from RecurDyn installation
python src/recurdyn-doc-parser.py \
    --input /path/to/RecurDyn/Help/ProcessNet \
    --output output/processnet-knowledge.json \
    --markdown output/markdown

# Query the knowledge base interactively
python src/processnet-query-interface.py

# Or search directly from command line
python src/processnet-query-interface.py --search "CreateArc"
python src/processnet-query-interface.py --find "GetAllBodies"
python src/processnet-query-interface.py --examples "geometry"
```

## Project Structure

```
RecurDyn-ProcessNet/
├── docs/                           # Project documentation
│   ├── project-overview-pdr.md     # Product Development Requirements
│   ├── code-standards.md           # Code standards and conventions
│   ├── codebase-summary.md         # Codebase structure summary
│   ├── system-architecture.md      # System architecture documentation
│   ├── project-roadmap.md          # Development roadmap
│   └── tech-stack.md               # Technology stack details
├── knowledge/                      # Source documentation (CHM + HTML)
│   ├── ProcessNetHelp.chm          # CHM file to extract
│   ├── RecurDynHelp/               # Sphinx HTML documentation
│   └── Tutorial/                   # Tutorial HTML files
├── src/                            # Source code
│   ├── recurdyn-doc-parser.py      # HTML/CHM parser
│   ├── processnet-query-interface.py # Query CLI interface
│   └── processnet-api-server.py    # REST API server
├── output/                         # Generated outputs
│   ├── extracted_chm/              # Extracted CHM contents
│   ├── processnet_knowledge.json   # Main knowledge base
│   └── markdown/                   # Generated markdown docs
├── plans/                          # Implementation plans
│   └── reports/                    # Research reports
├── requirements.txt                # Python dependencies
├── ProcessNet_Extraction_Requirements.md  # Detailed requirements
└── ProcessNet_Hybrid_Verification_Workflow.md  # Verification workflow
```

## Key Features

### Documentation Extraction

- **Recursive HTML Discovery**: Processes all files in directory tree
- **Multiple Parsing Strategies**: Handles definition lists, tables, heading structures
- **Content Extraction**: Methods, classes, properties, parameters, code examples
- **Encoding Detection**: Auto-detects file encoding (UTF-8, Windows-1252, Latin-1)

### Query Interface

- **Exact Method Lookup**: O(1) dictionary-based lookup
- **Fuzzy Search**: RapidFuzz-based approximate matching
- **Description Search**: Full-text search in method descriptions
- **Namespace Exploration**: Browse by namespace hierarchy
- **Code Example Finder**: Search and retrieve code examples
- **REST API Server**: HTTP endpoints for automation workflows

### Output Formats

- **JSON Knowledge Base**: Complete API reference with indices
- **Markdown Documentation**: Human-readable reference docs
- **Interactive CLI**: Real-time query interface
- **REST API**: HTTP server for programmatic access

## Target Use Cases

### 1. DOE Batch Execution

Automate Design of Experiments with parameter variation:

```python
# Load base model
model = ProcessNet.Model.Load("base_model.rdyn")

# Create design variations
for mass in [100, 150, 200]:
    for stiffness in [1000, 2000, 3000]:
        variant = model.Clone()
        variant.SetParameter("body_mass", mass)
        variant.SetParameter("spring_k", stiffness)
        variant.SaveAs(f"doe_m{mass}_k{stiffness}.rdyn")
        variant.Run()
```

### 2. Model Introspection

Explore and analyze model structure:

```python
# Read model structure
model = ProcessNet.Model.Load("existing_model.rdyn")

# Map all entities
entity_map = {
    "bodies": [b.GetID() for b in model.GetAllBodies()],
    "joints": [j.GetID() for j in model.GetAllJoints()],
    "forces": [f.GetID() for f in model.GetAllForces()]
}
```

### 3. Result Post-Processing

Extract and process simulation results:

```python
# Process results without opening RecurDyn
result = ProcessNet.Result.Load("sim_output.rsl")

# Extract data
time = result.GetTimeArray()
force_magnitude = result.GetEntityData("Force_1", "Magnitude")
displacement = result.GetEntityData("Body_2", "Displacement_X")
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Python Runtime | Python 3.10+ |
| HTML Parsing | BeautifulSoup4 + lxml |
| Fuzzy Search | RapidFuzz |
| Encoding Detection | chardet |
| CHM Extraction | libchm-bin / p7zip-full |

See [docs/tech-stack.md](docs/tech-stack.md) for detailed technology stack information.

## Documentation

- [Project Overview & PDR](docs/project-overview-pdr.md) - Product Development Requirements
- [Codebase Summary](docs/codebase-summary.md) - Codebase structure overview
- [Code Standards](docs/code-standards.md) - Development conventions
- [System Architecture](docs/system-architecture.md) - Architecture design
- [Project Roadmap](docs/project-roadmap.md) - Development milestones

## Development Workflow

### Extraction Phase

```bash
# Full extraction with verbose logging
python src/recurdyn-doc-parser.py \
    --input knowledge/RecurDynHelp \
    --output output/processnet-knowledge.json \
    --markdown output/markdown \
    --verbose
```

### Query Phase

#### CLI Interface

```bash
# Interactive mode
python src/processnet-query-interface.py

# Commands available:
#   search <query>     - Fuzzy search for methods/interfaces
#   find <method>      - Exact method lookup
#   desc <keywords>    - Search by description
#   list <namespace>   - List namespace contents
#   namespaces         - List all namespaces
#   examples [keyword] - Find code examples
#   stats              - Show statistics
```

#### REST API Server

```bash
# Start the API server
python src/processnet-api-server.py --port 8000

# Or with custom knowledge base path
python src/processnet-api-server.py --kb output/processnet-knowledge.json --port 8080

# API Documentation available at:
#   http://localhost:8000/docs    - Swagger UI
#   http://localhost:8000/redoc   - ReDoc
```

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/stats` | Knowledge base statistics |
| GET | `/api/namespaces` | List all namespaces |
| GET | `/api/namespaces/{name}` | Get namespace details |
| GET | `/api/search?q={query}` | Fuzzy search methods |
| GET | `/api/find/{name}` | Exact method lookup |
| GET | `/api/examples?keyword={kw}` | Find code examples |

**Example API Requests:**

```bash
# Search for methods
curl "http://localhost:8000/api/search?q=save&limit=10"

# Find exact method
curl "http://localhost:8000/api/find/SaveModel"

# Get namespace contents
curl "http://localhost:8000/api/namespaces/ProcessNet.Model"

# Get statistics
curl "http://localhost:8000/api/stats"
```

**Python Client Example:**

```python
import requests

API_BASE = "http://localhost:8000/api"

# Search for save-related methods
response = requests.get(f"{API_BASE}/search", params={"q": "save", "limit": 10})
methods = response.json()["results"]

# Get namespace info
ns = requests.get(f"{API_BASE}/namespaces/ProcessNet.Geometry").json()
print(f"Classes: {len(ns['classes'])}")

# Find specific method
method = requests.get(f"{API_BASE}/find/SaveNewModel").json()
if method["count"] > 0:
    print(f"Found: {method['results'][0]['signature']}")
```

### Verification Workflow

See [ProcessNet_Hybrid_Verification_Workflow.md](ProcessNet_Hybrid_Verification_Workflow.md) for the complete verification protocol.

## Requirements

See [ProcessNet_Extraction_Requirements.md](ProcessNet_Extraction_Requirements.md) for detailed requirements.

## Key Classes

### ProcessNetDocParser

Main parser class for extracting API documentation from HTML files.

**Key Methods:**
- `discover_files()` - Recursively find all documentation files
- `parse_html_file()` - Extract content from single HTML file
- `build_knowledge_base()` - Process all files and build JSON knowledge base
- `generate_markdown()` - Export markdown documentation

**Data Structures:**
- `Parameter` - Method parameter with name, type, description
- `Method` - Method/function with signature, parameters, return type
- `Property` - Class property with type and read-only flag
- `ClassDef` - Class definition with inheritance, methods, properties
- `CodeExample` - Code example with title, code, language
- `Namespace` - Namespace container for classes and methods

### ProcessNetKnowledge

Query interface for searching the knowledge base.

**Key Methods:**
- `find_method()` - Exact method lookup by name
- `search_method_fuzzy()` - Fuzzy search with similarity threshold
- `search_by_description()` - Full-text description search
- `list_namespace_contents()` - Browse namespace hierarchy
- `find_examples()` - Find code examples by keyword
- `get_statistics()` - Knowledge base statistics

## Performance Targets

- **Extraction Speed:** <5 minutes for 500 HTML files
- **Memory Usage:** <500 MB peak during extraction
- **Query Response:** <100ms for any lookup operation
- **Output Size:** 5-50 MB JSON (depends on documentation size)

## Success Criteria

### Minimum Viable Output
- At least 80% of HTML files successfully parsed
- All major namespaces identified (ProcessNet.Model, ProcessNet.Geometry, etc.)
- Method signatures extracted with >90% accuracy
- Query interface returns correct results for test cases

### Optimal Output
- >95% parsing success rate
- Complete parameter type information
- All code examples extracted
- Cross-references preserved
- Markdown output is clean and readable

## Contributing

This project follows the code standards outlined in [docs/code-standards.md](docs/code-standards.md).

## License

This project is part of the RecurDyn ProcessNet automation toolkit.

## Version History

- **v1.0** (2026-01-28) - Initial release with extraction and query capabilities

## Support

For detailed requirements, see [ProcessNet_Extraction_Requirements.md](ProcessNet_Extraction_Requirements.md).

For verification workflow, see [ProcessNet_Hybrid_Verification_Workflow.md](ProcessNet_Hybrid_Verification_Workflow.md).
