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

        Enhanced to extract parameter types, descriptions, optional flags, and default values
        from multiple sources: signature spans, field-list documentation, and signature text.

        Args:
            dt_element: BeautifulSoup dt element containing method signature
            dd_element: BeautifulSoup dd element containing method description

        Returns:
            List of Parameter objects
        """
        parameters = []

        # Input validation - limit text length to prevent regex DoS
        MAX_PARAM_TEXT_LENGTH = 10000

        # Method 1: Extract from Sphinx signature spans (<em class="sig-param">)
        sig_params = dt_element.find_all('em', class_='sig-param')
        for sig_param in sig_params:
            param_name_elem = sig_param.find('span', class_='n')
            if param_name_elem:
                param_name = param_name_elem.get_text(strip=True)

                # Extract parameter type from preceding type span
                param_type = ""
                type_elem = sig_param.find('span', class_='property')
                if type_elem:
                    param_type = type_elem.get_text(strip=True)
                else:
                    # Try to find type before parameter name in signature
                    sig_text = sig_param.get_text(strip=True)
                    type_match = re.match(r'([^\s,()]+)\s+' + re.escape(param_name), sig_text)
                    if type_match:
                        param_type = type_match.group(1)

                # Check for default value
                default_val = None
                default_elem = sig_param.find('span', class_='default_value')
                if default_elem:
                    default_val = default_elem.get_text(strip=True)

                parameters.append(Parameter(
                    name=param_name,
                    type=param_type,
                    default=default_val,
                    is_optional=default_val is not None
                ))

        # Method 2: If no params found via spans, parse from signature text
        if not parameters:
            sig_text = dt_element.get_text(strip=True)
            # Match pattern: TypeName(param1, param2=value, param3)
            param_match = re.search(r'\(([^)]*)\)', sig_text)
            if param_match:
                params_str = param_match.group(1)
                if params_str.strip() and params_str.strip() != 'void':
                    # Split by comma (handling nested brackets)
                    param_parts = self._split_parameters(params_str)
                    for part in param_parts:
                        part = part.strip()
                        if not part:
                            continue
                        # Check for default value
                        if '=' in part:
                            param_name, default_val = part.split('=', 1)
                            param_name = param_name.strip()
                            default_val = default_val.strip()
                            # Extract type from before parameter name
                            type_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_<>,\s]*)\s+(\w+)$', param_name)
                            if type_match:
                                param_type = type_match.group(1).strip()
                                param_name = type_match.group(2)
                            else:
                                param_type = ""
                                param_name = param_name.split()[-1] if param_name else part
                            parameters.append(Parameter(
                                name=param_name,
                                type=param_type,
                                default=default_val,
                                is_optional=True
                            ))
                        else:
                            # No default, extract type and name
                            type_match = re.match(r'([a-zA-Z_][a-zA-Z0-9_<>,\s]*)\s+(\w+)$', part)
                            if type_match:
                                param_type = type_match.group(1).strip()
                                param_name = type_match.group(2)
                            else:
                                param_type = ""
                                param_name = part.split()[-1] if part.split() else part
                            parameters.append(Parameter(
                                name=param_name,
                                type=param_type,
                                is_optional=False
                            ))

        # Method 3: Extract parameter types and descriptions from field-list
        if dd_element:
            field_list = dd_element.find('dl', class_='field-list')
            if field_list:
                # Find Parameters field
                for dt in field_list.find_all('dt', class_='field-odd'):
                    if 'Parameters' in dt.get_text() or 'param' in dt.get('text', '').lower():
                        dd = dt.find_next_sibling('dd')
                        if dd:
                            # Parse parameter documentation
                            param_text = dd.get_text()[:MAX_PARAM_TEXT_LENGTH]
                            # Update parameters with types and descriptions from field-list
                            for param in parameters:
                                # Look for parameter name in bold
                                if f"**{param.name}**" in str(dd) or f"<strong>{param.name}</strong>" in str(dd):
                                    # Try markdown format first
                                    param_match = re.search(
                                        rf'\*\*{re.escape(param.name)}\*\*\s*[:\-]\s*([^\-\n*]+?)(?:\n|\*|$)',
                                        str(dd)
                                    )
                                    # Fallback: Try HTML <strong> format
                                    if not param_match:
                                        param_match = re.search(
                                            rf'<strong>{re.escape(param.name)}</strong>\s*[:\-]\s*([^\-<]+?)(?:<|$)',
                                            str(dd)
                                        )
                                    if param_match:
                                        extracted_type = param_match.group(1).strip()
                                        if not param.type and extracted_type:
                                            param.type = extracted_type

                                    # Extract description after type
                                    desc_match = re.search(
                                        rf'\*\*{re.escape(param.name)}\*\*[^:]*:.*?\n(.*?)(?=\n\*\*|\n\n|$)',
                                        str(dd),
                                        re.DOTALL
                                    )
                                    if desc_match:
                                        param.description = desc_match.group(1).strip()[:500]

        return parameters

    def _split_parameters(self, params_str: str) -> list:
        """Split parameter string by comma, handling nested brackets."""
        parts = []
        current = ""
        depth = 0
        for char in params_str:
            if char in '<>[':
                depth += 1
            elif char in '>]':
                depth = max(0, depth - 1)
            elif char == ',' and depth == 0:
                parts.append(current)
                current = ""
            else:
                current += char
        if current:
            parts.append(current)
        return parts

    def parse_sphinx_return_type(self, dd_element, signature_text: str = "") -> tuple:
        """
        Extract return type and description from Sphinx field-list or signature.

        Enhanced to extract from multiple sources: field-list "Returns:", "Return Type",
        "Type", or from the signature text itself (e.g., "void MethodName()").

        Args:
            dd_element: BeautifulSoup dd element containing method description
            signature_text: Optional signature text for parsing return type

        Returns:
            Tuple of (return_type, return_description)
        """
        return_type = ""
        return_desc = ""

        # Method 1: Extract from signature text (e.g., "string MethodName()", "void Method()")
        if signature_text:
            # Pattern: "TypeName MethodName(" or "TypeName ClassName.MethodName("
            sig_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_<>,\s]*)\s+\w+(?:\.\w+)?\s*\(', signature_text)
            if sig_match:
                extracted_type = sig_match.group(1).strip()
                # Clean up type annotations
                extracted_type = re.sub(r'\s+', ' ', extracted_type)
                return_type = extracted_type

        # Method 2: Extract from field-list
        if dd_element:
            field_list = dd_element.find('dl', class_='field-list')
            if field_list:
                # Look for various return type field names (case-insensitive)
                for dt in field_list.find_all('dt'):
                    dt_text = dt.get_text(strip=True)
                    dt_text_lower = dt_text.lower()
                    if any(keyword.lower() in dt_text_lower for keyword in ['Return Type', 'Type', 'Returns', 'rtype']):
                        dd = dt.find_next_sibling('dd')
                        if dd:
                            if 'Return' in dt_text or 'rtype' in dt_text:
                                # Full return description
                                full_text = dd.get_text(strip=True)
                                # Extract first word/type as return type (include generics like list[float])
                                type_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_<>,\s\[\]\.\-]*)', full_text)
                                if type_match:
                                    return_type = return_type or type_match.group(1).strip()
                                    return_desc = full_text[:500]
                            else:
                                # Just the type
                                return_type = return_type or dd.get_text(strip=True)

        # Method 3: Check for void return if no type found
        if not return_type and signature_text:
            if ' void ' in signature_text or signature_text.startswith('void '):
                return_type = 'void'

        return (return_type, return_desc)

    def clean_signature(self, signature: str) -> str:
        """
        Clean up method signature by removing special characters and formatting.

        Removes:
        - Pilcrow symbols (¶)
        - Extra whitespace
        - Trailing punctuation
        - Unicode special characters

        Args:
            signature: Raw signature string

        Returns:
            Cleaned signature string
        """
        if not signature:
            return signature

        # Remove pilcrow symbols and similar
        signature = signature.replace('¶', '')
        signature = signature.replace('\u00b6', '')  # Unicode pilcrow
        signature = signature.replace('\u2191', '')  # Up arrow

        # Remove other common documentation artifacts
        signature = re.sub(r'\s*\[source\]', '', signature)
        signature = re.sub(r'\s*\[edit\]', '', signature)

        # Normalize whitespace
        signature = re.sub(r'\s+', ' ', signature)

        # Remove trailing punctuation (but keep parentheses)
        signature = signature.rstrip('.;,')

        # Remove leading/trailing whitespace
        signature = signature.strip()

        return signature

    def extract_autosummary_members(self, soup: BeautifulSoup) -> dict:
        """
        Extract methods and properties from autosummary tables with rubric headers.
        This is the pattern used in class definition pages (e.g., IForceTire.html).

        Returns:
            dict with 'methods' and 'properties' lists
        """
        results = {'methods': [], 'properties': []}

        # Find all rubric paragraphs
        for rubric in soup.find_all('p', class_='rubric'):
            rubric_text = rubric.get_text(strip=True).lower()

            # Find next sibling table with 'autosummary' class
            table = rubric.find_next('table')
            if not table or 'autosummary' not in ' '.join(table.get('class', [])):
                continue

            # Parse table rows
            tbody = table.find('tbody')
            if not tbody:
                continue

            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) >= 2:
                    # First cell contains member name (in <code> tag)
                    name_cell = cells[0]
                    code_tag = name_cell.find('code')
                    if code_tag:
                        name = code_tag.get_text(strip=True)
                    else:
                        name = name_cell.get_text(strip=True)

                    # Second cell contains description (in <p> tag)
                    desc_cell = cells[1]
                    p_tag = desc_cell.find('p')
                    if p_tag:
                        description = p_tag.get_text(strip=True)
                    else:
                        description = desc_cell.get_text(strip=True)

                    # Categorize based on rubric text
                    if 'method' in rubric_text or 'function' in rubric_text:
                        results['methods'].append(Method(
                            name=name,
                            description=(description or "")[:500],
                            signature=f"{name}()"
                        ))
                    elif 'propert' in rubric_text or 'attribute' in rubric_text:
                        results['properties'].append(Property(
                            name=name,
                            description=(description or "")[:500]
                        ))

        return results

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

    def _is_enum_class(self, inheritance: str) -> bool:
        """
        Check if a class is an enum based on its inheritance.
        Only returns True for classes inheriting from IntEnum.

        Args:
            inheritance: The inheritance string extracted from class definition

        Returns:
            True if the class inherits from IntEnum
        """
        return 'IntEnum' in inheritance

    def extract_enum_members(self, dd_element) -> list:
        """
        Extract enum member values from autosummary tables.

        Enum members are in tables after a "Members" rubric paragraph.
        Each row contains member name and value description.

        Args:
            dd_element: The dd element containing the enum definition

        Returns:
            List of Property objects representing enum members
        """
        members = []

        if not dd_element:
            return members

        # Find "Members" rubric within the enum dd element
        rubric = dd_element.find('p', class_='rubric')
        if not rubric or 'member' not in rubric.get_text().lower():
            return members

        # Find the autosummary table after the rubric
        table = rubric.find_next('table')
        if not table:
            return members

        # Parse table rows
        tbody = table.find('tbody')
        if not tbody:
            return members

        for row in tbody.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 2:
                # Extract member name from code tag
                name_cell = cells[0]
                code_tag = name_cell.find('code')
                if code_tag:
                    member_name = code_tag.get_text(strip=True)
                else:
                    member_name = name_cell.get_text(strip=True)

                # Extract value from description (e.g., "Constant value is 1.")
                desc_cell = cells[1]
                description = desc_cell.get_text(strip=True)

                # Parse numeric value from description
                value = None
                value_match = re.search(r'(?:Constant\s+)?value\s+is\s+(-?\d+)', description, re.IGNORECASE)
                if value_match:
                    value = value_match.group(1)

                members.append(Property(
                    name=member_name,
                    type='int',
                    description=f"Value: {value}. {description}" if value else description[:500],
                    read_only=True
                ))

        return members

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

                            # Create class definition
                            class_def = ClassDef(
                                name=class_name,
                                description=(description or "")[:500],
                                inheritance=inheritance
                            )

                            # If it's an enum (IntEnum), extract enum members as properties
                            if self._is_enum_class(inheritance):
                                enum_members = self.extract_enum_members(dd)
                                for member in enum_members:
                                    class_def.properties.append(member)

                            classes.append(class_def)

        return classes

    def extract_method_signatures(self, soup: BeautifulSoup) -> list:
        """
        Extract method signatures from Sphinx-formatted documentation.

        Supports both legacy definition lists and Sphinx .py.method patterns.
        Enhanced to extract parameter types and return types with signature cleanup.

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
                        # Clean up the signature
                        sig_text = self.clean_signature(sig_text)

                        # Extract description
                        description = ""
                        if dd:
                            # Get first paragraph as description
                            first_p = dd.find('p', recursive=False)
                            if first_p:
                                description = first_p.get_text(strip=True)

                        # Parse parameters from signature and field-list
                        parameters = self.parse_sphinx_parameters(dt, dd)

                        # Parse return type with signature text for better extraction
                        return_type, return_desc = self.parse_sphinx_return_type(dd, sig_text)

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
                    # Clean signature
                    sig_text = self.clean_signature(sig_text)

                    # Check if it looks like a method signature
                    if '(' in sig_text and ')' in sig_text:
                        dd = dt.find_next_sibling('dd')
                        description = dd.get_text(strip=True) if dd else ""

                        # Parse method name
                        match = re.match(r'(\w+)\s*\(', sig_text)
                        if match:
                            method_name = match.group(1)

                            # Try to extract parameters even from legacy format
                            parameters = self.parse_sphinx_parameters(dt, dd)

                            # Extract return type from signature
                            return_type, _ = self.parse_sphinx_return_type(dd, sig_text)

                            methods.append(Method(
                                name=method_name,
                                signature=sig_text,
                                description=description[:500],
                                parameters=[asdict(p) for p in parameters],
                                returns=return_type
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

        # ENHANCEMENT: Extract members from autosummary tables (class definition pages)
        autosummary_members = self.extract_autosummary_members(soup)
        result['properties'].extend(autosummary_members['properties'])
        result['methods'].extend(autosummary_members['methods'])

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

    def _extract_class_name_from_filename(self, file_path: Path) -> Optional[str]:
        """
        Extract class name from filename using naming convention.
        Examples:
          IApplication_Save.html -> IApplication
          IBody_GetMass.html -> IBody
          CoreExample.html -> CoreExample
        """
        filename = file_path.stem  # Remove .html extension

        # Check for underscore pattern: ClassName_MemberName
        if '_' in filename:
            parts = filename.split('_')
            if len(parts) >= 2:
                return parts[0]

        # If no underscore, the filename itself might be the class name
        return filename

    def _is_member_file(self, file_path: Path) -> bool:
        """
        Detect if file is a member (method/property) file based on path.
        Returns True if path contains Methods or Properties subfolder.

        Examples:
          Python/Professional/IApplication/Methods/IApplication_Save.html -> True
          Python/Professional/IApplication.html -> False
        """
        parts = file_path.parts
        return 'Methods' in parts or 'Properties' in parts

    def _extract_parent_class_from_path(self, file_path: Path) -> Optional[str]:
        """
        Extract parent class name from directory structure for member files.

        Examples:
          Python/Professional/IApplication/Methods/IApplication_Save.html -> IApplication
          Python/Professional/IBody/Properties/IBody_Mass.html -> IBody
        """
        parts = file_path.parts

        # Find Methods or Properties folder
        for i, part in enumerate(parts):
            if part in ('Methods', 'Properties'):
                # Parent class is the folder before Methods/Properties
                if i > 0:
                    return parts[i - 1]

        return None

    def _associate_members_with_classes(self, ns_data: dict, file_path: Path, content: dict, is_member_file: bool = False):
        """
        Associate methods and properties with their parent classes based on filename.
        This fixes the bug where all members were stored at namespace level.

        Args:
            ns_data: Namespace data dictionary
            file_path: Path to the HTML file
            content: Parsed content from the file
            is_member_file: True if file is in /Methods/ or /Properties/ subfolder
        """
        # Determine parent class name
        if is_member_file:
            class_name = self._extract_parent_class_from_path(file_path)
        else:
            class_name = self._extract_class_name_from_filename(file_path)

        if not class_name:
            return

        # Find the class in namespace
        target_class = None
        for cls in ns_data['classes']:
            if cls['name'].lower() == class_name.lower():
                target_class = cls
                break

        # CRITICAL FIX: Only create class entry if NOT a member file
        if not target_class and (content['methods'] or content['properties']):
            if is_member_file:
                # Member file without parent class - log as orphan
                logger.warning(
                    f"Orphaned member file: {file_path.name} - "
                    f"Parent class '{class_name}' not found. "
                    f"Methods: {len(content['methods'])}, Properties: {len(content['properties'])}"
                )
                # Collect orphans for manual review
                if 'orphaned_members' not in ns_data:
                    ns_data['orphaned_members'] = []
                ns_data['orphaned_members'].append({
                    'file': str(file_path.relative_to(self.input_path)),
                    'parent_class': class_name,
                    'methods': [m.name for m in content['methods']],
                    'properties': [p.name for p in content['properties']]
                })
                return
            else:
                # Regular class file - create class entry
                target_class = {
                    'name': class_name,
                    'description': f'Class {class_name}',
                    'inheritance': '',
                    'methods': [],
                    'properties': [],
                    'source_file': str(file_path.relative_to(self.input_path))
                }
                ns_data['classes'].append(target_class)

                # Add to class index
                class_lower = class_name.lower()
                namespace = [k for k, v in self.knowledge_base['namespaces'].items() if v is ns_data][0]
                if class_lower not in self.knowledge_base['class_index']:
                    self.knowledge_base['class_index'][class_lower] = []
                if namespace not in self.knowledge_base['class_index'][class_lower]:
                    self.knowledge_base['class_index'][class_lower].append(namespace)

        # Associate methods with class
        if target_class and content['methods']:
            for method in content['methods']:
                method_dict = asdict(method)
                # Check if not already in class methods
                if not any(m['name'] == method_dict['name'] for m in target_class['methods']):
                    target_class['methods'].append(method_dict)

        # Associate properties with class
        if target_class and content['properties']:
            for prop in content['properties']:
                prop_dict = asdict(prop)
                # Check if not already in class properties
                if not any(p['name'] == prop_dict['name'] for p in target_class['properties']):
                    target_class['properties'].append(prop_dict)

    def build_knowledge_base(self):
        """Build the complete knowledge base from all files."""
        start_time = datetime.now()

        logger.info(f"Discovering files in {self.input_path}...")
        files = self.discover_files()
        logger.info(f"Found {len(files)} HTML files")

        # Sort files by path depth - process class definition files (shallow) before member files (deep)
        # This ensures parent classes exist before we try to associate members
        files.sort(key=lambda p: len(p.parts))
        logger.info("Files sorted by path depth (class files first, then member files)")

        # Initialize ProcessNet namespace
        self.knowledge_base['namespaces']['ProcessNet'] = {
            'full_name': 'FunctionBay.RecurDyn.ProcessNet',
            'description': 'RecurDyn ProcessNet API for automation',
            'classes': [],
            'standalone_methods': [],
            'examples': [],
            'files': []
        }

        # Track member file statistics
        member_files_processed = 0
        orphaned_members_count = 0

        for idx, file_path in enumerate(files, 1):
            progress = (idx / len(files)) * 100
            if idx % 100 == 0 or idx == len(files):
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
                        # Check if class already exists
                        existing = any(c['name'] == cls_dict['name'] for c in ns_data['classes'])
                        if not existing:
                            ns_data['classes'].append(cls_dict)

                            # Add to class index
                            class_lower = cls.name.lower()
                            if class_lower not in self.knowledge_base['class_index']:
                                self.knowledge_base['class_index'][class_lower] = []
                            if namespace not in self.knowledge_base['class_index'][class_lower]:
                                self.knowledge_base['class_index'][class_lower].append(namespace)
                            self.stats['classes_extracted'] += 1

                # Detect if this is a member file (in /Methods/ or /Properties/ subfolder)
                is_member_file = self._is_member_file(file_path)
                if is_member_file:
                    member_files_processed += 1

                # Associate methods/properties with classes based on filename
                self._associate_members_with_classes(ns_data, file_path, content, is_member_file)

                # Track orphaned members (member files without parent class)
                if 'orphaned_members' in ns_data:
                    orphaned_members_count = len(ns_data['orphaned_members'])

                # REMOVED: standalone_methods[] population (as per validation decision)
                # Member files should NOT be added to standalone_methods
                # Only track methods for indexing purposes
                if content['methods']:
                    for method in content['methods']:
                        # Add to method index for search purposes
                        method_lower = method.name.lower()
                        if method_lower not in self.knowledge_base['method_index']:
                            self.knowledge_base['method_index'][method_lower] = []
                        if namespace not in self.knowledge_base['method_index'][method_lower]:
                            self.knowledge_base['method_index'][method_lower].append(namespace)
                        self.stats['methods_extracted'] += 1

                # Add properties to namespace (backward compatibility)
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
        logger.info(f"  Member files processed: {member_files_processed}")
        logger.info(f"  Orphaned members: {orphaned_members_count}")
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

                # Count methods from all classes
                classes = ns_data.get('classes', [])
                total_methods = sum(len(cls.get('methods', [])) for cls in classes)

                f.write(f"**Classes:** {len(classes)}\n\n")
                f.write(f"**Methods:** {total_methods}\n\n")
                f.write(f"**Examples:** {len(ns_data.get('examples', []))}\n\n")

                # Classes section with methods grouped by class
                if classes:
                    f.write("## Classes\n\n")
                    for cls in classes:
                        cls_name = cls.get('name', 'Unknown')
                        f.write(f"### {cls_name}\n\n")

                        if cls.get('description'):
                            f.write(f"{cls['description']}\n\n")

                        # Show methods for this class
                        methods = cls.get('methods', [])
                        if methods:
                            f.write(f"**Methods ({len(methods)}):**\n\n")
                            for method in methods[:10]:  # Limit 10 methods per class
                                method_name = method.get('name', 'Unknown')
                                f.write(f"#### {method_name}\n\n")
                                if method.get('signature'):
                                    f.write(f"```\n{method['signature']}\n```\n\n")
                                if method.get('description'):
                                    f.write(f"{method['description'][:300]}\n\n")

                            if len(methods) > 10:
                                f.write(f"*... and {len(methods) - 10} more methods*\n\n")

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
