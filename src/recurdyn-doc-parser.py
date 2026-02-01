#!/usr/bin/env python3
"""
RecurDyn ProcessNet Documentation Parser

Extracts API documentation from RecurDyn HTML files and builds a structured
knowledge base for automation workflows.

Usage:
    python recurdyn-doc-parser.py [--input PATH] [--output PATH]
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
class Parameter:
    """Represents a method parameter."""
    name: str
    type: str = ""
    description: str = ""
    default: Optional[str] = None
    is_optional: bool = False
    is_out: bool = False


@dataclass
class Method:
    """Represents a class method or function."""
    name: str
    signature: str = ""
    description: str = ""
    parameters: list = field(default_factory=list)
    returns: str = ""
    return_description: str = ""
    example_code: str = ""
    source_file: str = ""
    exceptions: list = field(default_factory=list)
    is_static: bool = False
    access_modifier: str = ""


@dataclass
class Property:
    """Represents a class property."""
    name: str
    type: str = ""
    description: str = ""
    read_only: bool = False
    source_file: str = ""


@dataclass
class ClassDef:
    """Represents a class definition."""
    name: str
    description: str = ""
    inheritance: str = ""
    methods: list = field(default_factory=list)
    properties: list = field(default_factory=list)
    source_file: str = ""


@dataclass
class CodeExample:
    """Represents a code example."""
    title: str = ""
    code: str = ""
    language: str = "csharp"
    description: str = ""
    source_file: str = ""


@dataclass
class Namespace:
    """Represents a namespace."""
    name: str
    full_name: str = ""
    description: str = ""
    classes: list = field(default_factory=list)
    standalone_methods: list = field(default_factory=list)
    examples: list = field(default_factory=list)
    files: list = field(default_factory=list)


class ProcessNetDocParser:
    """Parser for RecurDyn ProcessNet documentation."""

    # Known ProcessNet interfaces and classes
    KNOWN_INTERFACES = [
        'IApplication', 'IModelDocument', 'IPlotDocument', 'ISubSystem',
        'IBody', 'IReferenceFrame', 'IMarker', 'IJoint', 'IForce',
        'IGeometry', 'IRequest', 'IResult', 'IContact', 'IConstraint',
        'ISpring', 'IDamper', 'IMotion', 'ISensor', 'IExpression',
        'IRecurDynApp', 'RDApplication'
    ]

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
                'source': 'RecurDyn ProcessNet API',
                'version': 'extracted',
                'extraction_date': datetime.now().isoformat(),
                'total_files_processed': 0,
                'extraction_duration_seconds': 0
            },
            'namespaces': {},
            'method_index': {},
            'class_index': {},
            'interface_index': {}
        }
        self.errors = []
        self.stats = {
            'files_processed': 0,
            'files_skipped': 0,
            'files_failed': 0,
            'methods_extracted': 0,
            'classes_extracted': 0,
            'properties_extracted': 0,
            'examples_extracted': 0
        }

    def discover_files(self) -> list:
        """Discover all documentation files recursively."""
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
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = chardet.detect(raw_data)
            return result.get('encoding', 'utf-8') or 'utf-8'

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

    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title."""
        title_tag = soup.find('title')
        if title_tag:
            title = title_tag.get_text(strip=True)
            # Remove common suffixes
            title = re.sub(r'\s*[—–-]\s*RecurDyn.*$', '', title)
            return title
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        return ""

    def extract_code_blocks(self, soup: BeautifulSoup, source_file: str) -> list:
        """Extract code examples from HTML."""
        examples = []

        # Find code blocks in highlight divs
        for highlight in soup.find_all('div', class_='highlight'):
            pre = highlight.find('pre')
            if pre:
                code = pre.get_text()
                # Detect language from class
                lang = 'csharp'
                for cls in highlight.get('class', []):
                    if 'python' in cls.lower():
                        lang = 'python'
                    elif 'c#' in cls.lower() or 'csharp' in cls.lower():
                        lang = 'csharp'

                # Check if code contains ProcessNet-related content
                if any(iface in code for iface in self.KNOWN_INTERFACES) or \
                   'FunctionBay.RecurDyn' in code or 'ProcessNet' in code:
                    examples.append(CodeExample(
                        code=code.strip(),
                        language=lang,
                        source_file=source_file
                    ))

        return examples

    def extract_interfaces_from_code(self, code: str) -> list:
        """Extract interface references from code."""
        found = []
        for iface in self.KNOWN_INTERFACES:
            if iface in code:
                found.append(iface)
        return found

    def parse_sphinx_parameters(self, dt_element, dd_element) -> list:
        """
        Extract parameters from Sphinx-formatted method documentation.

        Parses both signature parameters and field-list parameter documentation.

        Args:
            dt_element: BeautifulSoup dt element containing method signature
            dd_element: BeautifulSoup dd element containing method description

        Returns:
            List of Parameter objects
        """
        parameters = []

        # Input validation - limit text length to prevent regex DoS
        MAX_PARAM_TEXT_LENGTH = 10000

        # Extract parameter names from signature
        sig_params = dt_element.find_all('em', class_='sig-param')
        for sig_param in sig_params:
            param_name_elem = sig_param.find('span', class_='n')
            if param_name_elem:
                param_name = param_name_elem.get_text(strip=True)

                # Check for default value
                default_val = None
                default_elem = sig_param.find('span', class_='default_value')
                if default_elem:
                    default_val = default_elem.get_text(strip=True)

                parameters.append(Parameter(
                    name=param_name,
                    default=default_val,
                    is_optional=default_val is not None
                ))

        # Extract parameter types and descriptions from field-list
        if dd_element:
            field_list = dd_element.find('dl', class_='field-list')
            if field_list:
                # Find Parameters field
                for dt in field_list.find_all('dt', class_='field-odd'):
                    if 'Parameters' in dt.get_text():
                        dd = dt.find_next_sibling('dd')
                        if dd:
                            # Parse parameter documentation
                            param_text = dd.get_text()[:MAX_PARAM_TEXT_LENGTH]
                            # Format: **ParamName** - ParamType or ParamName - ParamType (plain text)
                            for param in parameters:
                                # Look for parameter name in bold
                                if f"**{param.name}**" in str(dd) or f"<strong>{param.name}</strong>" in str(dd):
                                    # Try markdown format first
                                    param_match = re.search(
                                        rf'\*\*{re.escape(param.name)}\*\*\s*-\s*([^\-\n]+)',
                                        param_text
                                    )
                                    if param_match:
                                        param.type = param_match.group(1).strip()
                                    else:
                                        # Try without dash separator (markdown)
                                        param_match = re.search(
                                            rf'\*\*{re.escape(param.name)}\*\*\s+([^\n]+)',
                                            param_text
                                        )
                                        if param_match:
                                            param.type = param_match.group(1).strip()
                                        else:
                                            # Try plain text format: ParamName - Type
                                            param_match = re.search(
                                                rf'{re.escape(param.name)}\s*-\s*([^\n]+)',
                                                param_text
                                            )
                                            if param_match:
                                                param.type = param_match.group(1).strip()

        return parameters

    def parse_sphinx_return_type(self, dd_element) -> tuple:
        """
        Extract return type and description from Sphinx field-list.

        Args:
            dd_element: BeautifulSoup dd element containing method description

        Returns:
            Tuple of (return_type, return_description)
        """
        if not dd_element:
            return ("", "")

        field_list = dd_element.find('dl', class_='field-list')
        if not field_list:
            return ("", "")

        # Look for "Return Type" or "Type" field
        for dt in field_list.find_all('dt'):
            dt_text = dt.get_text(strip=True)
            if 'Return Type' in dt_text or dt_text == 'Type':
                dd = dt.find_next_sibling('dd')
                if dd:
                    return_type = dd.get_text(strip=True)
                    return (return_type, "")

        return ("", "")

    def extract_sphinx_properties(self, soup: BeautifulSoup) -> list:
        """
        Extract property definitions from Sphinx-formatted documentation.

        Returns:
            List of Property objects
        """
        properties = []

        # Find .py.property definition lists
        for dl in soup.find_all('dl', class_='py'):
            if 'property' in dl.get('class', []):
                dt = dl.find('dt', class_='sig')
                dd = dl.find('dd', recursive=False)

                if dt:
                    # Extract property name from .sig-name.descname
                    name_elem = dt.find('span', class_='sig-name')
                    if not name_elem:
                        name_elem = dt.find('span', class_='descname')

                    if name_elem:
                        prop_name = name_elem.get_text(strip=True)

                        # Extract description
                        description = ""
                        if dd:
                            first_p = dd.find('p', recursive=False)
                            if first_p:
                                description = first_p.get_text(strip=True)

                        # Extract type from field-list
                        prop_type = ""
                        read_only = False

                        if dd:
                            field_list = dd.find('dl', class_='field-list')
                            if field_list:
                                for dt_field in field_list.find_all('dt'):
                                    if 'Type' in dt_field.get_text():
                                        dd_field = dt_field.find_next_sibling('dd')
                                        if dd_field:
                                            prop_type = dd_field.get_text(strip=True)

                            # Check for read-only indicator
                            if 'read-only' in description.lower() or 'readonly' in description.lower():
                                read_only = True

                        properties.append(Property(
                            name=prop_name,
                            type=prop_type,
                            description=(description or "")[:500],
                            read_only=read_only
                        ))

        return properties

    def extract_sphinx_classes(self, soup: BeautifulSoup) -> list:
        """
        Extract class definitions from Sphinx-formatted documentation.

        Returns:
            List of ClassDef objects
        """
        classes = []

        # Find .py.class definition lists
        for dl in soup.find_all('dl', class_='py'):
            if 'class' in dl.get('class', []):
                dt = dl.find('dt', class_='sig')
                dd = dl.find('dd', recursive=False)

                if dt:
                    # Check if it's actually a class (has 'class' keyword or 'Bases:')
                    property_elem = dt.find('em', class_='property')
                    is_class = False
                    if property_elem and 'class' in property_elem.get_text().lower():
                        is_class = True

                    # Also check for 'Bases:' in description (enum/class indicator)
                    if dd:
                        dd_text = dd.get_text()
                        if 'Bases:' in dd_text:
                            is_class = True

                    if is_class:
                        # Extract class name
                        name_elem = dt.find('span', class_='sig-name')
                        if not name_elem:
                            name_elem = dt.find('span', class_='descname')
                        if not name_elem:
                            name_elem = dt.find('span', class_='sig-prename')

                        if name_elem:
                            class_name = name_elem.get_text(strip=True)

                            # Extract description
                            description = ""
                            inheritance = ""

                            if dd:
                                # Extract Bases/inheritance
                                bases_match = re.search(r'Bases?:\s*(.+?)(?:\n|$)', dd.get_text())
                                if bases_match:
                                    inheritance = bases_match.group(1).strip()

                                # Get description (first paragraph)
                                first_p = dd.find('p', recursive=False)
                                if first_p and 'Bases:' not in first_p.get_text():
                                    description = first_p.get_text(strip=True)
                                elif dd.find_all('p'):
                                    # Try second paragraph if first is Bases
                                    paragraphs = dd.find_all('p', recursive=False)
                                    if len(paragraphs) > 1:
                                        description = paragraphs[1].get_text(strip=True)

                            classes.append(ClassDef(
                                name=class_name,
                                description=(description or "")[:500],
                                inheritance=inheritance
                            ))

        return classes

    def extract_method_signatures(self, soup: BeautifulSoup) -> list:
        """
        Extract method signatures from Sphinx-formatted documentation.

        Supports both legacy definition lists and Sphinx .py.method patterns.

        Returns:
            List of Method objects with parameters and return types
        """
        methods = []

        # Extract Sphinx-style methods (.py.method)
        for dl in soup.find_all('dl', class_='py'):
            # Check if it's a method (not property or class)
            if 'method' in dl.get('class', []) or 'function' in dl.get('class', []):
                dt = dl.find('dt', class_='sig')
                dd = dl.find('dd', recursive=False)

                if dt:
                    # Extract method name from .sig-name.descname
                    name_elem = dt.find('span', class_='sig-name')
                    if not name_elem:
                        name_elem = dt.find('span', class_='descname')

                    if name_elem:
                        method_name = name_elem.get_text(strip=True)

                        # Extract full signature text
                        sig_text = dt.get_text(strip=True)

                        # Extract description
                        description = ""
                        if dd:
                            # Get first paragraph as description
                            first_p = dd.find('p', recursive=False)
                            if first_p:
                                description = first_p.get_text(strip=True)

                        # Parse parameters from signature and field-list
                        parameters = self.parse_sphinx_parameters(dt, dd)

                        # Parse return type
                        return_type, return_desc = self.parse_sphinx_return_type(dd)

                        methods.append(Method(
                            name=method_name,
                            signature=sig_text,
                            description=(description or "")[:500],
                            parameters=[asdict(p) for p in parameters],
                            returns=return_type,
                            return_description=return_desc
                        ))

        # Fallback: legacy definition list extraction
        if not methods:
            for dl in soup.find_all('dl'):
                for dt in dl.find_all('dt', recursive=False):
                    sig_text = dt.get_text(strip=True)
                    # Check if it looks like a method signature
                    if '(' in sig_text and ')' in sig_text:
                        dd = dt.find_next_sibling('dd')
                        description = dd.get_text(strip=True) if dd else ""

                        # Parse method name
                        match = re.match(r'(\w+)\s*\(', sig_text)
                        if match:
                            method_name = match.group(1)
                            methods.append(Method(
                                name=method_name,
                                signature=sig_text,
                                description=description[:500]
                            ))

        return methods

    def determine_namespace_from_content(self, soup: BeautifulSoup, title: str) -> str:
        """
        Determine namespace from HTML content.

        Checks for module ID, title content, and file structure.

        Returns:
            Namespace string (e.g., 'ProcessNet.Geometry', 'ProcessNet')
        """
        # Check for Sphinx module ID
        section = soup.find('section', id=lambda x: x and x.startswith('module-recurdyn.'))
        if section:
            module_id = section.get('id', '')
            # Extract module name from id="module-recurdyn.ModuleName"
            match = re.search(r'module-recurdyn\.(.+)', module_id)
            if match:
                module_name = match.group(1)
                # Convert to ProcessNet namespace
                if module_name != 'recurdyn':
                    return f'ProcessNet.{module_name}'

        # Check title for namespace indicators
        if 'ProcessNet' in title:
            return 'ProcessNet'

        # Check for recurdyn module references
        dt_elements = soup.find_all('dt', class_='sig')
        for dt in dt_elements:
            dt_id = dt.get('id', '')
            if dt_id.startswith('recurdyn.'):
                # Extract: recurdyn.ModuleName.ClassName
                parts = dt_id.split('.')
                if len(parts) >= 2:
                    module_name = parts[1]
                    return f'ProcessNet.{module_name}'

        return 'ProcessNet'

    def parse_html_file(self, file_path: Path) -> dict:
        """Parse a single HTML file and extract content."""
        result = {
            'title': '',
            'namespace': '',
            'classes': [],
            'properties': [],
            'methods': [],
            'examples': [],
            'interfaces_referenced': []
        }

        soup = self.read_html_file(file_path)
        if not soup:
            return result

        rel_path = str(file_path.relative_to(self.input_path))

        # Extract title
        result['title'] = self.extract_title(soup)

        # Determine namespace
        result['namespace'] = self.determine_namespace_from_content(soup, result['title'])

        # Extract Sphinx-formatted content
        result['classes'] = self.extract_sphinx_classes(soup)
        result['properties'] = self.extract_sphinx_properties(soup)
        result['methods'] = self.extract_method_signatures(soup)

        # Extract code examples
        result['examples'] = self.extract_code_blocks(soup, rel_path)

        # Extract interfaces from all code
        main_content = soup.find('div', class_='document') or soup.find('main') or soup.body
        if main_content:
            text = main_content.get_text()
            result['interfaces_referenced'] = self.extract_interfaces_from_code(text)

        # Add source file to all extracted items
        for method in result['methods']:
            method.source_file = rel_path
        for prop in result['properties']:
            prop.source_file = rel_path
        for cls in result['classes']:
            cls.source_file = rel_path

        return result

    def build_knowledge_base(self):
        """Build the complete knowledge base from all files."""
        start_time = datetime.now()

        logger.info(f"Discovering files in {self.input_path}...")
        files = self.discover_files()
        logger.info(f"Found {len(files)} HTML files")

        # Initialize ProcessNet namespace
        self.knowledge_base['namespaces']['ProcessNet'] = {
            'full_name': 'FunctionBay.RecurDyn.ProcessNet',
            'description': 'RecurDyn ProcessNet API for automation',
            'classes': [],
            'standalone_methods': [],
            'examples': [],
            'files': []
        }

        for idx, file_path in enumerate(files, 1):
            progress = (idx / len(files)) * 100
            logger.info(f"[{progress:5.1f}%] ({idx}/{len(files)}) {file_path.name}")

            try:
                content = self.parse_html_file(file_path)
                namespace = content.get('namespace', 'ProcessNet')

                # Ensure namespace exists in knowledge base
                if namespace not in self.knowledge_base['namespaces']:
                    self.knowledge_base['namespaces'][namespace] = {
                        'full_name': f'FunctionBay.RecurDyn.{namespace}',
                        'description': f'{namespace} API',
                        'classes': [],
                        'standalone_methods': [],
                        'examples': [],
                        'files': []
                    }

                ns_data = self.knowledge_base['namespaces'][namespace]

                # Add classes to namespace
                if content['classes']:
                    for cls in content['classes']:
                        cls_dict = asdict(cls)
                        ns_data['classes'].append(cls_dict)

                        # Add to class index
                        class_lower = cls.name.lower()
                        if class_lower not in self.knowledge_base['class_index']:
                            self.knowledge_base['class_index'][class_lower] = []
                        if namespace not in self.knowledge_base['class_index'][class_lower]:
                            self.knowledge_base['class_index'][class_lower].append(namespace)
                        self.stats['classes_extracted'] += 1

                # Add properties to namespace
                if content['properties']:
                    # Initialize properties list if not exists
                    if 'properties' not in ns_data:
                        ns_data['properties'] = []

                    for prop in content['properties']:
                        prop_dict = asdict(prop)
                        ns_data['properties'].append(prop_dict)
                        self.stats['properties_extracted'] += 1

                # Add examples to namespace
                if content['examples']:
                    for ex in content['examples']:
                        ex_dict = asdict(ex)
                        ns_data['examples'].append(ex_dict)
                        self.stats['examples_extracted'] += 1

                # Add methods to namespace
                if content['methods']:
                    for method in content['methods']:
                        method_dict = asdict(method)
                        ns_data['standalone_methods'].append(method_dict)

                        # Add to method index
                        method_lower = method.name.lower()
                        if method_lower not in self.knowledge_base['method_index']:
                            self.knowledge_base['method_index'][method_lower] = []
                        if namespace not in self.knowledge_base['method_index'][method_lower]:
                            self.knowledge_base['method_index'][method_lower].append(namespace)
                        self.stats['methods_extracted'] += 1

                # Track interfaces
                for iface in content['interfaces_referenced']:
                    iface_lower = iface.lower()
                    if iface_lower not in self.knowledge_base['interface_index']:
                        self.knowledge_base['interface_index'][iface_lower] = []
                    if namespace not in self.knowledge_base['interface_index'][iface_lower]:
                        self.knowledge_base['interface_index'][iface_lower].append(namespace)

                # Add file to namespace
                rel_path = str(file_path.relative_to(self.input_path))
                if rel_path not in ns_data['files']:
                    ns_data['files'].append(rel_path)

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
        logger.info(f"  Classes extracted: {self.stats['classes_extracted']}")
        logger.info(f"  Methods extracted: {self.stats['methods_extracted']}")
        logger.info(f"  Properties extracted: {self.stats['properties_extracted']}")
        logger.info(f"  Examples extracted: {self.stats['examples_extracted']}")
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

    def generate_markdown(self, output_dir: Path):
        """Generate markdown documentation from knowledge base."""
        output_dir.mkdir(parents=True, exist_ok=True)

        for ns_name, ns_data in self.knowledge_base['namespaces'].items():
            md_path = output_dir / f"{ns_name.replace('.', '_')}.md"

            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(f"# {ns_name}\n\n")
                f.write(f"> {ns_data.get('description', '')}\n\n")

                # Overview
                f.write("## Overview\n\n")
                f.write(f"**Full Name:** {ns_data.get('full_name', ns_name)}\n\n")
                f.write(f"**Methods:** {len(ns_data.get('standalone_methods', []))}\n\n")
                f.write(f"**Examples:** {len(ns_data.get('examples', []))}\n\n")

                # Methods
                if ns_data.get('standalone_methods'):
                    f.write("## Methods\n\n")
                    for method in ns_data['standalone_methods'][:50]:  # Limit for readability
                        f.write(f"### {method['name']}\n\n")
                        if method.get('signature'):
                            f.write(f"```\n{method['signature']}\n```\n\n")
                        if method.get('description'):
                            f.write(f"{method['description']}\n\n")

                # Examples
                if ns_data.get('examples'):
                    f.write("## Code Examples\n\n")
                    for i, example in enumerate(ns_data['examples'][:20], 1):
                        f.write(f"### Example {i}\n\n")
                        if example.get('title'):
                            f.write(f"**{example['title']}**\n\n")
                        f.write(f"```{example.get('language', 'csharp')}\n")
                        f.write(example.get('code', '')[:2000])  # Limit code length
                        f.write("\n```\n\n")
                        if example.get('source_file'):
                            f.write(f"*Source: {example['source_file']}*\n\n")

            logger.info(f"Generated {md_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract ProcessNet API documentation from RecurDyn HTML files'
    )
    parser.add_argument(
        '--input', '-i',
        type=Path,
        default=Path('knowledge'),
        help='Input directory containing HTML documentation'
    )
    parser.add_argument(
        '--output', '-o',
        type=Path,
        default=Path('output/processnet-knowledge.json'),
        help='Output JSON file path'
    )
    parser.add_argument(
        '--markdown', '-m',
        type=Path,
        default=Path('output/markdown'),
        help='Output directory for markdown files'
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

    doc_parser = ProcessNetDocParser(args.input, args.output)
    doc_parser.build_knowledge_base()
    doc_parser.save_knowledge_base()
    doc_parser.generate_markdown(args.markdown)

    logger.info("Extraction complete!")


if __name__ == '__main__':
    main()
