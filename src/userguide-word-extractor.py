#!/usr/bin/env python3
"""
RecurDyn ProcessNet User Guide Word HTML Extractor

Extracts user guide content from Microsoft Word HTML export files.
Strips MSO markup, extracts heading hierarchy, and preserves content.

Usage:
    python userguide-word-extractor.py [--input PATH] [--output PATH]
"""

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

from bs4 import BeautifulSoup, Tag
import chardet

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class GuideSection:
    """Represents a section in the user guide."""
    title: str
    level: int  # 1-6 based on heading
    content: str  # Cleaned prose text
    images: list = field(default_factory=list)
    source_file: str = ""
    section_id: str = ""  # Generated from title


@dataclass
class UserGuide:
    """Represents a complete user guide document."""
    title: str
    source_file: str
    sections: list = field(default_factory=list)
    word_count: int = 0
    image_count: int = 0


class MSOHTMLCleaner:
    """Cleans Microsoft Office HTML markup from Word exports."""

    @staticmethod
    def strip_mso_markup(html: str) -> str:
        """Remove all Microsoft Office markup from HTML.

        Minimal cleaning to preserve structure while removing MSO artifacts.
        """
        # Remove conditional comments - simpler approach
        html = re.sub(r'<!\[if [^\]]*\]>.*?<!\[endif\]>', '', html, flags=re.DOTALL)

        # Remove MSO namespace declarations from html tag
        html = re.sub(r'xmlns:[vowmx]+="[^"]*"', '', html)

        # Remove o:p and similar self-closing tags
        html = re.sub(r'<o:p>\s*</o:p>', '', html)
        html = re.sub(r'<o:p/>', '', html)
        html = re.sub(r'</?o:p>', '', html)

        # Remove MSO elements
        html = re.sub(r'</?[owxv]:[^>]*>', '', html)

        # Clean up MSO class attributes but keep the element
        html = re.sub(r'\s*class=["\'][^"\']*Mso[^"\']*["\']', '', html)
        html = re.sub(r'\s*class=["\'][^"\']*Toc[^"\']*["\']', '', html)

        # Remove style attributes containing mso-
        html = re.sub(r'\s+style="[^"]*mso-[^"]*"', '', html)
        html = re.sub(r'\s+style="[^"]*mso-[^"]*"', '', html)

        # Clean up extra whitespace
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)

        return html.strip()


class UserGuideWordExtractor:
    """Extractor for Word HTML user guide files."""

    # Heading tags to track
    HEADING_TAGS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    # Classes that indicate TOC entries (to skip)
    TOC_CLASSES = ['MsoToc', 'MsoTocHeading']

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.cleaner = MSOHTMLCleaner()
        self.guides = []
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'total_sections': 0,
            'total_words': 0,
            'total_images': 0
        }
        self.errors = []

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding with Korean charset handling."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(50000)
                result = chardet.detect(raw_data)
                encoding = result.get('encoding', 'utf-8')

                # Handle KS_C_5601-1987 Korean encoding
                if encoding and 'ks' in encoding.lower():
                    return 'euc-kr'  # Korean encoding

                return encoding or 'utf-8'
        except Exception as e:
            logger.warning(f"Encoding detection failed for {file_path}: {e}")
            return 'utf-8'

    def read_html_file(self, file_path: Path) -> Optional[str]:
        """Read HTML file with proper encoding handling."""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            return content
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            self.errors.append({'file': str(file_path), 'error': str(e)})
            return None

    def generate_section_id(self, title: str) -> str:
        """Generate URL-safe section ID from title."""
        # Remove special chars, replace spaces with hyphens
        clean = re.sub(r'[^\w\s-]', '', title.lower())
        clean = re.sub(r'[-\s]+', '-', clean)
        return clean.strip('-')

    def extract_images(self, soup: BeautifulSoup, source_file: str) -> list:
        """Extract image references from HTML."""
        images = []

        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src:
                # Handle relative paths in .files/ directories
                if 'image' in src.lower() or '.files' in src:
                    images.append(src)

        return images

    def is_toc_heading(self, element: Tag) -> bool:
        """Check if heading is part of table of contents."""
        classes = element.get('class', [])
        return any(cls for cls in classes if any(toc in cls for toc in self.TOC_CLASSES))

    def extract_sections_from_soup(self, soup: BeautifulSoup, source_file: str) -> list:
        """Extract heading hierarchy and content from HTML."""
        sections = []
        body = soup.find('body')
        if not body:
            return sections

        # Find all headings in document order
        headings = body.find_all(self.HEADING_TAGS)
        logger.info(f"Found {len(headings)} headings in {source_file}")

        for i, heading in enumerate(headings):
            # Skip TOC headings
            if self.is_toc_heading(heading):
                continue

            # Get heading level and text
            level = int(heading.name[1])  # h3 -> 3
            title = heading.get_text(strip=True)

            if not title or len(title) < 2:
                continue

            # Extract content after heading until next heading of same or higher level
            content_parts = []
            images = []

            # Get all siblings until next heading
            current = heading.next_sibling
            while current:
                if isinstance(current, Tag):
                    # Stop if we hit another heading
                    if current.name in self.HEADING_TAGS:
                        current_level = int(current.name[1])
                        # Stop if same or higher level (lower number)
                        if current_level <= level:
                            break

                    # Collect text from content elements
                    if current.name in ['p', 'div', 'li', 'span', 'td', 'th']:
                        text = current.get_text(separator=' ', strip=True)
                        # Filter out empty content and common MSO artifacts
                        if text and len(text) > 3 and text not in ['\xa0', '&nbsp;', ' ']:
                            content_parts.append(text)

                    # Collect images
                    if current.name == 'img':
                        src = current.get('src', '')
                        if src and ('image' in src.lower() or '.files' in src):
                            # Clean up URL encoding
                            src = src.replace('%20', ' ')
                            images.append(src)

                    # Find nested images
                    for img in current.find_all('img'):
                        src = img.get('src', '')
                        if src and ('image' in src.lower() or '.files' in src):
                            src = src.replace('%20', ' ')
                            if src not in images:
                                images.append(src)

                current = current.next_sibling

            # Combine content with proper spacing
            content = ' '.join(content_parts)

            # Only create section if we have content or it's a meaningful heading
            if content or len(title) > 10:
                section = GuideSection(
                    title=title,
                    level=level,
                    content=content[:3000],  # Limit content length
                    images=images,
                    source_file=source_file,
                    section_id=self.generate_section_id(title)
                )
                sections.append(section)

        return sections

    def count_words(self, text: str) -> int:
        """Count words in text."""
        return len(text.split())

    def parse_guide_file(self, file_path: Path) -> Optional[UserGuide]:
        """Parse a single Word HTML guide file."""
        logger.info(f"Parsing {file_path.name}")

        # Read file
        html_content = self.read_html_file(file_path)
        if not html_content:
            return None

        # Extract images from original HTML before cleaning
        raw_images = self._extract_images_from_html(html_content, file_path.name)

        # Strip MSO markup for content parsing
        try:
            cleaned_html = self.cleaner.strip_mso_markup(html_content)
        except Exception as e:
            logger.error(f"Failed to clean HTML: {e}")
            cleaned_html = html_content  # Fallback to original

        # Parse with BeautifulSoup
        try:
            soup = BeautifulSoup(cleaned_html, 'lxml')
        except Exception as e:
            logger.error(f"BeautifulSoup parsing failed: {e}")
            return None

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else file_path.stem

        # Extract sections
        sections = self.extract_sections_from_soup(soup, file_path.name)

        # Add raw images to sections that don't have images
        for section in sections:
            if not section.images:
                # Try to match images from the raw extraction
                section.images = [img for img in raw_images if img]

        # Collect all images
        all_images = []
        total_words = 0

        for section in sections:
            all_images.extend(section.images)
            total_words += self.count_words(section.content)

        # Create guide
        guide = UserGuide(
            title=title,
            source_file=file_path.name,
            sections=sections,
            word_count=total_words,
            image_count=len(set(all_images))  # Unique images
        )

        return guide

    def _extract_images_from_html(self, html: str, source_file: str) -> list:
        """Extract image references from raw HTML before MSO cleaning."""
        images = []

        # Match img src attributes
        img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
        for match in re.finditer(img_pattern, html, re.IGNORECASE):
            src = match.group(1)
            if 'image' in src.lower() or '.files' in src:
                src = src.replace('%20', ' ')
                images.append(src)

        # Match v:imagedata src attributes
        vml_pattern = r'<v:imagedata[^>]+src=["\']([^"\']+)["\']'
        for match in re.finditer(vml_pattern, html, re.IGNORECASE):
            src = match.group(1)
            src = src.replace('%20', ' ')
            images.append(src)

        return list(set(images))  # Unique images

    def extract_all_guides(self):
        """Extract all guide files from input directory."""
        # Find all HTM files
        htm_files = sorted(self.input_path.glob('*.htm'))
        logger.info(f"Found {len(htm_files)} guide files")

        for idx, file_path in enumerate(htm_files, 1):
            logger.info(f"[{idx}/{len(htm_files)}] Processing {file_path.name}")

            try:
                guide = self.parse_guide_file(file_path)
                if guide:
                    self.guides.append(asdict(guide))
                    self.stats['files_processed'] += 1
                    self.stats['total_sections'] += len(guide.sections)
                    self.stats['total_words'] += guide.word_count
                    self.stats['total_images'] += guide.image_count
                else:
                    self.stats['files_failed'] += 1

            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                self.errors.append({'file': str(file_path), 'error': str(e)})
                self.stats['files_failed'] += 1

    def build_output(self) -> dict:
        """Build output dictionary with statistics."""
        return {
            'word_guides': self.guides,
            'statistics': {
                'total_guides': self.stats['files_processed'],
                'total_sections': self.stats['total_sections'],
                'total_words': self.stats['total_words'],
                'total_images': self.stats['total_images']
            },
            'metadata': {
                'extraction_date': datetime.now().isoformat(),
                'source_directory': str(self.input_path),
                'files_processed': self.stats['files_processed'],
                'files_failed': self.stats['files_failed']
            }
        }

    def save_output(self):
        """Save extracted guides to JSON file."""
        # Ensure output directory exists
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        output = self.build_output()

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)

        logger.info(f"Output saved to {self.output_path}")
        logger.info(f"Total guides: {output['statistics']['total_guides']}")
        logger.info(f"Total sections: {output['statistics']['total_sections']}")
        logger.info(f"Total words: {output['statistics']['total_words']}")
        logger.info(f"Total images: {output['statistics']['total_images']}")

        # Save errors if any
        if self.errors:
            error_path = self.output_path.parent / 'userguide-extraction-errors.json'
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, indent=2, ensure_ascii=False)
            logger.warning(f"Errors saved to {error_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract ProcessNet User Guide content from Word HTML files'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default=Path('output/extracted_chm/Content/UserGuideFiles'),
        help='Input directory containing Word HTML guide files'
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

    logger.info("Starting user guide extraction...")
    logger.info(f"Input directory: {args.input}")
    logger.info(f"Output file: {args.output}")

    extractor = UserGuideWordExtractor(args.input, args.output)
    extractor.extract_all_guides()
    extractor.save_output()

    logger.info("Extraction complete!")


if __name__ == '__main__':
    main()
