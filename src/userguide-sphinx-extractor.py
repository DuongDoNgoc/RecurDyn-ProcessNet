#!/usr/bin/env python3
"""
Sphinx User Guide Extractor for RecurDyn ProcessNet

Extracts user guide content from Sphinx ReadTheDocs HTML files and builds
a structured knowledge base with section hierarchy, navigation, and content.

Usage:
    python userguide-sphinx-extractor.py [--input PATH] [--output PATH]
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

from bs4 import BeautifulSoup
import chardet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class SphinxSection:
    """Represents a section in Sphinx documentation."""
    number: str  # "43.2.10"
    title: str  # "ProcessNet Gadget"
    full_title: str  # "43.2.10. ProcessNet Gadget"
    level: int  # Depth in hierarchy (1, 2, 3, 4)
    content: str  # Main prose content
    parent_number: str = ""  # "43.2" for "43.2.10"
    children: List[str] = field(default_factory=list)  # Child section numbers
    prev_href: str = ""
    next_href: str = ""
    source_file: str = ""
    section_id: str = ""  # HTML id attribute


@dataclass
class ToctreeEntry:
    """Represents an entry in the toctree navigation."""
    number: str  # Section number
    title: str  # Section title
    href: str  # Link to HTML file
    level: int  # Hierarchy level


class SphinxUserGuideExtractor:
    """Extractor for Sphinx ReadTheDocs user guide documentation."""

    # Patterns for section number extraction
    SECTION_NUMBER_PATTERN = re.compile(r'^([\d.]+)\.\s*(.+)$')
    SECTION_NUMBER_SPAN = re.compile(r'<span class="section-number">([^<]+)</span>')

    # ProcessNet section prefix (sections starting with 43 are ProcessNet)
    PROCESSNET_SECTION_PREFIX = "43"

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.output_data = {
            'sphinx_guides': {
                'toctree': [],
                'sections': {}
            },
            'statistics': {
                'total_sections': 0,
                'max_depth': 0,
                'total_words': 0,
                'files_processed': 0
            },
            'metadata': {
                'source': 'RecurDyn ProcessNet User Guide (Sphinx)',
                'extraction_date': datetime.now().isoformat(),
                'input_path': str(self.input_path)
            }
        }
        self.sections_by_number: Dict[str, SphinxSection] = {}
        self.toctree_entries: List[ToctreeEntry] = []
        self.errors = []
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'sections_extracted': 0
        }

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8') or 'utf-8'
        except Exception as e:
            logger.warning(f"Encoding detection failed for {file_path}: {e}, using UTF-8")
            return 'utf-8'

    def read_html_file(self, file_path: Path) -> Optional[BeautifulSoup]:
        """Read and parse HTML file with encoding detection."""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            return BeautifulSoup(content, 'lxml')
        except Exception as e:
            logger.error(f"Failed to read {file_path.name}: {e}")
            self.errors.append({'file': str(file_path), 'error': str(e)})
            return None

    def extract_section_number_from_heading(self, heading_text: str) -> tuple:
        """
        Extract section number and title from heading text.

        Args:
            heading_text: Raw heading text like "43.2.10. ProcessNet Gadget"

        Returns:
            Tuple of (section_number, title) or (None, heading_text) if no number
        """
        # Try to match pattern "NUMBER. TITLE"
        match = self.SECTION_NUMBER_PATTERN.match(heading_text.strip())
        if match:
            number = match.group(1).rstrip('.')
            title = match.group(2).strip()
            return (number, title)

        # Check for span element format
        span_match = self.SECTION_NUMBER_SPAN.search(heading_text)
        if span_match:
            number = span_match.group(1).rstrip('.')
            # Remove span and clean up title
            title = self.SECTION_NUMBER_SPAN.sub('', heading_text).strip()
            # Remove leading dot if present
            title = title.lstrip('.').strip()
            return (number, title)

        return (None, heading_text.strip())

    def parse_section_number_level(self, section_number: str) -> int:
        """
        Calculate hierarchy level from section number.

        Args:
            section_number: Section number like "43.2.10"

        Returns:
            Level in hierarchy (1, 2, 3, 4, etc.)
        """
        if not section_number:
            return 0
        # Count dots to determine level
        # "43" -> level 1
        # "43.2" -> level 2
        # "43.2.10" -> level 3
        return section_number.count('.') + 1

    def get_parent_number(self, section_number: str) -> str:
        """
        Get parent section number from child section number.

        Args:
            section_number: Section number like "43.2.10"

        Returns:
            Parent number like "43.2" or "" if no parent
        """
        if not section_number:
            return ""
        parts = section_number.split('.')
        if len(parts) > 1:
            return '.'.join(parts[:-1])
        return ""

    def extract_prev_next_links(self, soup: BeautifulSoup) -> tuple:
        """
        Extract prev/next navigation links from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Tuple of (prev_href, next_href)
        """
        prev_href = ""
        next_href = ""

        # Find link tags
        for link in soup.find_all('link', rel='prev'):
            href = link.get('href', '')
            if href:
                prev_href = href
                break

        for link in soup.find_all('link', rel='next'):
            href = link.get('href', '')
            if href:
                next_href = href
                break

        return (prev_href, next_href)

    def extract_toctree_from_file(self, soup: BeautifulSoup, source_file: str) -> List[ToctreeEntry]:
        """
        Extract toctree navigation entries from sidebar.

        Only extracts ProcessNet sections (those starting with 43).

        Args:
            soup: BeautifulSoup object
            source_file: Source file name for reference

        Returns:
            List of ToctreeEntry objects
        """
        entries = []

        # Find toctree in sidebar
        for li in soup.find_all('li', class_=re.compile(r'toctree-l\d')):
            # Get class to determine level
            classes = li.get('class', [])
            level = 1
            for cls in classes:
                if cls.startswith('toctree-l'):
                    try:
                        level = int(cls.replace('toctree-l', ''))
                    except ValueError:
                        pass

            # Get link
            link = li.find('a', class_='reference internal')
            if link:
                href = link.get('href', '')
                title = link.get_text(strip=True)

                # Extract section number from title
                number, title_text = self.extract_section_number_from_heading(title)

                # Only include ProcessNet sections (starting with 43)
                if number and number.startswith(self.PROCESSNET_SECTION_PREFIX):
                    entries.append(ToctreeEntry(
                        number=number,
                        title=title_text,
                        href=href,
                        level=level
                    ))

        return entries

    def extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract main prose content from HTML.

        Args:
            soup: BeautifulSoup object

        Returns:
            Cleaned text content
        """
        # Find main content area
        main_content = soup.find('main') or soup.find('div', role='main') or soup.find('div', class_='document')

        if not main_content:
            return ""

        # Remove navigation, code blocks, and other non-prose elements
        for element in main_content.find_all(['nav', 'script', 'style', 'aside']):
            element.decompose()

        # Get text
        text = main_content.get_text(separator='\n', strip=True)

        # Clean up: remove excessive whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()

        return text

    def extract_sections_from_file(self, soup: BeautifulSoup, source_file: str) -> List[SphinxSection]:
        """
        Extract all sections from HTML file.

        Args:
            soup: BeautifulSoup object
            source_file: Source file name for reference

        Returns:
            List of SphinxSection objects
        """
        sections = []

        # Get prev/next links
        prev_href, next_href = self.extract_prev_next_links(soup)

        # Find all headings
        for heading in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            heading_text = heading.get_text(strip=True)

            # Extract section number and title
            section_number, title = self.extract_section_number_from_heading(heading_text)

            if not section_number:
                # Skip headings without section numbers
                continue

            # Calculate level
            level = self.parse_section_number_level(section_number)

            # Get parent number
            parent_number = self.get_parent_number(section_number)

            # Get section ID
            section_id = heading.get('id', '')

            # Extract content after this heading (until next heading)
            content = ""
            next_element = heading.find_next_sibling()
            while next_element and next_element.name not in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                # Get text content
                element_text = next_element.get_text(separator=' ', strip=True)
                if element_text:
                    content += element_text + "\n\n"
                next_element = next_element.find_next_sibling()

            # Clean content
            content = re.sub(r'\s+', ' ', content).strip()

            # Limit content length
            if len(content) > 10000:
                content = content[:10000] + "..."

            # Create section
            section = SphinxSection(
                number=section_number,
                title=title,
                full_title=heading_text,
                level=level,
                content=content,
                parent_number=parent_number,
                prev_href=prev_href,
                next_href=next_href,
                source_file=source_file,
                section_id=section_id
            )

            sections.append(section)

        return sections

    def build_parent_child_relationships(self):
        """Build parent-child relationships between sections."""
        for section_number, section in self.sections_by_number.items():
            if section.parent_number and section.parent_number in self.sections_by_number:
                parent = self.sections_by_number[section.parent_number]
                if section_number not in parent.children:
                    parent.children.append(section_number)

    def process_html_file(self, file_path: Path):
        """Process a single HTML file and extract content."""
        soup = self.read_html_file(file_path)
        if not soup:
            self.stats['files_failed'] += 1
            return

        rel_path = str(file_path.relative_to(self.input_path))

        try:
            # Extract sections
            sections = self.extract_sections_from_file(soup, rel_path)

            # Store sections by number
            for section in sections:
                if section.number not in self.sections_by_number:
                    self.sections_by_number[section.number] = section
                    self.stats['sections_extracted'] += 1

            # Extract toctree (only from index files to avoid duplication)
            if 'index' in file_path.name:
                toctree = self.extract_toctree_from_file(soup, rel_path)
                # Store toctree entries for later processing
                self.toctree_entries.extend(toctree)

            self.stats['files_processed'] += 1

        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            self.errors.append({'file': str(file_path), 'error': str(e)})
            self.stats['files_failed'] += 1

    def calculate_statistics(self):
        """Calculate extraction statistics."""
        total_words = 0
        max_depth = 0

        for section in self.sections_by_number.values():
            # Count words in content
            words = len(section.content.split())
            total_words += words

            # Track max depth
            if section.level > max_depth:
                max_depth = section.level

        self.output_data['statistics']['total_sections'] = len(self.sections_by_number)
        self.output_data['statistics']['max_depth'] = max_depth
        self.output_data['statistics']['total_words'] = total_words
        self.output_data['statistics']['files_processed'] = self.stats['files_processed']

    def build_toctree_output(self):
        """Build deduplicated and sorted toctree output."""
        seen = set()
        unique_entries = []

        for entry in self.toctree_entries:
            # Create unique key from number and href
            key = (entry.number, entry.href)
            if key not in seen:
                seen.add(key)
                unique_entries.append(entry)

        # Sort by number
        unique_entries.sort(key=lambda e: e.number)

        # Convert to dict
        self.output_data['sphinx_guides']['toctree'] = [asdict(e) for e in unique_entries]

    def build_output(self):
        """Build final output structure."""
        # Build toctree
        self.build_toctree_output()

        # Convert sections to dict
        for number, section in self.sections_by_number.items():
            self.output_data['sphinx_guides']['sections'][number] = asdict(section)

        # Calculate statistics
        self.calculate_statistics()

    def extract_user_guide(self):
        """Extract user guide from all HTML files in input directory."""
        logger.info(f"Starting extraction from {self.input_path}")

        # Find all HTML files
        html_files = sorted(self.input_path.glob('*.html'))

        if not html_files:
            logger.error(f"No HTML files found in {self.input_path}")
            return

        logger.info(f"Found {len(html_files)} HTML files")

        # Process each file
        for idx, file_path in enumerate(html_files, 1):
            progress = (idx / len(html_files)) * 100
            logger.info(f"[{progress:5.1f}%] ({idx}/{len(html_files)}) {file_path.name}")

            self.process_html_file(file_path)

        # Build relationships
        logger.info("Building parent-child relationships...")
        self.build_parent_child_relationships()

        # Build output
        logger.info("Building output structure...")
        self.build_output()

        # Log summary
        logger.info("=" * 60)
        logger.info("Extraction Summary:")
        logger.info(f"  Files processed: {self.stats['files_processed']}")
        logger.info(f"  Files failed: {self.stats['files_failed']}")
        logger.info(f"  Sections extracted: {self.stats['sections_extracted']}")
        logger.info(f"  Toctree entries: {len(self.output_data['sphinx_guides']['toctree'])}")
        logger.info(f"  Max depth: {self.output_data['statistics']['max_depth']}")
        logger.info(f"  Total words: {self.output_data['statistics']['total_words']}")

    def save_output(self):
        """Save extracted data to JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.output_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Output saved to {self.output_path}")

        # Save errors if any
        if self.errors:
            error_path = self.output_path.parent / 'userguide-extraction-errors.json'
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, indent=2, ensure_ascii=False)
            logger.warning(f"Errors saved to {error_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Extract Sphinx user guide documentation from RecurDyn ProcessNet HTML files'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default=Path('knowledge/RecurDynHelp/ProcessNet'),
        help='Input directory containing Sphinx HTML files'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('output/processnet-userguide.json'),
        help='Output JSON file path'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if not args.input.exists():
        logger.error(f"Input path does not exist: {args.input}")
        sys.exit(1)

    extractor = SphinxUserGuideExtractor(args.input, args.output)
    extractor.extract_user_guide()
    extractor.save_output()

    logger.info("Extraction complete!")


if __name__ == '__main__':
    main()
