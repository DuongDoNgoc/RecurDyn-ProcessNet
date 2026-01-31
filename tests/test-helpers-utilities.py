"""
Test helper utilities for tolerance calculations and common operations.
"""
from typing import Dict, Tuple
from bs4 import BeautifulSoup
from pathlib import Path


def calculate_tolerance_range(expected_count: int, tolerance_percent: float) -> Tuple[int, int]:
    """
    Calculate tolerance range for count validation.

    Args:
        expected_count: Expected value
        tolerance_percent: Tolerance as decimal (0.20 for 20%)

    Returns:
        Tuple of (min_acceptable, max_acceptable)
    """
    tolerance = int(expected_count * tolerance_percent)
    return (expected_count - tolerance, expected_count + tolerance)


def is_within_tolerance(actual: int, expected: int, tolerance_percent: float) -> bool:
    """
    Check if actual count is within tolerance of expected.

    Args:
        actual: Actual measured value
        expected: Expected value
        tolerance_percent: Tolerance as decimal (0.20 for 20%)

    Returns:
        True if within tolerance
    """
    min_val, max_val = calculate_tolerance_range(expected, tolerance_percent)
    return min_val <= actual <= max_val


def parse_html_file(file_path: Path) -> BeautifulSoup:
    """
    Parse HTML file with BeautifulSoup.

    Args:
        file_path: Path to HTML file

    Returns:
        BeautifulSoup object

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        return BeautifulSoup(f.read(), 'html.parser')


def count_elements(soup: BeautifulSoup, tag: str, class_name: str = None, filter_text: str = None) -> int:
    """
    Count HTML elements matching criteria.

    Args:
        soup: BeautifulSoup object
        tag: HTML tag name
        class_name: Optional class name filter
        filter_text: Optional text content filter

    Returns:
        Count of matching elements
    """
    if class_name:
        elements = soup.find_all(tag, class_=class_name)
    else:
        elements = soup.find_all(tag)

    if filter_text:
        elements = [el for el in elements if filter_text in el.get_text()]

    return len(elements)
