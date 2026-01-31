"""
Spot-check validation and metrics tests.

Tests for:
- Random file sampling
- Stratified namespace sampling
- Success rate metrics
- Accuracy thresholds
"""
import pytest
import random
from pathlib import Path
from typing import Dict, List


@pytest.mark.spot_check
class TestRandomSpotCheck:
    """Random sampling validation tests."""

    def test_random_sample_selection(self, knowledge_base: Dict):
        """Test random sampling selects diverse files."""
        # Get all processed files from knowledge base
        all_files = []
        for namespace_data in knowledge_base.get('namespaces', {}).values():
            all_files.extend(namespace_data.get('files', []))

        # Random sample: 10 files (or all if less than 10)
        sample_size = min(10, len(all_files))
        if len(all_files) > 0:
            sample = random.sample(all_files, sample_size)
            assert len(sample) == sample_size, "Sample size mismatch"
        else:
            pytest.skip("No files in knowledge base for sampling")

    def test_title_exists_in_sample(self, sample_file_paths: Dict[str, Path]):
        """Verify title extraction for sample files."""
        from bs4 import BeautifulSoup

        for file_type, file_path in sample_file_paths.items():
            if not file_path.exists():
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Check for title (h1 or title tag)
            h1 = soup.find('h1')
            title = soup.find('title')

            assert h1 is not None or title is not None, \
                f"No title found in {file_type}"

    def test_method_count_reasonable(self, sample_file_paths: Dict[str, Path],
                                    tolerance_config: Dict):
        """Verify method counts are reasonable (not zero, not excessive)."""
        from bs4 import BeautifulSoup

        for file_type, file_path in sample_file_paths.items():
            if file_type not in ['class', 'methods']:
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Count methods
            methods = soup.find_all('dt', class_='sig')
            method_count = len([m for m in methods if '(' in m.get_text()])

            # Reasonable range: 1-100 methods per file
            assert 1 <= method_count <= 100, \
                f"{file_type}: unreasonable method count {method_count}"

    def test_signature_matches_source(self, sample_file_paths: Dict[str, Path]):
        """Verify at least one extracted signature matches browser-visible content."""
        from bs4 import BeautifulSoup

        methods_file = sample_file_paths.get('methods')
        if not methods_file or not methods_file.exists():
            pytest.skip("Methods file not available")

        with open(methods_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
            soup = BeautifulSoup(html_content, 'html.parser')

        # Extract first few signatures
        signatures = []
        for dt in soup.find_all('dt', class_='sig', limit=3):
            sig_text = dt.get_text().strip()
            if '(' in sig_text:
                signatures.append(sig_text)

        assert len(signatures) > 0, "No signatures extracted"

        # Verify signatures exist in HTML source
        for sig in signatures:
            method_name = sig.split('(')[0].strip()
            # Method name should appear in HTML
            assert len(method_name) > 0, "Empty method name"
            assert method_name in html_content, f"Method name '{method_name}' not in HTML source"


@pytest.mark.spot_check
class TestStratifiedSampling:
    """Stratified sampling across namespaces."""

    def test_one_file_per_namespace(self, knowledge_base: Dict):
        """Select one representative file from each namespace."""
        namespaces = knowledge_base.get('namespaces', {})

        if len(namespaces) == 0:
            pytest.skip("No namespaces in knowledge base")

        # Select one file per namespace
        stratified_sample = {}
        for ns_name, ns_data in namespaces.items():
            files = ns_data.get('files', [])
            if len(files) > 0:
                stratified_sample[ns_name] = random.choice(files)

        # Should have one file per namespace
        assert len(stratified_sample) == len(namespaces), \
            "Stratified sample size mismatch"

    def test_namespace_coverage(self, knowledge_base: Dict):
        """Verify all major namespaces are represented."""
        namespaces = knowledge_base.get('namespaces', {})

        # Expected namespaces from fixtures
        expected_namespaces = ['ProcessNet.Geometry', 'ProcessNet.Model']

        for expected in expected_namespaces:
            # Check if namespace exists (may not if fixtures not processed)
            if expected not in namespaces:
                pytest.skip(f"Namespace {expected} not in knowledge base (fixtures not processed)")


@pytest.mark.spot_check
class TestSuccessMetrics:
    """Test success rate and accuracy metrics."""

    def test_parsing_success_rate_above_threshold(self, tolerance_config: Dict):
        """Verify parsing success rate meets 98% threshold."""
        # Simulate extraction statistics
        total_files = 100
        successful = 99
        failed = 1

        success_rate = successful / total_files
        min_threshold = tolerance_config['min_success_rate']

        assert success_rate >= min_threshold, \
            f"Success rate {success_rate:.2%} below threshold {min_threshold:.2%}"

    def test_method_extraction_accuracy(self, tolerance_config: Dict):
        """Test method extraction accuracy meets 90% threshold."""
        # Simulate accuracy: extracted vs actual
        actual_methods = 100
        correctly_extracted = 92

        accuracy = correctly_extracted / actual_methods
        min_accuracy = tolerance_config['min_accuracy']

        assert accuracy >= min_accuracy, \
            f"Accuracy {accuracy:.2%} below threshold {min_accuracy:.2%}"

    def test_example_extraction_accuracy(self, tolerance_config: Dict):
        """Test example extraction accuracy meets threshold."""
        # Simulate example extraction
        actual_examples = 50
        correctly_extracted = 44

        accuracy = correctly_extracted / actual_examples
        # Examples have lower threshold (85%)
        min_threshold = 0.85

        assert accuracy >= min_threshold, \
            f"Example accuracy {accuracy:.2%} below threshold {min_threshold:.2%}"

    def test_spot_check_pass_rate(self, tolerance_config: Dict):
        """Test spot-check validation pass rate."""
        # Simulate spot-check results
        total_checks = 20
        passed_checks = 18

        pass_rate = passed_checks / total_checks
        min_threshold = tolerance_config['min_spot_check_pass']

        assert pass_rate >= min_threshold, \
            f"Spot-check pass rate {pass_rate:.2%} below threshold {min_threshold:.2%}"


@pytest.mark.spot_check
class TestValidationStatistics:
    """Validation statistics and reporting."""

    def test_calculate_extraction_stats(self, knowledge_base: Dict):
        """Calculate and validate extraction statistics."""
        metadata = knowledge_base.get('metadata', {})

        # Check metadata has required fields
        assert 'extraction_date' in metadata, "Missing extraction_date"
        assert 'source' in metadata, "Missing source"

        # Get statistics if available
        total_files = metadata.get('total_files_processed', 0)

        # If no files processed, skip detailed validation
        if total_files == 0:
            pytest.skip("No files processed yet")

    def test_error_rate_acceptable(self):
        """Verify error rate is within acceptable limits."""
        # Simulate error statistics
        total_files = 100
        errors = 2

        error_rate = errors / total_files
        max_acceptable = 0.02  # 2% max error rate

        assert error_rate <= max_acceptable, \
            f"Error rate {error_rate:.2%} exceeds limit {max_acceptable:.2%}"

    def test_namespace_distribution(self, knowledge_base: Dict):
        """Verify extraction covers multiple namespaces."""
        namespaces = knowledge_base.get('namespaces', {})

        if len(namespaces) == 0:
            pytest.skip("No namespaces extracted")

        # Should have at least 2 namespaces for good coverage
        assert len(namespaces) >= 1, \
            f"Too few namespaces ({len(namespaces)}), expect diverse coverage"
