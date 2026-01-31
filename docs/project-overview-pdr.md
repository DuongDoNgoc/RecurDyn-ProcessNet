# RecurDyn ProcessNet - Project Overview & Product Development Requirements

**Date:** 2026-01-28
**Version:** 1.0
**Status:** Active Development

## Executive Summary

The RecurDyn ProcessNet Knowledge Base Extraction project transforms RecurDyn's proprietary HTML/CHM documentation into a structured, queryable knowledge base. This enables AI-assisted development of automation workflows for Design of Experiments (DOE), model introspection, and result post-processing.

**Business Value:** Reduces automation development time from weeks to days by providing accurate API reference for AI code generation.

**Technical Approach:** Python-based HTML parsing with BeautifulSoup, fuzzy search capabilities, and multiple output formats (JSON, Markdown, interactive CLI).

## Problem Statement

### Current Challenges

1. **Proprietary Documentation Format**: RecurDyn ProcessNet API documentation exists only in CHM (compiled HTML) and scattered HTML files
2. **No Searchable API Reference**: Developers must manually browse documentation to find methods and signatures
3. **High Learning Curve**: Automation development requires extensive trial-and-error to discover correct API usage
4. **Inefficient Automation Development**: Each automation script requires manual API lookup and verification

### Impact on Development

- **Time Loss**: 2-4 hours per automation task spent on API discovery
- **Error-Prone**: Manual transcription of method signatures leads to bugs
- **Limited Reusability**: Knowledge stays with individual developers
- **Slow Iteration**: Changes require re-consulting documentation

## Solution Overview

### Core Offering

Transform static ProcessNet documentation into:
1. **Machine-Readable Knowledge Base** - JSON format with indexed search
2. **Human-Readable Documentation** - Markdown reference files
3. **Interactive Query Interface** - CLI tool for real-time API lookup

### Key Capabilities

| Capability | Description |
|------------|-------------|
| Recursive HTML Discovery | Processes ALL files in documentation directory tree |
| Multi-Strategy Parsing | Handles definition lists, tables, heading structures |
| Encoding Detection | Auto-detects UTF-8, Windows-1252, Latin-1 |
| Exact Method Lookup | O(1) dictionary-based search |
| Fuzzy Search | RapidFuzz approximate matching for typos/variations |
| Description Search | Full-text search in method documentation |
| Namespace Browsing | Hierarchical exploration of API structure |
| Code Example Finder | Search and retrieve usage examples |

## Product Development Requirements (PDR)

### Functional Requirements

#### FR-1: Documentation Extraction

**Priority:** P0 (Critical)

The system SHALL extract API documentation from RecurDyn HTML/CHM files:

- **FR-1.1**: Recursively discover all HTML files in specified directory
- **FR-1.2**: Extract method signatures with parameter names and types
- **FR-1.3**: Extract class definitions with inheritance chains
- **FR-1.4**: Extract property definitions with type information
- **FR-1.5**: Extract code examples with language detection
- **FR-1.6**: Detect and handle multiple file encodings
- **FR-1.7**: Parse multiple HTML layout patterns (definition lists, tables, headings)
- **FR-1.8**: Generate JSON knowledge base with metadata and indices

**Acceptance Criteria:**
- Processes 100% of discoverable HTML files (excluding excluded patterns)
- Extracts method signatures with >90% accuracy
- Captures code examples from 95% of files containing examples
- Generates valid JSON with complete namespace hierarchy

#### FR-2: Knowledge Base Structure

**Priority:** P0 (Critical)

The system SHALL organize extracted content into structured format:

- **FR-2.1**: Namespaces as top-level containers
- **FR-2.2**: Classes within appropriate namespaces
- **FR-2.3**: Methods within classes or as standalone functions
- **FR-2.4**: Parameters with name, type, and description
- **FR-2.5**: Properties with type and read-only flag
- **FR-2.6**: Code examples with title, code, and language
- **FR-2.7**: Cross-references between related elements
- **FR-2.8**: Source file tracking for traceability

**Acceptance Criteria:**
- JSON structure validates against defined schema
- All namespaces from source docs are represented
- Method indices enable O(1) lookup by name
- Namespace hierarchy reflects original documentation structure

#### FR-3: Query Interface

**Priority:** P0 (Critical)

The system SHALL provide search and query capabilities:

- **FR-3.1**: Exact method lookup by name (case-insensitive)
- **FR-3.2**: Fuzzy search with configurable similarity threshold
- **FR-3.3**: Full-text search in method descriptions
- **FR-3.4**: Namespace content listing
- **FR-3.5**: Code example search by keyword
- **FR-3.6**: Interactive CLI mode with command history
- **FR-3.7**: JSON output format for programmatic access
- **FR-3.8**: Statistics and metadata reporting

**Acceptance Criteria:**
- Exact lookup returns results in <100ms
- Fuzzy search returns relevant matches for typos (80%+ similarity)
- Description search finds methods by conceptual keywords
- Interactive mode supports all query types
- CLI provides help and usage instructions

#### FR-4: Documentation Export

**Priority:** P1 (High)

The system SHALL generate human-readable documentation:

- **FR-4.1**: Markdown files per namespace
- **FR-4.2**: Table of contents for large files
- **FR-4.3**: Cross-references between related items
- **FR-4.4**: Code examples with syntax highlighting
- **FR-4.5**: Method signatures in code blocks
- **FR-4.6**: Parameter tables with types and descriptions
- **FR-4.7**: Namespace overview with statistics

**Acceptance Criteria:**
- Markdown files render correctly in standard viewers
- Code blocks preserve indentation and formatting
- Internal links resolve correctly
- Files are readable without additional processing

#### FR-5: Error Handling

**Priority:** P1 (High)

The system SHALL handle errors gracefully:

- **FR-5.1**: Log files that fail to parse with error reasons
- **FR-5.2**: Continue processing on individual file errors
- **FR-5.3**: Generate error summary report
- **FR-5.4**: Validate input paths before processing
- **FR-5.5**: Handle encoding failures with fallback chain
- **FR-5.6**: Warn on missing expected content (methods, examples)
- **FR-5.7**: Provide progress feedback during extraction

**Acceptance Criteria:**
- Individual file errors don't stop batch processing
- Error log includes file path and specific error
- Progress indicator shows current file and percentage
- Warnings logged for suspicious conditions

#### FR-6: Test Automation

**Priority:** P1 (High)

The system SHALL include comprehensive automated testing with browser verification:

- **FR-6.1**: pytest framework with >80% code coverage
- **FR-6.2**: Unit tests for all parser components
- **FR-6.3**: Integration tests for complete workflows
- **FR-6.4**: MCP Playwright browser verification for visual validation
- **FR-6.5**: Spot-check validation with 98% accuracy target
- **FR-6.6**: Regression tests for parser adjustments
- **FR-6.7**: Test markers for 5-phase test pipeline (@pytest.mark.phase_1 through phase_5)
- **FR-6.8**: Fixture-based test data management

**Acceptance Criteria:**
- Test suite executes in <2 minutes
- Browser verification completes in <5 seconds per file
- Code coverage >80%
- Method signature accuracy 90%+
- Spot-check validation achieves 98% accuracy
- All 3 use cases have test coverage
- Zero regressions on parser adjustments

### Non-Functional Requirements

#### NFR-1: Performance

- **NFR-1.1**: Extraction speed: <5 minutes for 500 HTML files
- **NFR-1.2**: Query response: <100ms for any lookup operation
- **NFR-1.3**: Memory usage: <500 MB peak during extraction
- **NFR-1.4**: Startup time: <2 seconds to load knowledge base

#### NFR-2: Reliability

- **NFR-2.1**: Parsing success rate: >80% of HTML files
- **NFR-2.2**: Zero data loss: All extracted content preserved in output
- **NFR-2.3**: Reproducible: Same input produces same output
- **NFR-2.4**: Error recovery: Graceful degradation on malformed HTML

#### NFR-3: Usability

- **NFR-3.1**: CLI follows standard conventions (--help, --version)
- **NFR-3.2**: Error messages are actionable and specific
- **NFR-3.3**: Interactive mode provides help and examples
- **NFR-3.4**: Output formats are documented with examples

#### NFR-4: Maintainability

- **NFR-4.1**: Code follows project coding standards
- **NFR-4.2**: Functions have docstrings with examples
- **NFR-4.3**: Type hints used for all function signatures
- **NFR-4.4**: Modular design enables easy extension

#### NFR-5: Compatibility

- **NFR-5.1**: Python 3.10+ runtime
- **NFR-5.2**: Linux/Windows/WSL compatibility
- **NFR-5.3**: Handles Windows-style paths in input
- **NFR-5.4**: Works with multiple HTML encoding formats

#### NFR-6: Test Automation

- **NFR-6.1**: Test execution: <2 minutes for full suite
- **NFR-6.2**: Browser verification: <5 seconds per file
- **NFR-6.3**: Code coverage: >80% of codebase
- **NFR-6.4**: Spot-check accuracy: 98% success rate
- **NFR-6.5**: Method signature accuracy: 90%+ correctness
- **NFR-6.6**: Fixture setup time: <10 seconds
- **NFR-6.7**: MCP Playwright integration: 100% operational

## Target Use Cases

### UC-1: DOE Batch Execution

**Actor:** Automation Engineer
**Goal:** Run parameter study with multiple design variations

**Workflow:**
1. Load base RecurDyn model
2. Define parameter ranges (mass, stiffness, dimensions)
3. Generate design variants
4. Execute simulations in batch
5. Collect results for analysis

**Required API Methods:**
- `Model.Load()` - Load model file
- `Model.Clone()` - Create copy of model
- `SetParameter()` - Modify model parameters
- `Run()` - Execute simulation
- `SaveAs()` - Save variant with naming convention

**Success Metrics:**
- Can generate 100+ design variants automatically
- All simulations complete without manual intervention
- Results organized for post-processing

### UC-2: Model Introspection

**Actor:** Automation Engineer
**Goal:** Analyze and understand model structure programmatically

**Workflow:**
1. Load existing model
2. Enumerate all entities (bodies, joints, forces)
3. Extract entity properties and relationships
4. Generate model structure report
5. Create similar entities programmatically

**Required API Methods:**
- `GetAllBodies()` - List all bodies
- `GetAllJoints()` - List all joints
- `GetEntityByID()` - Retrieve specific entity
- `GetID()` - Get entity identifier
- `GetType()` - Get entity type
- `CreateBodyLike()` - Create entity from template

**Success Metrics:**
- Can map complete model hierarchy
- Entity properties extracted correctly
- Can replicate model structure automatically

### UC-3: Result Post-Processing

**Actor:** Data Analyst / Automation Engineer
**Goal:** Extract and analyze simulation results without GUI

**Workflow:**
1. Load result file (.rsl)
2. Extract time series data
3. Query entity-specific results
4. Export to CSV/Excel for analysis
5. Generate plots and reports

**Required API Methods:**
- `Result.Load()` - Load result file
- `GetTimeArray()` - Extract time points
- `GetEntityData()` - Get entity time series
- `Export()` - Export to external format

**Success Metrics:**
- Can process results without opening RecurDyn
- Batch processing of multiple result files
- Data exported in standard formats

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Documentation Source                     │
│  (HTML files, CHM archives, RecurDyn installation)         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  ProcessNetDocParser                         │
│  • File discovery (recursive)                               │
│  • Encoding detection                                       │
│  • HTML parsing (BeautifulSoup)                             │
│  • Content extraction (methods, classes, examples)          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Knowledge Base                            │
│  • JSON structure with namespaces, classes, methods         │
│  • Method index (O(1) lookup)                               │
│  • Class index                                              │
│  • Interface index                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
    ┌───────────┐ ┌──────────┐ ┌──────────────┐
    │  JSON     │ │Markdown  │ │   Query      │
    │  Export   │ │ Export   │ │  Interface   │
    └───────────┘ └──────────┘ └──────────────┘
                                              │
                                              ▼
                                  ┌──────────────────────┐
                                  │   Interactive CLI    │
                                  │ • Exact search       │
                                  │ • Fuzzy search       │
                                  │ • Description search │
                                  │ • Namespace browse   │
                                  └──────────────────────┘
```

### Data Flow

1. **Extraction Phase**
   - Input: HTML/CHM files from RecurDyn installation
   - Processing: BeautifulSoup parsing → Content extraction → Index building
   - Output: JSON knowledge base + Markdown docs

2. **Query Phase**
   - Input: Search query (method name, keyword, description)
   - Processing: Index lookup → Result assembly → Formatting
   - Output: Formatted results (console/JSON)

## Success Criteria

### Minimum Viable Product (MVP)

- [ ] Extracts API documentation from HTML files
- [ ] Generates JSON knowledge base with namespaces and methods
- [ ] Provides exact method lookup via CLI
- [ ] Achieves >80% file parsing success rate
- [ ] Extracts method signatures with >90% accuracy

### Production Ready

- [ ] >95% parsing success rate
- [ ] Complete parameter type information
- [ ] All code examples extracted and formatted
- [ ] Cross-references preserved between elements
- [ ] Fuzzy search with configurable threshold
- [ ] Markdown documentation with cross-references
- [ ] Interactive CLI with help and examples
- [ ] Error handling with detailed logging
- [ ] Performance targets met (<5min extraction, <100ms queries)

### Complete Feature Set

- [ ] All MVP and production criteria met
- [ ] Description search (full-text in method docs)
- [ ] Namespace browsing with hierarchy
- [ ] Code example finder with keyword search
- [ ] Statistics and metadata reporting
- [ ] Validation against test cases for all 3 use cases
- [ ] Documentation complete with examples
- [ ] Verification workflow executed and passed

## Technical Constraints

### Dependencies

- **Python 3.10+** - Required runtime
- **BeautifulSoup4 4.12+** - HTML parsing
- **lxml 5.0+** - Fast parser backend
- **RapidFuzz 3.0+** - Fuzzy string matching
- **chardet 5.0+** - Encoding detection
- **libchm-bin** - CHM extraction (system package)

### Limitations

- **Static HTML Only**: Does not execute JavaScript or handle dynamic content
- **Documentation Structure**: Assumes standard Sphinx/HTML documentation format
- **Encoding Coverage**: Handles common encodings but may fail on rare ones
- **File Size**: Large HTML files (>10MB) may cause memory issues

### Assumptions

- RecurDyn documentation follows predictable HTML patterns
- CHM files can be extracted with standard tools
- Method signatures are consistent across documentation
- Code examples use Python/IronPython syntax

## Risk Assessment

### High Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| Non-standard HTML structure | High | Multiple parsing strategies with fallbacks |
| Encoding issues | Medium | Auto-detection with fallback chain |
| Large file count performance | Medium | Progress tracking and optimization |

### Medium Risk

| Risk | Impact | Mitigation |
|------|--------|------------|
| CHM extraction failures | Medium | Multiple extraction tools (libchm, 7zip) |
| Memory constraints | Low | Streaming parsing for large files |
| API changes in future RecurDyn | Low | Version tracking in metadata |

## Quality Assurance

### Testing Strategy

**5-Phase Test Integration Plan with MCP Playwright**

#### Phase 1: Test Infrastructure
- pytest framework setup with conftest.py
- Fixture-based test data management
- Test markers for organization (@pytest.mark.phase_N)
- Target: >80% code coverage

#### Phase 2: MCP Playwright Browser Verification
- Automated browser verification using MCP Playwright
- Visual method counting via DOM inspection
- Screenshot capture for comparison
- Target: <5 seconds per file, >98% success rate

#### Phase 3: Sample Extraction Validation
- Extract 5 representative file types (geometry, model, body, joint, force)
- Verify extraction completeness
- Test different HTML patterns (definition lists, tables, headings)
- Target: >90% method extraction accuracy

#### Phase 4: Parser Adjustment & Regression Tests
- Identify and fix extraction gaps from Phase 3
- Regression test suite for table-based extraction
- Preserve formatting and highlight information
- Target: Zero regressions, 95%+ accuracy

#### Phase 5: Spot-Check & Use Case Coverage
- Random sampling of 50+ extracted methods
- Browser-based spot-check validation
- Verify all 3 use cases have adequate coverage
- Target: 98% spot-check accuracy, 90%+ method signatures

### Test Organization

**Structure (tests/):**
```
tests/
├── conftest.py                              # Shared fixtures
├── test_parser.py                           # Unit tests (Phase 1)
├── test_query_interface.py                  # Unit tests (Phase 1)
├── test_integration.py                      # Integration (Phase 3-4)
├── test_mcp_playwright_verification.py      # Browser tests (Phase 2, 5)
├── test_data/
│   ├── fixtures/
│   │   ├── definition_list.html
│   │   ├── table_based.html
│   │   ├── heading_based.html
│   │   └── code_example.html
│   └── sample_files/
│       ├── geometry.html
│       ├── model.html
│       ├── body.html
│       ├── joint.html
│       └── force.html
└── test_samples/
    └── extracted_methods.json               # Phase 4 regression baseline
```

### Success Metrics

| Metric | Target | Phase |
|--------|--------|-------|
| Test Execution Time | <2 minutes | All |
| Code Coverage | >80% | 1 |
| Browser Verification | <5 sec/file | 2, 5 |
| Extraction Accuracy | >90% | 3, 5 |
| Spot-Check Accuracy | 98% | 5 |
| Method Signatures | 90%+ correct | 5 |
| Use Case Coverage | 3/3 | 5 |

### Verification Protocol

See [ProcessNet_Hybrid_Verification_Workflow.md](../ProcessNet_Hybrid_Verification_Workflow.md) for complete verification protocol.

**Browser-Based Validation:**
- MCP Playwright for automated visual verification
- DOM inspection for method counting
- Screenshot comparison for accuracy validation
- Spot-check sampling with 98% accuracy target

### Acceptance Testing

**Phase-Based Acceptance:**
1. Phase 1: Test infrastructure initialized with >80% coverage
2. Phase 2: Browser verification operational, <5 second performance
3. Phase 3: Sample files extract with >90% accuracy
4. Phase 4: Parser adjustments have zero regressions
5. Phase 5: 98% spot-check accuracy achieved, all use cases validated

**Final Validation:**
- Extract sample documentation files
- Verify extraction accuracy with browser-based checks
- Validate query interface returns correct results
- Test all 3 use cases with generated knowledge base

## Implementation Roadmap

See [docs/project-roadmap.md](project-roadmap.md) for detailed development timeline.

## Documentation

- [Codebase Summary](codebase-summary.md) - Code structure overview
- [Code Standards](code-standards.md) - Development conventions
- [System Architecture](system-architecture.md) - Architecture details
- [Project Roadmap](project-roadmap.md) - Development milestones
- [Tech Stack](tech-stack.md) - Technology stack details

## Related Documents

- [ProcessNet_Extraction_Requirements.md](../ProcessNet_Extraction_Requirements.md) - Detailed technical requirements
- [ProcessNet_Hybrid_Verification_Workflow.md](../ProcessNet_Hybrid_Verification_Workflow.md) - Verification workflow
- [requirements.txt](../requirements.txt) - Python dependencies

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-28 | Initial PDR document |

## Approval

**Product Owner:** _Pending_
**Technical Lead:** _Pending_
**Date Approved:** _Pending_

---

**Document Status:** Draft
**Next Review:** Upon MVP completion
**Maintainer:** Development Team
