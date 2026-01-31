"""
Shared pytest fixtures for ProcessNet Hybrid Verification Tests
"""
import json
import pytest
from pathlib import Path
from typing import Dict, List
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Import using exec to handle kebab-case module names
import importlib.util

# Load parser module
spec_parser = importlib.util.spec_from_file_location(
    "recurdyn_doc_parser",
    Path(__file__).parent.parent / "src" / "recurdyn-doc-parser.py"
)
parser_module = importlib.util.module_from_spec(spec_parser)
spec_parser.loader.exec_module(parser_module)

ProcessNetDocParser = parser_module.ProcessNetDocParser
Method = parser_module.Method
ClassDef = parser_module.ClassDef
Namespace = parser_module.Namespace
CodeExample = parser_module.CodeExample
Property = parser_module.Property

# Load query interface module
spec_qi = importlib.util.spec_from_file_location(
    "processnet_query_interface",
    Path(__file__).parent.parent / "src" / "processnet-query-interface.py"
)
qi_module = importlib.util.module_from_spec(spec_qi)
spec_qi.loader.exec_module(qi_module)

ProcessNetKnowledge = qi_module.ProcessNetKnowledge
SearchResult = qi_module.SearchResult
FUZZY_AVAILABLE = qi_module.FUZZY_AVAILABLE


@pytest.fixture(scope="session")
def test_fixtures_dir() -> Path:
    """Return path to test fixtures directory."""
    return Path(__file__).parent / 'fixtures' / 'sample-html'


@pytest.fixture(scope="session")
def screenshots_dir() -> Path:
    """Return path to screenshots directory."""
    screenshots = Path(__file__).parent / 'screenshots'
    screenshots.mkdir(exist_ok=True)
    return screenshots


@pytest.fixture(scope="session")
def sample_file_paths(test_fixtures_dir: Path) -> Dict[str, Path]:
    """
    Provide paths to 5 representative sample files.

    File types:
    - index: Overview/TOC structure
    - namespace: Namespace-level documentation
    - class: Class definition with methods
    - methods: Detailed method documentation
    - examples: Tutorial/example documentation
    """
    return {
        'index': test_fixtures_dir / 'index.html',
        'namespace': test_fixtures_dir / 'namespace-geometry.html',
        'class': test_fixtures_dir / 'class-body.html',
        'methods': test_fixtures_dir / 'methods-create.html',
        'examples': test_fixtures_dir / 'examples-tutorial.html'
    }


@pytest.fixture(scope="session")
def parser_instance(tmp_path_factory) -> ProcessNetDocParser:
    """
    Provide a ProcessNetDocParser instance with temporary output.

    Scope: session to reuse across tests.
    """
    temp_dir = tmp_path_factory.mktemp("parser_output")
    output_path = temp_dir / "knowledge-base.json"

    # Create parser with test fixtures as input
    fixtures_dir = Path(__file__).parent / 'fixtures' / 'sample-html'
    parser = ProcessNetDocParser(
        input_path=fixtures_dir,
        output_path=output_path
    )

    return parser


@pytest.fixture(scope="session")
def knowledge_base(parser_instance: ProcessNetDocParser, sample_file_paths: Dict[str, Path]) -> Dict:
    """
    Loaded knowledge base from sample file extraction.

    Scope: session to run extraction once and reuse results.
    """
    # Process sample files
    for file_type, file_path in sample_file_paths.items():
        if file_path.exists():
            parser_instance.parse_html_file(file_path)

    # Return the knowledge base dictionary
    return parser_instance.knowledge_base


@pytest.fixture
def extraction_results(knowledge_base: Dict) -> Dict:
    """
    Cached extraction results for validation.

    Returns dict with counts and extracted data.
    """
    return {
        'methods_count': knowledge_base['metadata'].get('total_methods', 0),
        'classes_count': knowledge_base['metadata'].get('total_classes', 0),
        'examples_count': knowledge_base['metadata'].get('total_examples', 0),
        'namespaces': list(knowledge_base.get('namespaces', {}).keys()),
        'method_index': knowledge_base.get('method_index', {}),
        'class_index': knowledge_base.get('class_index', {})
    }


@pytest.fixture
def tolerance_config() -> Dict[str, float]:
    """
    Tolerance thresholds for count validation.

    Default: ±20% tolerance for method/class counts.
    """
    return {
        'count_tolerance_percent': 0.20,  # 20%
        'min_success_rate': 0.98,  # 98%
        'min_accuracy': 0.90,  # 90%
        'min_spot_check_pass': 0.85  # 85%
    }


@pytest.fixture
def use_case_methods() -> Dict[str, List[str]]:
    """
    Required methods for each use case.

    Based on project-overview-pdr.md use case definitions.
    """
    return {
        'UC-1-DOE': [
            'Load',
            'Clone',
            'SetParameter',
            'Run',
            'SaveAs'
        ],
        'UC-2-Model': [
            'GetAllBodies',
            'GetAllJoints',
            'GetEntityByID',
            'GetID',
            'GetType'
        ],
        'UC-3-Result': [
            'Load',
            'GetTimeArray',
            'GetEntityData',
            'Export'
        ]
    }


@pytest.fixture
def expected_sample_data() -> Dict:
    """
    Expected data for sample file validation.

    Updated based on actual fixture content.
    """
    return {
        'index': {
            'title': 'ProcessNet API Reference',
            'has_toc': True
        },
        'namespace': {
            'namespace': 'ProcessNet.Geometry',
            'min_classes': 3
        },
        'class': {
            'class_name': 'Body',
            'namespace': 'ProcessNet.Model',
            'expected_methods': 15,
            'tolerance': 3  # ±20% of 15
        },
        'methods': {
            'method_count': 10,
            'has_signatures': True,
            'signature_pattern': r'\([^)]*\)'  # Contains parentheses
        },
        'examples': {
            'min_code_blocks': 2,
            'language': 'csharp'
        }
    }
