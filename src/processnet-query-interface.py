#!/usr/bin/env python3
"""
ProcessNet Knowledge Base Query Interface

Provides search and query functionality for the ProcessNet API knowledge base.

Usage:
    python processnet-query-interface.py [--search QUERY] [--kb PATH]
    python processnet-query-interface.py  # Interactive mode
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

try:
    from rapidfuzz import fuzz, process
    FUZZY_AVAILABLE = True
except ImportError:
    FUZZY_AVAILABLE = False
    print("Warning: rapidfuzz not installed. Fuzzy search disabled.")


@dataclass
class SearchResult:
    """Represents a search result."""
    name: str
    type: str  # 'method', 'class', 'interface', 'example'
    namespace: str
    signature: str = ""
    description: str = ""
    code: str = ""
    source_file: str = ""
    score: float = 100.0


class ProcessNetKnowledge:
    """Query interface for ProcessNet knowledge base."""

    def __init__(self, kb_path: str = "output/processnet-knowledge.json"):
        self.kb_path = Path(kb_path)
        self.kb = None
        self._method_names = []
        self._interface_names = []
        self._load_knowledge_base()

    def _load_knowledge_base(self):
        """Load the knowledge base from JSON file."""
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base not found: {self.kb_path}")

        with open(self.kb_path, 'r', encoding='utf-8') as f:
            self.kb = json.load(f)

        # Build search indices
        self._build_indices()

    def _build_indices(self):
        """Build in-memory search indices."""
        self._method_names = list(self.kb.get('method_index', {}).keys())
        self._interface_names = list(self.kb.get('interface_index', {}).keys())

        # Extract method names from examples
        for ns_name, ns_data in self.kb.get('namespaces', {}).items():
            for example in ns_data.get('examples', []):
                code = example.get('code', '')
                # Extract method calls
                methods = re.findall(r'\.(\w+)\s*\(', code)
                for m in methods:
                    m_lower = m.lower()
                    if m_lower not in self._method_names:
                        self._method_names.append(m_lower)

    def find_method(self, method_name: str, namespace: Optional[str] = None) -> list:
        """
        Find method by exact name match (case-insensitive).

        Args:
            method_name: Method name to search for
            namespace: Optional namespace filter

        Returns:
            List of matching SearchResult objects
        """
        results = []
        method_lower = method_name.lower()

        # Search in method index
        if method_lower in self.kb.get('method_index', {}):
            namespaces = self.kb['method_index'][method_lower]
            for ns in namespaces:
                if namespace and ns.lower() != namespace.lower():
                    continue

                # Find the method in namespace data
                ns_data = self.kb['namespaces'].get(ns, {})
                for method in ns_data.get('standalone_methods', []):
                    if method['name'].lower() == method_lower:
                        results.append(SearchResult(
                            name=method['name'],
                            type='method',
                            namespace=ns,
                            signature=method.get('signature', ''),
                            description=method.get('description', ''),
                            source_file=method.get('source_file', '')
                        ))

        # Search in code examples
        for ns_name, ns_data in self.kb.get('namespaces', {}).items():
            if namespace and ns_name.lower() != namespace.lower():
                continue

            for example in ns_data.get('examples', []):
                code = example.get('code', '')
                if f'.{method_name}(' in code or f' {method_name}(' in code:
                    # Extract signature from code
                    pattern = rf'\.{re.escape(method_name)}\s*\([^)]*\)'
                    match = re.search(pattern, code)
                    sig = match.group(0) if match else f".{method_name}()"

                    results.append(SearchResult(
                        name=method_name,
                        type='example',
                        namespace=ns_name,
                        signature=sig,
                        code=code[:500],
                        source_file=example.get('source_file', '')
                    ))

        return results

    def search_method_fuzzy(self, query: str, threshold: float = 60.0, limit: int = 10) -> list:
        """
        Search for methods using fuzzy string matching.

        Args:
            query: Search query
            threshold: Minimum similarity score (0-100)
            limit: Maximum results to return

        Returns:
            List of matching SearchResult objects
        """
        if not FUZZY_AVAILABLE:
            # Fallback to simple substring matching
            return self._search_substring(query, limit)

        results = []

        # Search in method names
        if self._method_names:
            matches = process.extract(
                query.lower(),
                self._method_names,
                scorer=fuzz.WRatio,
                limit=limit
            )

            for match_name, score, _ in matches:
                if score >= threshold:
                    # Get full method info
                    method_results = self.find_method(match_name)
                    for r in method_results:
                        r.score = score
                        results.append(r)

        # Search in interface names
        if self._interface_names:
            matches = process.extract(
                query.lower(),
                self._interface_names,
                scorer=fuzz.WRatio,
                limit=limit
            )

            for match_name, score, _ in matches:
                if score >= threshold:
                    results.append(SearchResult(
                        name=match_name,
                        type='interface',
                        namespace='ProcessNet',
                        score=score
                    ))

        # Sort by score and remove duplicates
        seen = set()
        unique_results = []
        for r in sorted(results, key=lambda x: x.score, reverse=True):
            key = (r.name.lower(), r.type)
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        return unique_results[:limit]

    def _search_substring(self, query: str, limit: int = 10) -> list:
        """Fallback substring search when rapidfuzz is not available."""
        results = []
        query_lower = query.lower()

        for method_name in self._method_names:
            if query_lower in method_name:
                method_results = self.find_method(method_name)
                results.extend(method_results)

        for iface_name in self._interface_names:
            if query_lower in iface_name:
                results.append(SearchResult(
                    name=iface_name,
                    type='interface',
                    namespace='ProcessNet'
                ))

        return results[:limit]

    def search_by_description(self, keywords: str) -> list:
        """
        Search in method descriptions and code examples.

        Args:
            keywords: Space-separated keywords to search for

        Returns:
            List of matching SearchResult objects
        """
        results = []
        keyword_list = keywords.lower().split()

        for ns_name, ns_data in self.kb.get('namespaces', {}).items():
            # Search in methods
            for method in ns_data.get('standalone_methods', []):
                desc = method.get('description', '').lower()
                if all(kw in desc for kw in keyword_list):
                    results.append(SearchResult(
                        name=method['name'],
                        type='method',
                        namespace=ns_name,
                        signature=method.get('signature', ''),
                        description=method.get('description', ''),
                        source_file=method.get('source_file', '')
                    ))

            # Search in examples
            for example in ns_data.get('examples', []):
                code = example.get('code', '').lower()
                if all(kw in code for kw in keyword_list):
                    results.append(SearchResult(
                        name='Code Example',
                        type='example',
                        namespace=ns_name,
                        code=example.get('code', '')[:500],
                        source_file=example.get('source_file', '')
                    ))

        return results

    def list_namespace_contents(self, namespace: str) -> dict:
        """
        List all contents of a namespace.

        Args:
            namespace: Namespace name

        Returns:
            Dictionary with namespace contents
        """
        ns_data = self.kb.get('namespaces', {}).get(namespace, {})

        return {
            'name': namespace,
            'full_name': ns_data.get('full_name', namespace),
            'description': ns_data.get('description', ''),
            'classes': [c['name'] for c in ns_data.get('classes', [])],
            'methods': [m['name'] for m in ns_data.get('standalone_methods', [])],
            'examples_count': len(ns_data.get('examples', [])),
            'files': ns_data.get('files', [])
        }

    def list_namespaces(self) -> list:
        """List all available namespaces."""
        return list(self.kb.get('namespaces', {}).keys())

    def find_examples(self, keyword: Optional[str] = None, limit: int = 10) -> list:
        """
        Find code examples.

        Args:
            keyword: Optional keyword filter
            limit: Maximum results

        Returns:
            List of code examples
        """
        results = []

        for ns_name, ns_data in self.kb.get('namespaces', {}).items():
            for example in ns_data.get('examples', []):
                code = example.get('code', '')

                if keyword is None or keyword.lower() in code.lower():
                    results.append({
                        'namespace': ns_name,
                        'code': code,
                        'language': example.get('language', 'csharp'),
                        'source_file': example.get('source_file', '')
                    })

                if len(results) >= limit:
                    break

        return results

    def get_statistics(self) -> dict:
        """Get knowledge base statistics."""
        total_methods = sum(
            len(ns.get('standalone_methods', []))
            for ns in self.kb.get('namespaces', {}).values()
        )
        total_examples = sum(
            len(ns.get('examples', []))
            for ns in self.kb.get('namespaces', {}).values()
        )
        total_classes = sum(
            len(ns.get('classes', []))
            for ns in self.kb.get('namespaces', {}).values()
        )

        return {
            'namespaces': len(self.kb.get('namespaces', {})),
            'methods': total_methods,
            'classes': total_classes,
            'examples': total_examples,
            'interfaces': len(self._interface_names),
            'extraction_date': self.kb.get('metadata', {}).get('extraction_date', ''),
            'files_processed': self.kb.get('metadata', {}).get('total_files_processed', 0)
        }


def format_result(result: SearchResult) -> str:
    """Format a search result for console output."""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"Name: {result.name}")
    output.append(f"Type: {result.type}")
    output.append(f"Namespace: {result.namespace}")

    if result.signature:
        output.append(f"Signature: {result.signature}")

    if result.description:
        output.append(f"Description: {result.description[:200]}")

    if result.code:
        output.append(f"Code Preview:")
        output.append(f"  {result.code[:300]}...")

    if result.source_file:
        output.append(f"Source: {result.source_file}")

    if result.score < 100:
        output.append(f"Match Score: {result.score:.1f}%")

    return '\n'.join(output)


def interactive_mode(kb: ProcessNetKnowledge):
    """Run interactive query mode."""
    print("\n" + "="*60)
    print("ProcessNet Knowledge Query Interface")
    print("="*60)

    stats = kb.get_statistics()
    print(f"\nLoaded knowledge base:")
    print(f"  Namespaces: {stats['namespaces']}")
    print(f"  Methods: {stats['methods']}")
    print(f"  Examples: {stats['examples']}")
    print(f"  Interfaces: {stats['interfaces']}")

    print("\nCommands:")
    print("  search <query>     - Fuzzy search for methods/interfaces")
    print("  find <method>      - Exact method lookup")
    print("  desc <keywords>    - Search by description")
    print("  list <namespace>   - List namespace contents")
    print("  namespaces         - List all namespaces")
    print("  examples [keyword] - Find code examples")
    print("  stats              - Show statistics")
    print("  help               - Show this help")
    print("  quit               - Exit")

    while True:
        try:
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        command = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if command in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break

        elif command == 'search':
            if not arg:
                print("Usage: search <query>")
                continue
            results = kb.search_method_fuzzy(arg)
            if results:
                for r in results:
                    print(format_result(r))
            else:
                print(f"No results found for '{arg}'")

        elif command == 'find':
            if not arg:
                print("Usage: find <method_name>")
                continue
            results = kb.find_method(arg)
            if results:
                for r in results:
                    print(format_result(r))
            else:
                print(f"Method '{arg}' not found")

        elif command == 'desc':
            if not arg:
                print("Usage: desc <keywords>")
                continue
            results = kb.search_by_description(arg)
            if results:
                for r in results[:10]:
                    print(format_result(r))
            else:
                print(f"No results found for keywords '{arg}'")

        elif command == 'list':
            if not arg:
                print("Usage: list <namespace>")
                continue
            contents = kb.list_namespace_contents(arg)
            print(f"\nNamespace: {contents['name']}")
            print(f"Full Name: {contents['full_name']}")
            print(f"Description: {contents['description']}")
            print(f"Methods ({len(contents['methods'])}):")
            for m in contents['methods'][:20]:
                print(f"  - {m}")
            if len(contents['methods']) > 20:
                print(f"  ... and {len(contents['methods'])-20} more")
            print(f"Examples: {contents['examples_count']}")

        elif command == 'namespaces':
            namespaces = kb.list_namespaces()
            print("\nAvailable Namespaces:")
            for ns in namespaces:
                print(f"  - {ns}")

        elif command == 'examples':
            results = kb.find_examples(arg if arg else None)
            print(f"\nFound {len(results)} examples:")
            for i, ex in enumerate(results[:5], 1):
                print(f"\n--- Example {i} ({ex['source_file']}) ---")
                print(ex['code'][:500])

        elif command == 'stats':
            stats = kb.get_statistics()
            print("\nKnowledge Base Statistics:")
            for key, value in stats.items():
                print(f"  {key}: {value}")

        elif command == 'help':
            print("\nCommands:")
            print("  search <query>     - Fuzzy search for methods/interfaces")
            print("  find <method>      - Exact method lookup")
            print("  desc <keywords>    - Search by description")
            print("  list <namespace>   - List namespace contents")
            print("  namespaces         - List all namespaces")
            print("  examples [keyword] - Find code examples")
            print("  stats              - Show statistics")
            print("  quit               - Exit")

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands")


def main():
    parser = argparse.ArgumentParser(
        description='Query ProcessNet API knowledge base'
    )
    parser.add_argument(
        '--kb', '-k',
        type=str,
        default='output/processnet-knowledge.json',
        help='Path to knowledge base JSON file'
    )
    parser.add_argument(
        '--search', '-s',
        type=str,
        help='Search query (fuzzy match)'
    )
    parser.add_argument(
        '--find', '-f',
        type=str,
        help='Find method by exact name'
    )
    parser.add_argument(
        '--examples', '-e',
        type=str,
        nargs='?',
        const='',
        help='Find code examples (optional keyword filter)'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    args = parser.parse_args()

    try:
        kb = ProcessNetKnowledge(args.kb)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Handle command-line queries
    if args.search:
        results = kb.search_method_fuzzy(args.search)
        if args.json:
            print(json.dumps([{
                'name': r.name,
                'type': r.type,
                'namespace': r.namespace,
                'signature': r.signature,
                'score': r.score
            } for r in results], indent=2))
        else:
            for r in results:
                print(format_result(r))

    elif args.find:
        results = kb.find_method(args.find)
        if args.json:
            print(json.dumps([{
                'name': r.name,
                'type': r.type,
                'namespace': r.namespace,
                'signature': r.signature,
                'description': r.description
            } for r in results], indent=2))
        else:
            for r in results:
                print(format_result(r))

    elif args.examples is not None:
        keyword = args.examples if args.examples else None
        results = kb.find_examples(keyword)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            for i, ex in enumerate(results, 1):
                print(f"\n--- Example {i} ({ex['source_file']}) ---")
                print(ex['code'][:1000])

    else:
        # Interactive mode
        interactive_mode(kb)


if __name__ == '__main__':
    main()
