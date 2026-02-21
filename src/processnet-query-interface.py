#!/usr/bin/env python3
"""
ProcessNet Knowledge Base Query Interface

Provides search and query functionality for the ProcessNet API knowledge base (v7+).
Supports Python API, C#/VB API, and User Guides with language filtering.

Usage:
    python processnet-query-interface.py [--search QUERY] [--language LANG] [--kb PATH]
    python processnet-query-interface.py  # Interactive mode
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
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
    type: str  # 'method', 'class', 'interface', 'example', 'member', 'guide'
    namespace: str
    signature: str = ""
    description: str = ""
    code: str = ""
    source_file: str = ""
    score: float = 100.0
    language: str = "python"  # python, csharp, vb
    section: str = "python_api"  # python_api, csharp_vb_api, user_guides


class ProcessNetKnowledge:
    """Query interface for ProcessNet knowledge base (v7 multi-section)."""

    def __init__(self, kb_path: str = "output/processnet-knowledge-v7.json"):
        self.kb_path = Path(kb_path)
        self.kb = None
        self._python_method_names = []
        self._python_interface_names = []
        self._csharp_vb_member_names = []
        self._guide_keywords = []
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
        """Build in-memory search indices for all sections."""
        # Check if this is v7+ (multi-section) or older format
        if 'python_api' in self.kb:
            # v7+ format with sections
            python_api = self.kb.get('python_api', {})
            self._python_method_names = list(python_api.get('method_index', {}).keys())
            self._python_interface_names = list(python_api.get('interface_index', {}).keys())

            csharp_vb_api = self.kb.get('csharp_vb_api', {})
            self._csharp_vb_member_names = list(csharp_vb_api.get('entity_index', {}).keys())

            user_guides = self.kb.get('user_guides', {})
            if isinstance(user_guides, dict):
                self._guide_keywords = list(user_guides.keys())
        else:
            # Backward compatibility: v6 and earlier format (flat structure)
            self._python_method_names = list(self.kb.get('method_index', {}).keys())
            self._python_interface_names = list(self.kb.get('interface_index', {}).keys())

    def _get_all_methods_from_classes(self, ns_data: dict) -> list:
        """Aggregate methods from all classes in a namespace."""
        all_methods = []
        for cls in ns_data.get('classes', []):
            cls_name = cls.get('name', '')
            for method in cls.get('methods', []):
                # Add class context to method
                method_with_class = dict(method)
                method_with_class['parent_class'] = cls_name
                all_methods.append(method_with_class)
        return all_methods

    def find_method(self, method_name: str, namespace: Optional[str] = None, language: str = "all") -> list:
        """
        Find method by exact name match (case-insensitive).

        Args:
            method_name: Method name to search for
            namespace: Optional namespace filter
            language: Filter by language (python, csharp, vb, all)

        Returns:
            List of matching SearchResult objects
        """
        results = []
        method_lower = method_name.lower()

        # Detect KB format
        is_v7_format = 'python_api' in self.kb

        if is_v7_format:
            # v7+ multi-section format
            # Search Python API
            if language in ("all", "python"):
                python_api = self.kb.get('python_api', {})
                if method_lower in python_api.get('method_index', {}):
                    namespaces = python_api['method_index'][method_lower]
                    for ns in namespaces:
                        if namespace and ns.lower() != namespace.lower():
                            continue

                        ns_data = python_api.get('namespaces', {}).get(ns, {})
                        all_methods = self._get_all_methods_from_classes(ns_data)
                        for method in all_methods:
                            if method['name'].lower() == method_lower:
                                results.append(SearchResult(
                                    name=method['name'],
                                    type='method',
                                    namespace=ns,
                                    signature=method.get('signature', ''),
                                    description=method.get('description', ''),
                                    source_file=method.get('source_file', ''),
                                    language='python',
                                    section='python_api'
                                ))

            # Search C#/VB API by entity index
            if language in ("all", "csharp", "vb"):
                csharp_vb_api = self.kb.get('csharp_vb_api', {})
                entity_index = csharp_vb_api.get('entity_index', {})

                if method_lower in entity_index:
                    entity_namespaces = entity_index[method_lower]
                    for ns_name in entity_namespaces:
                        if namespace and ns_name.lower() != namespace.lower():
                            continue

                        ns_data = csharp_vb_api.get('namespaces', {}).get(ns_name, {})
                        members = ns_data.get('members', [])

                        for member in members:
                            if member.get('name', '').lower() == method_lower:
                                results.append(SearchResult(
                                    name=member['name'],
                                    type=member.get('entity_type', 'member'),
                                    namespace=ns_name,
                                    signature=member.get('syntax_csharp', member.get('syntax_vb', '')),
                                    description=member.get('description', ''),
                                    source_file=member.get('source_file', ''),
                                    language='csharp',
                                    section='csharp_vb_api'
                                ))
        else:
            # Backward compat: v6 and earlier format
            if language in ("all", "python"):
                if method_lower in self.kb.get('method_index', {}):
                    namespaces = self.kb['method_index'][method_lower]
                    for ns in namespaces:
                        if namespace and ns.lower() != namespace.lower():
                            continue

                        ns_data = self.kb['namespaces'].get(ns, {})
                        all_methods = self._get_all_methods_from_classes(ns_data)
                        for method in all_methods:
                            if method['name'].lower() == method_lower:
                                results.append(SearchResult(
                                    name=method['name'],
                                    type='method',
                                    namespace=ns,
                                    signature=method.get('signature', ''),
                                    description=method.get('description', ''),
                                    source_file=method.get('source_file', ''),
                                    language='python',
                                    section='python_api'
                                ))

        return results

    def search_method_fuzzy(self, query: str, threshold: float = 60.0, limit: int = 10, language: str = "all") -> list:
        """
        Search for methods using fuzzy string matching across all sections.

        Args:
            query: Search query
            threshold: Minimum similarity score (0-100)
            limit: Maximum results to return
            language: Filter by language (python, csharp, vb, all)

        Returns:
            List of matching SearchResult objects
        """
        if not FUZZY_AVAILABLE:
            return self._search_substring(query, limit, language)

        results = []

        # Search Python API methods
        if language in ("all", "python"):
            if self._python_method_names:
                matches = process.extract(
                    query.lower(),
                    self._python_method_names,
                    scorer=fuzz.WRatio,
                    limit=limit
                )

                for match_name, score, _ in matches:
                    if score >= threshold:
                        method_results = self.find_method(match_name, language="python")
                        for r in method_results:
                            r.score = score
                            results.append(r)

            # Search Python API interfaces
            if self._python_interface_names:
                matches = process.extract(
                    query.lower(),
                    self._python_interface_names,
                    scorer=fuzz.WRatio,
                    limit=limit
                )

                for match_name, score, _ in matches:
                    if score >= threshold:
                        results.append(SearchResult(
                            name=match_name,
                            type='interface',
                            namespace='ProcessNet',
                            score=score,
                            language='python',
                            section='python_api'
                        ))

        # Search C#/VB API members
        if language in ("all", "csharp", "vb"):
            if self._csharp_vb_member_names:
                matches = process.extract(
                    query.lower(),
                    self._csharp_vb_member_names,
                    scorer=fuzz.WRatio,
                    limit=limit
                )

                for match_name, score, _ in matches:
                    if score >= threshold:
                        member_results = self.find_method(match_name, language="csharp" if language in ("csharp", "all") else "vb")
                        for r in member_results:
                            r.score = score
                            results.append(r)

        # Sort by score and remove duplicates, prioritizing high-score matches
        seen = set()
        unique_results = []
        for r in sorted(results, key=lambda x: (-x.score, x.name.lower())):
            key = (r.name.lower(), r.type, r.language)
            if key not in seen:
                seen.add(key)
                unique_results.append(r)

        return unique_results[:limit]

    def _search_substring(self, query: str, limit: int = 10, language: str = "all") -> list:
        """Fallback substring search when rapidfuzz is not available."""
        results = []
        query_lower = query.lower()

        # Python API
        if language in ("all", "python"):
            for method_name in self._python_method_names:
                if query_lower in method_name:
                    method_results = self.find_method(method_name, language="python")
                    results.extend(method_results)

            for iface_name in self._python_interface_names:
                if query_lower in iface_name:
                    results.append(SearchResult(
                        name=iface_name,
                        type='interface',
                        namespace='ProcessNet',
                        language='python',
                        section='python_api'
                    ))

        # C#/VB API
        if language in ("all", "csharp", "vb"):
            for member_name in self._csharp_vb_member_names:
                if query_lower in member_name:
                    member_results = self.find_method(member_name, language="csharp")
                    results.extend(member_results)

        return results[:limit]

    def search_by_description(self, keywords: str, language: str = "all") -> list:
        """
        Search in method descriptions across all sections.

        Args:
            keywords: Space-separated keywords to search for
            language: Filter by language (python, csharp, vb, all)

        Returns:
            List of matching SearchResult objects
        """
        results = []
        keyword_list = keywords.lower().split()

        # Search Python API
        if language in ("all", "python"):
            python_api = self.kb.get('python_api', {})
            for ns_name, ns_data in python_api.get('namespaces', {}).items():
                all_methods = self._get_all_methods_from_classes(ns_data)
                for method in all_methods:
                    desc = method.get('description', '').lower()
                    if all(kw in desc for kw in keyword_list):
                        results.append(SearchResult(
                            name=method['name'],
                            type='method',
                            namespace=ns_name,
                            signature=method.get('signature', ''),
                            description=method.get('description', ''),
                            source_file=method.get('source_file', ''),
                            language='python',
                            section='python_api'
                        ))

        # Search C#/VB API
        if language in ("all", "csharp", "vb"):
            csharp_vb_api = self.kb.get('csharp_vb_api', {})
            for ns_name, ns_data in csharp_vb_api.get('namespaces', {}).items():
                for entity in ns_data.get('entities', []):
                    entity_lang = entity.get('language', 'csharp').lower()
                    if language != "all" and entity_lang not in (language, language[:-1]):
                        continue

                    desc = entity.get('description', '').lower()
                    if all(kw in desc for kw in keyword_list):
                        results.append(SearchResult(
                            name=entity['name'],
                            type=entity.get('type', 'member'),
                            namespace=ns_name,
                            signature=entity.get('signature', ''),
                            description=entity.get('description', ''),
                            source_file=entity.get('source_file', ''),
                            language=entity_lang,
                            section='csharp_vb_api'
                        ))

        return results

    def list_namespace_contents(self, namespace: str, language: str = "all") -> dict:
        """
        List all contents of a namespace across sections.

        Args:
            namespace: Namespace name
            language: Filter by language (python, csharp, vb, all)

        Returns:
            Dictionary with namespace contents
        """
        result = {'name': namespace, 'sections': {}}

        # Python API
        if language in ("all", "python"):
            python_api = self.kb.get('python_api', {})
            ns_data = python_api.get('namespaces', {}).get(namespace, {})
            if ns_data:
                result['sections']['python_api'] = {
                    'full_name': ns_data.get('full_name', namespace),
                    'description': ns_data.get('description', ''),
                    'classes': [c['name'] for c in ns_data.get('classes', [])],
                    'methods': [m['name'] for m in self._get_all_methods_from_classes(ns_data)],
                    'files': ns_data.get('files', [])
                }

        # C#/VB API
        if language in ("all", "csharp", "vb"):
            csharp_vb_api = self.kb.get('csharp_vb_api', {})
            ns_data = csharp_vb_api.get('namespaces', {}).get(namespace, {})
            if ns_data:
                entities = ns_data.get('entities', [])
                if language != "all":
                    entities = [e for e in entities if e.get('language', '').lower() in (language, language[:-1])]

                result['sections']['csharp_vb_api'] = {
                    'full_name': ns_data.get('full_name', namespace),
                    'description': ns_data.get('description', ''),
                    'entity_count': len(entities),
                    'entities': [e['name'] for e in entities[:20]]
                }

        return result

    def list_namespaces(self, language: str = "all") -> list:
        """
        List all available namespaces.

        Args:
            language: Filter by language (python, csharp, vb, all)

        Returns:
            List of namespace names
        """
        namespaces = set()

        if language in ("all", "python"):
            python_api = self.kb.get('python_api', {})
            namespaces.update(python_api.get('namespaces', {}).keys())

        if language in ("all", "csharp", "vb"):
            csharp_vb_api = self.kb.get('csharp_vb_api', {})
            namespaces.update(csharp_vb_api.get('namespaces', {}).keys())

        return sorted(list(namespaces))

    def find_examples(self, keyword: Optional[str] = None, limit: int = 10, language: str = "all") -> list:
        """
        Find code examples from Python API.

        Args:
            keyword: Optional keyword filter
            limit: Maximum results
            language: Filter by language (python, csharp, vb, all) - only python examples in v7

        Returns:
            List of code examples
        """
        results = []

        # Only Python API has examples in current KB structure
        if language in ("all", "python"):
            python_api = self.kb.get('python_api', {})
            for ns_name, ns_data in python_api.get('namespaces', {}).items():
                for example in ns_data.get('examples', []):
                    code = example.get('code', '')

                    if keyword is None or keyword.lower() in code.lower():
                        results.append({
                            'namespace': ns_name,
                            'code': code,
                            'language': 'python',
                            'source_file': example.get('source_file', ''),
                            'section': 'python_api'
                        })

                    if len(results) >= limit:
                        return results

        return results

    def get_statistics(self) -> dict:
        """Get knowledge base statistics for all sections."""
        # Python API stats
        python_api = self.kb.get('python_api', {})
        python_methods = sum(
            len(self._get_all_methods_from_classes(ns))
            for ns in python_api.get('namespaces', {}).values()
        )
        python_examples = sum(
            len(ns.get('examples', []))
            for ns in python_api.get('namespaces', {}).values()
        )
        python_classes = sum(
            len(ns.get('classes', []))
            for ns in python_api.get('namespaces', {}).values()
        )

        # C#/VB API stats - members are in 'members' key, not 'entities'
        csharp_vb_api = self.kb.get('csharp_vb_api', {})
        csharp_vb_members = sum(
            len(ns.get('members', []))
            for ns in csharp_vb_api.get('namespaces', {}).values()
        )

        metadata = self.kb.get('metadata', {})
        stats = metadata.get('statistics', {})

        return {
            'version': metadata.get('version', 'unknown'),
            'extraction_date': metadata.get('extraction_date', ''),
            'sections': {
                'python_api': {
                    'namespaces': len(python_api.get('namespaces', {})),
                    'classes': python_classes,
                    'methods': python_methods,
                    'interfaces': len(self._python_interface_names),
                    'examples': python_examples,
                    'files_processed': metadata.get('source_metadata', {}).get('python_api', {}).get('total_files_processed', 0)
                },
                'csharp_vb_api': {
                    'namespaces': len(csharp_vb_api.get('namespaces', {})),
                    'members': csharp_vb_members,
                    'files_processed': metadata.get('source_metadata', {}).get('csharp_vb_api', {}).get('total_files_processed', 0)
                },
                'user_guides': {
                    'sections': stats.get('guide_sections', 0),
                    'word_count': stats.get('guide_word_count', 0)
                }
            },
            'total_searchable_items': stats.get('total_searchable_items', 0)
        }


def format_result(result: SearchResult) -> str:
    """Format a search result for console output."""
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"Name: {result.name}")
    output.append(f"Type: {result.type}")
    output.append(f"Language: {result.language.upper()}")
    output.append(f"Section: {result.section}")
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
    print("ProcessNet Knowledge Query Interface (v7)")
    print("="*60)

    stats = kb.get_statistics()
    print(f"\nLoaded knowledge base (v{stats.get('version', '?')}):")
    print(f"  Total searchable items: {stats.get('total_searchable_items', 0)}")
    py_stats = stats.get('sections', {}).get('python_api', {})
    cs_stats = stats.get('sections', {}).get('csharp_vb_api', {})
    print(f"  Python API: {py_stats.get('methods', 0)} methods, {py_stats.get('classes', 0)} classes")
    print(f"  C#/VB API: {cs_stats.get('members', 0)} members")

    print("\nCommands:")
    print("  search <query> [--lang LANG]  - Fuzzy search (python|csharp|vb|all)")
    print("  find <method> [--lang LANG]   - Exact method lookup")
    print("  desc <keywords> [--lang LANG] - Search by description")
    print("  list <namespace> [--lang LANG]- List namespace contents")
    print("  namespaces [--lang LANG]      - List all namespaces")
    print("  examples [keyword]            - Find code examples")
    print("  stats                         - Show statistics")
    print("  help                          - Show this help")
    print("  quit                          - Exit")

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
                print("Usage: search <query> [--lang LANG]")
                continue
            # Parse optional language filter
            lang = "all"
            if "--lang" in arg:
                parts = arg.split("--lang")
                query = parts[0].strip()
                lang = parts[1].strip() if len(parts) > 1 else "all"
            else:
                query = arg
            results = kb.search_method_fuzzy(query, language=lang)
            if results:
                print(f"\nFound {len(results)} results for '{query}' ({lang}):")
                for r in results:
                    print(format_result(r))
            else:
                print(f"No results found for '{query}'")

        elif command == 'find':
            if not arg:
                print("Usage: find <method_name> [--lang LANG]")
                continue
            lang = "all"
            if "--lang" in arg:
                parts = arg.split("--lang")
                method_name = parts[0].strip()
                lang = parts[1].strip() if len(parts) > 1 else "all"
            else:
                method_name = arg
            results = kb.find_method(method_name, language=lang)
            if results:
                print(f"\nFound {len(results)} results for '{method_name}':")
                for r in results:
                    print(format_result(r))
            else:
                print(f"'{method_name}' not found")

        elif command == 'desc':
            if not arg:
                print("Usage: desc <keywords> [--lang LANG]")
                continue
            lang = "all"
            if "--lang" in arg:
                parts = arg.split("--lang")
                keywords = parts[0].strip()
                lang = parts[1].strip() if len(parts) > 1 else "all"
            else:
                keywords = arg
            results = kb.search_by_description(keywords, language=lang)
            if results:
                print(f"\nFound {len(results)} results:")
                for r in results[:10]:
                    print(format_result(r))
            else:
                print(f"No results found for keywords '{keywords}'")

        elif command == 'list':
            if not arg:
                print("Usage: list <namespace> [--lang LANG]")
                continue
            lang = "all"
            if "--lang" in arg:
                parts = arg.split("--lang")
                ns_name = parts[0].strip()
                lang = parts[1].strip() if len(parts) > 1 else "all"
            else:
                ns_name = arg
            contents = kb.list_namespace_contents(ns_name, language=lang)
            print(f"\nNamespace: {contents['name']}")
            for section, details in contents.get('sections', {}).items():
                print(f"\n  [{section}]")
                if 'full_name' in details:
                    print(f"    Full Name: {details['full_name']}")
                if 'description' in details:
                    print(f"    Description: {details['description']}")
                if 'methods' in details:
                    methods = details['methods']
                    print(f"    Methods ({len(methods)}):")
                    for m in methods[:10]:
                        print(f"      - {m}")
                    if len(methods) > 10:
                        print(f"      ... and {len(methods)-10} more")
                if 'entity_count' in details:
                    print(f"    Members: {details['entity_count']}")

        elif command == 'namespaces':
            lang = "all"
            if arg and "--lang" in arg:
                lang = arg.split("--lang")[1].strip()
            namespaces = kb.list_namespaces(language=lang)
            print(f"\nAvailable Namespaces ({lang}):")
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
            print("  search <query> [--lang LANG]      - Fuzzy search")
            print("  find <method> [--lang LANG]       - Exact method lookup")
            print("  desc <keywords> [--lang LANG]     - Search by description")
            print("  list <namespace> [--lang LANG]    - List namespace contents")
            print("  namespaces [--lang LANG]          - List all namespaces")
            print("  examples [keyword]                - Find code examples")
            print("  stats                             - Show statistics")
            print("  quit                              - Exit")
            print("\nLanguage filters: python, csharp, vb, all (default: all)")

        else:
            print(f"Unknown command: {command}")
            print("Type 'help' for available commands")


def main():
    parser = argparse.ArgumentParser(
        description='Query ProcessNet API knowledge base (v7+)',
        epilog='Languages: python, csharp, vb, all (default)'
    )
    parser.add_argument(
        '--kb', '-k',
        type=str,
        default='output/processnet-knowledge-v7.json',
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
        '--language', '-l',
        type=str,
        default='all',
        choices=['python', 'csharp', 'vb', 'all'],
        help='Filter by language (default: all)'
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
        results = kb.search_method_fuzzy(args.search, language=args.language)
        if args.json:
            print(json.dumps([{
                'name': r.name,
                'type': r.type,
                'namespace': r.namespace,
                'signature': r.signature,
                'language': r.language,
                'section': r.section,
                'score': r.score
            } for r in results], indent=2))
        else:
            print(f"Search results for '{args.search}' ({args.language}):")
            for r in results:
                print(format_result(r))

    elif args.find:
        results = kb.find_method(args.find, language=args.language)
        if args.json:
            print(json.dumps([{
                'name': r.name,
                'type': r.type,
                'namespace': r.namespace,
                'signature': r.signature,
                'language': r.language,
                'section': r.section,
                'description': r.description
            } for r in results], indent=2))
        else:
            print(f"Lookup results for '{args.find}' ({args.language}):")
            for r in results:
                print(format_result(r))

    elif args.examples is not None:
        keyword = args.examples if args.examples else None
        results = kb.find_examples(keyword, language=args.language)
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
