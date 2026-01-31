"""
CLI, Markdown Export, and End-to-End Workflow Tests

Tests for:
1. CLI argument parsing and execution
2. Markdown generation functionality
3. Full extraction → query → export pipeline

Phase 1: Test Infrastructure - Coverage improvement
"""

import json
import pytest
from pathlib import Path
from typing import Dict
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

# Load query interface module
spec_qi = importlib.util.spec_from_file_location(
    "processnet_query_interface",
    Path(__file__).parent.parent / "src" / "processnet-query-interface.py"
)
qi_module = importlib.util.module_from_spec(spec_qi)
spec_qi.loader.exec_module(qi_module)

ProcessNetKnowledge = qi_module.ProcessNetKnowledge


class TestCLIExecution:
    """Test CLI argument parsing and execution path."""

    def test_parser_accepts_input_argument(self, tmp_path):
        """Test that parser accepts --input argument."""
        input_dir = tmp_path / "html"
        input_dir.mkdir()
        output_file = tmp_path / "output.json"

        parser = ProcessNetDocParser(input_dir, output_file)
        assert parser.input_path == input_dir
        assert parser.output_path == output_file

    def test_parser_creates_output_directory(self, tmp_path):
        """Test that markdown output directory is created."""
        input_dir = tmp_path / "html"
        input_dir.mkdir()
        output_file = tmp_path / "output.json"
        markdown_dir = tmp_path / "markdown"

        parser = ProcessNetDocParser(input_dir, output_file)
        parser.build_knowledge_base()  # Empty build
        parser.save_knowledge_base()
        parser.generate_markdown(markdown_dir)

        assert markdown_dir.exists()
        assert markdown_dir.is_dir()

    def test_main_function_exists(self):
        """Test that main() function is callable."""
        assert hasattr(parser_module, 'main')
        assert callable(parser_module.main)


class TestMarkdownGeneration:
    """Test markdown export functionality."""

    @pytest.fixture
    def populated_parser(self, tmp_path, sample_html_content):
        """Create parser with sample HTML content."""
        input_dir = tmp_path / "html"
        input_dir.mkdir()
        output_file = tmp_path / "output.json"

        # Create sample HTML file
        html_file = input_dir / "test.html"
        html_file.write_text(sample_html_content, encoding='utf-8')

        parser = ProcessNetDocParser(input_dir, output_file)
        parser.build_knowledge_base()

        return parser

    @pytest.fixture
    def sample_html_content(self):
        """Sample HTML content for testing."""
        return '''<!DOCTYPE html>
<html>
<head><title>Test Namespace</title></head>
<body>
    <h1>ProcessNet.Test</h1>
    <dl>
        <dt>TestMethod(param1: str) -> None</dt>
        <dd>A test method for validation.</dd>
    </dl>
    <div class="highlight">
        <pre><code>def example():
    pass</code></pre>
    </div>
</body>
</html>'''

    def test_markdown_file_created(self, populated_parser, tmp_path):
        """Test that markdown files are generated."""
        markdown_dir = tmp_path / "markdown"
        populated_parser.save_knowledge_base()
        populated_parser.generate_markdown(markdown_dir)

        # Check for markdown files
        md_files = list(markdown_dir.glob("*.md"))
        assert len(md_files) > 0

    def test_markdown_contains_namespace(self, populated_parser, tmp_path):
        """Test that markdown contains namespace information."""
        markdown_dir = tmp_path / "markdown"
        populated_parser.save_knowledge_base()
        populated_parser.generate_markdown(markdown_dir)

        # Find and check markdown file
        md_files = list(markdown_dir.glob("*.md"))
        if md_files:
            content = md_files[0].read_text()
            # Should contain namespace or method info
            assert "ProcessNet" in content or "Test" in content

    def test_markdown_contains_methods(self, populated_parser, tmp_path):
        """Test that markdown includes method documentation."""
        markdown_dir = tmp_path / "markdown"
        populated_parser.save_knowledge_base()
        populated_parser.generate_markdown(markdown_dir)

        md_files = list(markdown_dir.glob("*.md"))
        if md_files:
            content = md_files[0].read_text()
            # Should contain method section
            assert "## Methods" in content or "TestMethod" in content


class TestEndToEndWorkflow:
    """Test complete extraction → query → export pipeline."""

    @pytest.fixture
    def e2e_test_setup(self, tmp_path):
        """Set up complete E2E test environment."""
        # Create test HTML files
        input_dir = tmp_path / "html"
        input_dir.mkdir()

        # Sample HTML files representing different documentation types
        html_content = {
            'geometry.html': '''<!DOCTYPE html>
<html>
<head><title>Geometry Namespace</title></head>
<body>
    <h1>ProcessNet.Geometry</h1>
    <p>Geometry creation and manipulation.</p>
    <dl>
        <dt>CreateArc(center: Point, radius: double) -> Arc</dt>
        <dd>Creates an arc with specified center and radius.</dd>
        <dt>CreateLine(start: Point, end: Point) -> Line</dt>
        <dd>Creates a line between two points.</dd>
    </dl>
</body>
</html>''',
            'model.html': '''<!DOCTYPE html>
<html>
<head><title>Model Namespace</title></head>
<body>
    <h1>ProcessNet.Model</h1>
    <p>Model manipulation methods.</p>
    <dl>
        <dt>Load(filePath: str) -> Model</dt>
        <dd>Loads a model from the specified file path.</dd>
        <dt>Clone() -> Model</dt>
        <dd>Creates a copy of the current model.</dd>
    </dl>
</body>
</html>'''
        }

        for filename, content in html_content.items():
            (input_dir / filename).write_text(content, encoding='utf-8')

        output_file = tmp_path / "knowledge-base.json"
        markdown_dir = tmp_path / "markdown"

        return {
            'input_dir': input_dir,
            'output_file': output_file,
            'markdown_dir': markdown_dir,
            'expected_methods': ['CreateArc', 'CreateLine', 'Load', 'Clone']
        }

    def test_e2e_extraction_creates_json(self, e2e_test_setup):
        """Test complete extraction creates valid JSON."""
        parser = ProcessNetDocParser(
            e2e_test_setup['input_dir'],
            e2e_test_setup['output_file']
        )
        parser.build_knowledge_base()
        parser.save_knowledge_base()

        # Verify JSON file created
        assert e2e_test_setup['output_file'].exists()

        # Verify JSON is valid
        with open(e2e_test_setup['output_file'], 'r') as f:
            kb = json.load(f)

        assert 'metadata' in kb
        assert 'namespaces' in kb
        assert 'method_index' in kb

    def test_e2e_extraction_creates_markdown(self, e2e_test_setup):
        """Test complete extraction creates markdown files."""
        parser = ProcessNetDocParser(
            e2e_test_setup['input_dir'],
            e2e_test_setup['output_file']
        )
        parser.build_knowledge_base()
        parser.save_knowledge_base()
        parser.generate_markdown(e2e_test_setup['markdown_dir'])

        # Verify markdown directory created
        assert e2e_test_setup['markdown_dir'].exists()

        # Verify markdown files exist
        md_files = list(e2e_test_setup['markdown_dir'].glob("*.md"))
        assert len(md_files) > 0

    def test_e2e_query_interface_works(self, e2e_test_setup):
        """Test that query interface can load and search knowledge base."""
        # First create knowledge base
        parser = ProcessNetDocParser(
            e2e_test_setup['input_dir'],
            e2e_test_setup['output_file']
        )
        parser.build_knowledge_base()
        parser.save_knowledge_base()

        # Now query it
        kb = ProcessNetKnowledge(str(e2e_test_setup['output_file']))

        # Test method lookup
        results = kb.find_method("Load")
        assert len(results) > 0

    def test_e2e_full_pipeline(self, e2e_test_setup):
        """Test complete pipeline: extract → save → query → export."""
        # Step 1: Extract
        parser = ProcessNetDocParser(
            e2e_test_setup['input_dir'],
            e2e_test_setup['output_file']
        )
        parser.build_knowledge_base()
        parser.save_knowledge_base()
        parser.generate_markdown(e2e_test_setup['markdown_dir'])

        # Step 2: Verify JSON
        assert e2e_test_setup['output_file'].exists()
        assert e2e_test_setup['markdown_dir'].exists()

        # Step 3: Query
        kb = ProcessNetKnowledge(str(e2e_test_setup['output_file']))

        # Verify all expected methods are findable
        for method_name in e2e_test_setup['expected_methods']:
            results = kb.find_method(method_name)
            assert len(results) > 0, f"Method {method_name} not found"

        # Step 4: Verify markdown has content
        md_files = list(e2e_test_setup['markdown_dir'].glob("*.md"))
        assert len(md_files) > 0
        total_md_content = ""
        for md_file in md_files:
            total_md_content += md_file.read_text()

        # Verify at least some methods appear in markdown
        methods_in_md = sum(1 for m in e2e_test_setup['expected_methods']
                           if m in total_md_content)
        assert methods_in_md >= 2  # At least 2 methods should appear


class TestFileDiscovery:
    """Test file discovery and encoding detection."""

    def test_excludes_patterns_are_respected(self, tmp_path):
        """Test that exclude patterns filter files correctly."""
        input_dir = tmp_path / "html"
        input_dir.mkdir()

        # Create files that should be excluded
        (input_dir / "_static").mkdir()
        (input_dir / "_static" / "style.css").write_text("css")

        (input_dir / "_images").mkdir()
        (input_dir / "_images" / "img.png").write_bytes(b"png")

        # Create file that should be included
        (input_dir / "api.html").write_text("<html><body>API</body></html>")

        parser = ProcessNetDocParser(input_dir, tmp_path / "out.json")
        discovered = parser.discover_files()

        # Only html file should be discovered
        assert len(discovered) == 1
        assert discovered[0].name == "api.html"

    def test_recursive_directory_scan(self, tmp_path):
        """Test that file discovery is recursive."""
        input_dir = tmp_path / "html"
        input_dir.mkdir()

        # Create nested structure
        (input_dir / "level1").mkdir()
        (input_dir / "level1" / "level2").mkdir()

        (input_dir / "root.html").write_text("<html><body>Root</body></html>")
        (input_dir / "level1" / "nested.html").write_text("<html><body>Nested</body></html>")
        (input_dir / "level1" / "level2" / "deep.html").write_text("<html><body>Deep</body></html>")

        parser = ProcessNetDocParser(input_dir, tmp_path / "out.json")
        discovered = parser.discover_files()

        # All HTML files should be found
        assert len(discovered) == 3
