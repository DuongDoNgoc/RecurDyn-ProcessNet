#!/usr/bin/env python3
"""
CHM C#/VB API Documentation Extractor

Extracts API documentation from RecurDyn CHM HTML files and builds a structured
knowledge base with dual-language syntax (C# and VB.NET).

Usage:
    python chm-api-extractor.py [--input PATH] [--output PATH]
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
class ChmEnumMember:
    """Represents an enum member."""
    name: str
    value: str
    description: str


@dataclass
class ChmApiMember:
    """Represents a C#/VB API member (class, interface, enum, method, property, event)."""
    name: str
    entity_type: str  # class, interface, enum, method, property, event
    namespace: str
    full_name: str    # Microsoft.Help.F1 value
    help_id: str      # Microsoft.Help.Id value (T:, M:, P:, E:, etc.)
    description: str
    syntax_csharp: str
    syntax_vb: str
    assembly: str
    assembly_version: str
    members: List[Dict[str, Any]] = field(default_factory=list)  # For enums/classes
    parameters: List[Dict[str, Any]] = field(default_factory=list)  # For methods
    returns: str = ""
    source_file: str = ""


class ChmApiExtractor:
    """Extractor for CHM C#/VB API documentation."""

    # Entity type prefixes in Microsoft.Help.Id
    ENTITY_PREFIXES = {
        'T:': 'class',  # Type (class, interface, enum)
        'M:': 'method',  # Method
        'P:': 'property',  # Property
        'E:': 'event',  # Event
        'F:': 'field',  # Field (enum members)
    }

    # Patterns to exclude
    EXCLUDE_PATTERNS = [
        '_static', '_images', 'assets', 'css', 'js', '_sources',
        '.git', '__pycache__', 'mathjax'
    ]

    def __init__(self, input_path: Path, output_path: Path):
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.knowledge_base = {
            'metadata': {
                'source': 'RecurDyn CHM C#/VB API',
                'version': 'v7-extract',
                'extraction_date': datetime.now().isoformat(),
                'total_files_processed': 0,
                'extraction_duration_seconds': 0
            },
            'namespaces': {},
            'entity_index': {},
            'statistics': {
                'namespaces': 0,
                'classes': 0,
                'interfaces': 0,
                'enums': 0,
                'methods': 0,
                'properties': 0,
                'events': 0
            }
        }
        self.errors = []
        self.stats = {
            'files_processed': 0,
            'files_failed': 0,
            'members_extracted': 0,
            'namespaces': 0
        }

    def discover_files(self) -> List[Path]:
        """Discover all HTM files recursively."""
        all_files = []
        extensions = ['.html', '.htm']

        for path in self.input_path.rglob('*'):
            if path.suffix.lower() in extensions:
                skip = False
                for pattern in self.EXCLUDE_PATTERNS:
                    if pattern in str(path):
                        skip = True
                        break
                if not skip:
                    all_files.append(path)

        return sorted(all_files)

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(10000)
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8') or 'utf-8'
        except Exception:
            return 'utf-8'

    def read_html_file(self, file_path: Path) -> Optional[BeautifulSoup]:
        """Read and parse HTML file with encoding detection."""
        try:
            encoding = self.detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                content = f.read()
            return BeautifulSoup(content, 'lxml')
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            self.errors.append({'file': str(file_path), 'error': str(e)})
            return None

    def extract_meta_content(self, soup: BeautifulSoup, meta_name: str) -> str:
        """Extract content from meta tag by name attribute."""
        meta_tag = soup.find('meta', attrs={'name': meta_name})
        if meta_tag:
            return meta_tag.get('content', '').strip()
        return ""

    def extract_all_meta_f1(self, soup: BeautifulSoup) -> List[str]:
        """Extract all Microsoft.Help.F1 meta tag contents."""
        f1_values = []
        for meta in soup.find_all('meta', attrs={'name': re.compile(r'^Microsoft\.Help\.F1$', re.I)}):
            content = meta.get('content', '').strip()
            if content:
                f1_values.append(content)
        return f1_values

    def determine_entity_type(self, help_id: str) -> str:
        """Determine entity type from Microsoft.Help.Id prefix."""
        for prefix, entity_type in self.ENTITY_PREFIXES.items():
            if help_id.startswith(prefix):
                return entity_type
        # Default to class if unknown prefix
        return 'class'

    def extract_syntax_from_tabs(self, soup: BeautifulSoup, base_id: str) -> tuple:
        """
        Extract C# and VB syntax from tabbed code blocks.

        Args:
            soup: BeautifulSoup object
            base_id: Base ID for code tabs (e.g., 'ID0EBCA')

        Returns:
            Tuple of (csharp_syntax, vb_syntax)
        """
        syntax_csharp = ""
        syntax_vb = ""

        # Try Div1 (C#) and Div2 (VB) pattern
        div1 = soup.find('div', id=f'{base_id}_code_Div1')
        div2 = soup.find('div', id=f'{base_id}_code_Div2')

        if div1:
            pre = div1.find('pre')
            if pre:
                syntax_csharp = pre.get_text(strip=True)

        if div2:
            pre = div2.find('pre')
            if pre:
                syntax_vb = pre.get_text(strip=True)

        # Fallback: find any code divs
        if not syntax_csharp or not syntax_vb:
            for code_div in soup.find_all('div', class_='codeSnippetContainerCode'):
                pre = code_div.find('pre')
                if pre:
                    code = pre.get_text(strip=True)
                    # Heuristic: C# has 'public class', VB has 'Public Class'
                    if 'public class' in code.lower() or 'public enum' in code.lower() or \
                       'public interface' in code.lower():
                        syntax_csharp = code
                    elif 'public class' in code.lower() or 'public enum' in code.lower():
                        syntax_vb = code

        return syntax_csharp, syntax_vb

    def extract_enum_members(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """
        Extract enum members from enumMemberList table.

        Returns:
            List of enum member dictionaries
        """
        members = []
        enum_table = soup.find('table', id='enumMemberList')

        if not enum_table:
            return members

        tbody = enum_table.find('tbody')
        if not tbody:
            tbody = enum_table  # Some tables don't have tbody

        for row in tbody.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 3:
                # Extract member name from second cell
                name_cell = cells[1]
                span = name_cell.find('span', class_='selflink')
                if span:
                    member_name = span.get_text(strip=True)
                else:
                    member_name = name_cell.get_text(strip=True)

                # Extract value from third cell
                value_cell = cells[2]
                value = value_cell.get_text(strip=True)

                # Extract description from fourth cell (if present)
                description = ""
                if len(cells) >= 4:
                    desc_cell = cells[3]
                    description = desc_cell.get_text(strip=True)

                members.append({
                    'name': member_name,
                    'value': value,
                    'description': description[:500] if description else ""
                })

        return members

    def extract_assembly_info(self, soup: BeautifulSoup) -> tuple:
        """
        Extract assembly name and version from page content.

        Returns:
            Tuple of (assembly_name, assembly_version)
        """
        # Look for assembly in page text
        # Pattern: "Assembly: X (in X.dll) Version: Y"
        page_text = soup.get_text()

        # Extract assembly name
        assembly_match = re.search(r'Assembly:\s*([^\s(]+)', page_text)
        if assembly_match:
            assembly = assembly_match.group(1)
        else:
            assembly = ""

        # Extract version
        version_match = re.search(r'Version:\s*([\d.]+)', page_text)
        if version_match:
            version = version_match.group(1)
        else:
            version = ""

        return assembly, version

    def parse_html_file(self, file_path: Path) -> Optional[ChmApiMember]:
        """
        Parse a single HTML file and extract API member information.

        Returns:
            ChmApiMember object or None if extraction fails
        """
        soup = self.read_html_file(file_path)
        if not soup:
            return None

        # Extract metadata from meta tags
        container = self.extract_meta_content(soup, 'container')
        help_id = self.extract_meta_content(soup, 'Microsoft.Help.Id')
        description = self.extract_meta_content(soup, 'Description')
        f1_values = self.extract_all_meta_f1(soup)

        # Extract title as fallback for name
        title_tag = soup.find('title')
        title = title_tag.get_text(strip=True) if title_tag else ""

        # Skip files without essential metadata
        if not help_id:
            return None

        # Determine entity type from help_id prefix
        entity_type = self.determine_entity_type(help_id)

        # Extract name from help_id (after prefix and before parameters)
        # T:FunctionBay.Post.ProcessNet.ContourLegendPosition
        # P:FunctionBay.RecurDyn.ProcessNet.IForceTranslational.RefMarker
        # M:FunctionBay.Post.ProcessNet.IModelDatabase.OpenPropertyGrid(FunctionBay.Post.ProcessNet.IDatabaseItem,System.Boolean)
        name_match = re.search(r'^[A-Z]:(.+)$', help_id)
        if name_match:
            full_name_with_params = name_match.group(1)
            # Remove parameters for methods
            paren_match = re.search(r'^(.+?)\([^)]*\)$', full_name_with_params)
            if paren_match:
                full_name = paren_match.group(1)
            else:
                full_name = full_name_with_params

            # Extract simple name (last part after dot)
            name_parts = full_name.split('.')
            name = name_parts[-1] if name_parts else full_name
        else:
            # Fallback to title extraction: "IModelDatabase.OpenPropertyGrid Method (IDatabaseItem, Boolean)"
            if title:
                # Extract method name from title
                title_match = re.search(r'^(\w+(?:\.\w+)*)\.(\w+)\s+(?:Method|Property|Event)\s', title)
                if title_match:
                    name = title_match.group(2)
                    full_name = f"{title_match.group(1)}.{name}"
                else:
                    # Fallback: extract last word before " Method" etc.
                    name_match = re.search(r'(\w+)\s+(?:Method|Property|Event)\s', title)
                    if name_match:
                        name = name_match.group(1)
                    else:
                        name = title.split()[0] if title else file_path.stem
                    full_name = f1_values[0] if f1_values else name
            else:
                full_name = f1_values[0] if f1_values else ""
                name = full_name.split('.')[-1] if full_name else file_path.stem

        # Extract namespace from container or full_name
        if container:
            namespace = container
        else:
            # Extract namespace from full_name (everything except last part)
            name_parts = full_name.split('.')
            namespace = '.'.join(name_parts[:-1]) if len(name_parts) > 1 else 'Global'

        # Extract dual-language syntax
        # Find the first code snippet container
        code_container = soup.find('div', class_='codeSnippetContainer')
        if code_container:
            # Extract base ID from tab elements
            tab1 = code_container.find('div', class_='codeSnippetContainerTab')
            if tab1:
                # Extract ID from href or onclick
                tab_id = None
                for attr in ['href', 'onclick']:
                    attr_val = tab1.get(attr, '')
                    id_match = re.search(r"ChangeTab\(['\"](\w+)['\"]", attr_val)
                    if id_match:
                        tab_id = id_match.group(1)
                        break

                if tab_id:
                    syntax_csharp, syntax_vb = self.extract_syntax_from_tabs(soup, tab_id)
                else:
                    # Fallback: try to find any code blocks
                    syntax_csharp, syntax_vb = self.extract_syntax_from_tabs(soup, 'ID0EBCA')
            else:
                syntax_csharp, syntax_vb = self.extract_syntax_from_tabs(soup, 'ID0EBCA')
        else:
            syntax_csharp, syntax_vb = "", ""

        # Extract assembly info
        assembly, assembly_version = self.extract_assembly_info(soup)

        # Create member object
        member = ChmApiMember(
            name=name,
            entity_type=entity_type,
            namespace=namespace,
            full_name=full_name,
            help_id=help_id,
            description=description[:1000] if description else "",
            syntax_csharp=syntax_csharp[:2000] if syntax_csharp else "",
            syntax_vb=syntax_vb[:2000] if syntax_vb else "",
            assembly=assembly,
            assembly_version=assembly_version,
            source_file=str(file_path.relative_to(self.input_path))
        )

        # Extract enum members if this is an enum
        if entity_type == 'class' and 'enum' in syntax_csharp.lower():
            enum_members = self.extract_enum_members(soup)
            if enum_members:
                member.members = enum_members
                member.entity_type = 'enum'
                # Update statistics
                self.knowledge_base['statistics']['enums'] += 1

        # Extract class/interface members from property/method tables
        if entity_type in ['class', 'interface']:
            # Look for property and method tables
            property_table = soup.find('table', id='propertyList')
            method_table = soup.find('table', id='methodList')

            if property_table:
                for row in property_table.find_all('tr')[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        link = cells[1].find('a')
                        if link:
                            prop_name = link.get_text(strip=True)
                            member.members.append({
                                'name': prop_name,
                                'type': 'property',
                                'description': cells[2].get_text(strip=True)[:500] if len(cells) >= 3 else ""
                            })

            if method_table:
                for row in method_table.find_all('tr')[1:]:  # Skip header
                    cells = row.find_all('td')
                    if len(cells) >= 2:
                        link = cells[1].find('a')
                        if link:
                            method_name = link.get_text(strip=True)
                            member.members.append({
                                'name': method_name,
                                'type': 'method',
                                'description': cells[2].get_text(strip=True)[:500] if len(cells) >= 3 else ""
                            })

        # Update statistics
        if entity_type == 'class':
            self.knowledge_base['statistics']['classes'] += 1
        elif entity_type == 'interface':
            self.knowledge_base['statistics']['interfaces'] += 1
        elif entity_type == 'method':
            self.knowledge_base['statistics']['methods'] += 1
        elif entity_type == 'property':
            self.knowledge_base['statistics']['properties'] += 1
        elif entity_type == 'event':
            self.knowledge_base['statistics']['events'] += 1

        return member

    def build_knowledge_base(self):
        """Build the complete knowledge base from all files."""
        start_time = datetime.now()

        logger.info(f"Discovering files in {self.input_path}...")
        files = self.discover_files()
        logger.info(f"Found {len(files)} HTM files")

        for idx, file_path in enumerate(files, 1):
            progress = (idx / len(files)) * 100
            if idx % 1000 == 0 or idx == len(files):
                logger.info(f"[{progress:5.1f}%] ({idx}/{len(files)}) Processing files...")

            try:
                member = self.parse_html_file(file_path)
                if member:
                    # Add to namespace
                    namespace = member.namespace
                    if namespace not in self.knowledge_base['namespaces']:
                        self.knowledge_base['namespaces'][namespace] = {
                            'description': f"{namespace} namespace",
                            'members': []
                        }
                        self.stats['namespaces'] += 1
                        self.knowledge_base['statistics']['namespaces'] += 1

                    # Convert member to dict and add to namespace
                    member_dict = asdict(member)
                    self.knowledge_base['namespaces'][namespace]['members'].append(member_dict)

                    # Add to entity index
                    name_lower = member.name.lower()
                    if name_lower not in self.knowledge_base['entity_index']:
                        self.knowledge_base['entity_index'][name_lower] = []
                    if namespace not in self.knowledge_base['entity_index'][name_lower]:
                        self.knowledge_base['entity_index'][name_lower].append(namespace)

                    self.stats['members_extracted'] += 1

                self.stats['files_processed'] += 1

            except Exception as e:
                logger.error(f"Failed to process {file_path}: {e}")
                self.errors.append({'file': str(file_path), 'error': str(e)})
                self.stats['files_failed'] += 1

        # Update metadata
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        self.knowledge_base['metadata']['total_files_processed'] = self.stats['files_processed']
        self.knowledge_base['metadata']['extraction_duration_seconds'] = duration

        logger.info("=" * 60)
        logger.info("Extraction Summary:")
        logger.info(f"  Files processed: {self.stats['files_processed']}")
        logger.info(f"  Files failed: {self.stats['files_failed']}")
        logger.info(f"  Members extracted: {self.stats['members_extracted']}")
        logger.info(f"  Namespaces: {self.knowledge_base['statistics']['namespaces']}")
        logger.info(f"  Classes: {self.knowledge_base['statistics']['classes']}")
        logger.info(f"  Interfaces: {self.knowledge_base['statistics']['interfaces']}")
        logger.info(f"  Enums: {self.knowledge_base['statistics']['enums']}")
        logger.info(f"  Methods: {self.knowledge_base['statistics']['methods']}")
        logger.info(f"  Properties: {self.knowledge_base['statistics']['properties']}")
        logger.info(f"  Events: {self.knowledge_base['statistics']['events']}")
        logger.info(f"  Duration: {duration:.1f} seconds")

    def save_knowledge_base(self):
        """Save knowledge base to JSON file."""
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, indent=2, ensure_ascii=False)

        logger.info(f"Knowledge base saved to {self.output_path}")

        # Save errors if any
        if self.errors:
            error_path = self.output_path.parent / 'extraction-errors.json'
            with open(error_path, 'w', encoding='utf-8') as f:
                json.dump(self.errors, f, indent=2, ensure_ascii=False)
            logger.warning(f"Errors saved to {error_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract C#/VB API documentation from RecurDyn CHM HTML files'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default=Path('output/extracted_chm/html'),
        help='Input directory containing CHM HTML files'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('output/processnet-csharp-vb-api.json'),
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

    extractor = ChmApiExtractor(args.input, args.output)
    extractor.build_knowledge_base()
    extractor.save_knowledge_base()

    logger.info("Extraction complete!")


if __name__ == '__main__':
    main()
