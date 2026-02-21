#!/usr/bin/env python3
"""
Knowledge Base Consolidator - v7 Merger

Merges Python API, C#/VB API, and User Guides into unified KB.

Input:
  - output/processnet-knowledge-v6.json (Python API)
  - output/processnet-csharp-vb-api.json (C#/VB API)
  - output/processnet-userguide.json (User Guides)

Output:
  - output/processnet-knowledge-v7.json (Unified KB)
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


class KBConsolidator:
    """Merge multiple KBs into unified v7."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.python_kb = None
        self.csharp_vb_kb = None
        self.userguide_kb = None
        self.unified_kb = {}

    def load_python_kb(self, path: Path):
        """Load v6 Python KB."""
        logger.info(f"Loading Python KB from {path.name}")
        if not path.exists():
            raise FileNotFoundError(f"Python KB not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            self.python_kb = json.load(f)

        ns_count = len(self.python_kb.get('namespaces', {}))
        method_count = len(self.python_kb.get('method_index', {}))
        class_count = len(self.python_kb.get('class_index', {}))
        logger.info(f"  Loaded {ns_count} namespaces, {class_count} classes, {method_count} methods")

    def load_csharp_vb_kb(self, path: Path):
        """Load C#/VB KB from Phase 1."""
        logger.info(f"Loading C#/VB KB from {path.name}")
        if not path.exists():
            raise FileNotFoundError(f"C#/VB KB not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            self.csharp_vb_kb = json.load(f)

        ns_count = len(self.csharp_vb_kb.get('namespaces', {}))
        stats = self.csharp_vb_kb.get('statistics', {})
        # Calculate total members from statistics
        member_count = (
            stats.get('classes', 0) +
            stats.get('interfaces', 0) +
            stats.get('enums', 0) +
            stats.get('methods', 0) +
            stats.get('properties', 0) +
            stats.get('events', 0)
        )
        logger.info(f"  Loaded {ns_count} namespaces, {member_count} members")

    def load_userguide_kb(self, path: Path):
        """Load User Guide KB from Phases 2-3."""
        logger.info(f"Loading User Guide KB from {path.name}")
        if not path.exists():
            raise FileNotFoundError(f"User Guide KB not found: {path}")

        with open(path, 'r', encoding='utf-8') as f:
            self.userguide_kb = json.load(f)

        stats = self.userguide_kb.get('statistics', {})
        guide_count = stats.get('total_guides', 0)
        section_count = stats.get('total_sections', 0)
        word_count = stats.get('total_words', 0)
        logger.info(f"  Loaded {guide_count} guides, {section_count} sections, {word_count} words")

    def _ensure_index_entry(self, index: dict, key: str, original_name: str):
        """Create index entry if missing, track original case names."""
        if key not in index:
            index[key] = {'python': [], 'csharp_vb': [], 'original_names': []}
        if original_name and original_name not in index[key]['original_names']:
            index[key]['original_names'].append(original_name)

    def build_unified_index(self):
        """Create cross-API search indices with case-preserving keys."""
        logger.info("Building unified index...")

        methods_index = {}
        classes_index = {}
        interfaces_index = {}
        guide_index = {}

        # Index Python API
        logger.info("  Indexing Python API...")
        for ns_name, ns_data in self.python_kb.get('namespaces', {}).items():
            for cls in ns_data.get('classes', []):
                cls_name_orig = cls.get('name', '')
                cls_name = cls_name_orig.lower()
                if cls_name:
                    self._ensure_index_entry(classes_index, cls_name, cls_name_orig)
                    if ns_name not in classes_index[cls_name]['python']:
                        classes_index[cls_name]['python'].append(ns_name)

                for method in cls.get('methods', []):
                    method_name_orig = method.get('name', '')
                    method_name = method_name_orig.lower()
                    if method_name:
                        self._ensure_index_entry(methods_index, method_name, method_name_orig)
                        if ns_name not in methods_index[method_name]['python']:
                            methods_index[method_name]['python'].append(ns_name)

            # Index interfaces
            for interface in ns_data.get('interfaces', []):
                int_name_orig = interface.get('name', '')
                int_name = int_name_orig.lower()
                if int_name:
                    self._ensure_index_entry(interfaces_index, int_name, int_name_orig)
                    if ns_name not in interfaces_index[int_name]['python']:
                        interfaces_index[int_name]['python'].append(ns_name)

        # Index C#/VB API
        logger.info("  Indexing C#/VB API...")
        for ns_name, ns_data in self.csharp_vb_kb.get('namespaces', {}).items():
            for member in ns_data.get('members', []):
                name_orig = member.get('name', '')
                name = name_orig.lower()
                entity_type = member.get('entity_type', '')

                if entity_type in ('class', 'interface', 'enum', 'struct'):
                    self._ensure_index_entry(classes_index, name, name_orig)
                    if ns_name not in classes_index[name]['csharp_vb']:
                        classes_index[name]['csharp_vb'].append(ns_name)

                elif entity_type == 'method':
                    self._ensure_index_entry(methods_index, name, name_orig)
                    if ns_name not in methods_index[name]['csharp_vb']:
                        methods_index[name]['csharp_vb'].append(ns_name)

                if entity_type == 'interface':
                    self._ensure_index_entry(interfaces_index, name, name_orig)
                    if ns_name not in interfaces_index[name]['csharp_vb']:
                        interfaces_index[name]['csharp_vb'].append(ns_name)

        # Index user guide sections
        logger.info("  Indexing user guides...")
        if self.userguide_kb:
            for guide in self.userguide_kb.get('word_guides', []):
                for section in guide.get('sections', []):
                    title_lower = section.get('title', '').lower()
                    section_id = section.get('section_id', '')

                    # Index by words in title (>3 chars)
                    words = title_lower.split()
                    for word in words:
                        # Remove common words and short words
                        if len(word) > 3 and word not in ['with', 'from', 'that', 'this', 'about']:
                            if word not in guide_index:
                                guide_index[word] = []
                            if section_id and section_id not in guide_index[word]:
                                guide_index[word].append(section_id)

        self.unified_kb['unified_index'] = {
            'methods': methods_index,
            'classes': classes_index,
            'interfaces': interfaces_index,
            'guide_sections': guide_index
        }

        logger.info(f"  Indexed {len(methods_index)} unique methods")
        logger.info(f"  Indexed {len(classes_index)} unique classes/types")
        logger.info(f"  Indexed {len(interfaces_index)} unique interfaces")
        logger.info(f"  Indexed {len(guide_index)} guide keywords")

    def _build_metadata(self) -> Dict[str, Any]:
        """Create v7 metadata."""
        python_stats = self.python_kb.get('metadata', {})
        csharp_stats = self.csharp_vb_kb.get('statistics', {})
        guide_stats = self.userguide_kb.get('statistics', {})

        # Calculate statistics
        python_classes = len(self.python_kb.get('class_index', {}))
        python_methods = len(self.python_kb.get('method_index', {}))
        # Calculate total C#/VB members from all entity types
        csharp_vb_members = (
            csharp_stats.get('classes', 0) +
            csharp_stats.get('interfaces', 0) +
            csharp_stats.get('enums', 0) +
            csharp_stats.get('methods', 0) +
            csharp_stats.get('properties', 0) +
            csharp_stats.get('events', 0)
        )
        csharp_vb_namespaces = len(self.csharp_vb_kb.get('namespaces', {}))

        guide_word_count = guide_stats.get('total_words', 0)
        guide_sections = guide_stats.get('total_sections', 0)

        total_searchable = python_methods + csharp_vb_members + guide_sections

        return {
            'source': 'RecurDyn ProcessNet API',
            'version': 'v7',
            'extraction_date': datetime.now().isoformat(),
            'content_sources': {
                'python_api': 'processnet-knowledge-v6.json',
                'csharp_vb_api': 'processnet-csharp-vb-api.json',
                'user_guides': 'processnet-userguide.json'
            },
            'statistics': {
                'python_classes': python_classes,
                'python_methods': python_methods,
                'csharp_vb_members': csharp_vb_members,
                'csharp_vb_namespaces': csharp_vb_namespaces,
                'guide_word_count': guide_word_count,
                'guide_sections': guide_sections,
                'total_searchable_items': total_searchable
            },
            'source_metadata': {
                'python_api': python_stats,
                'csharp_vb_api': self.csharp_vb_kb.get('metadata', {}),
                'user_guides': self.userguide_kb.get('metadata', {})
            }
        }

    def merge_all(self):
        """Combine all KBs into unified structure."""
        logger.info("Merging all knowledge bases...")

        self.unified_kb = {
            'metadata': self._build_metadata(),
            'python_api': {
                'namespaces': self.python_kb.get('namespaces', {}),
                'method_index': self.python_kb.get('method_index', {}),
                'class_index': self.python_kb.get('class_index', {}),
                'interface_index': self.python_kb.get('interface_index', {})
            },
            'csharp_vb_api': {
                'namespaces': self.csharp_vb_kb.get('namespaces', {}),
                'entity_index': self.csharp_vb_kb.get('entity_index', {}),
                'statistics': self.csharp_vb_kb.get('statistics', {})
            },
            'user_guides': {
                'word_guides': self.userguide_kb.get('word_guides', []),
                'statistics': self.userguide_kb.get('statistics', {})
            }
        }

        # Build unified index last
        self.build_unified_index()

        logger.info("Merge completed successfully")

    def validate_structure(self) -> bool:
        """Verify all required keys present."""
        logger.info("Validating unified KB structure...")

        required_keys = [
            'metadata',
            'python_api',
            'csharp_vb_api',
            'user_guides',
            'unified_index'
        ]

        for key in required_keys:
            if key not in self.unified_kb:
                logger.error(f"Missing required key: {key}")
                return False

        # Verify nested structures
        if 'namespaces' not in self.unified_kb['python_api']:
            logger.error("Missing python_api.namespaces")
            return False

        if 'namespaces' not in self.unified_kb['csharp_vb_api']:
            logger.error("Missing csharp_vb_api.namespaces")
            return False

        if 'word_guides' not in self.unified_kb['user_guides']:
            logger.error("Missing user_guides.word_guides")
            return False

        # Verify indices have content
        if not self.unified_kb['unified_index']['methods']:
            logger.warning("Method index is empty")

        if not self.unified_kb['unified_index']['classes']:
            logger.warning("Class index is empty")

        # Verify backward compatibility: python_api should have same structure
        if not self.unified_kb['python_api']['method_index']:
            logger.warning("Python API method_index is empty - backward compatibility may be affected")

        logger.info("Structure validation passed")
        return True

    def save_v7_kb(self):
        """Write unified KB to JSON."""
        logger.info(f"Saving v7 KB to {self.output_path.name}")

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_path, 'w', encoding='utf-8') as f:
            json.dump(self.unified_kb, f, indent=2, ensure_ascii=False)

        size_mb = self.output_path.stat().st_size / (1024 * 1024)
        logger.info(f"v7 KB saved: {size_mb:.2f} MB")

        # Log statistics
        stats = self.unified_kb['metadata']['statistics']
        logger.info("=" * 60)
        logger.info("v7 Knowledge Base Statistics:")
        logger.info(f"  Python API: {stats['python_classes']} classes, {stats['python_methods']} methods")
        logger.info(f"  C#/VB API: {stats['csharp_vb_members']} members in {stats['csharp_vb_namespaces']} namespaces")
        logger.info(f"  User Guides: {stats['guide_sections']} sections, {stats['guide_word_count']} words")
        logger.info(f"  Total searchable items: {stats['total_searchable_items']}")
        logger.info("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Consolidate Python API, C#/VB API, and User Guides into unified v7 KB'
    )
    parser.add_argument(
        '--python-kb',
        type=Path,
        default=Path('output/processnet-knowledge-v6.json'),
        help='Path to Python API KB (v6)'
    )
    parser.add_argument(
        '--csharp-vb-kb',
        type=Path,
        default=Path('output/processnet-csharp-vb-api.json'),
        help='Path to C#/VB API KB'
    )
    parser.add_argument(
        '--userguide-kb',
        type=Path,
        default=Path('output/processnet-userguide.json'),
        help='Path to User Guide KB'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('output/processnet-knowledge-v7.json'),
        help='Output path for unified v7 KB'
    )

    args = parser.parse_args()

    try:
        consolidator = KBConsolidator(args.output)

        # Load all KBs
        consolidator.load_python_kb(args.python_kb)
        consolidator.load_csharp_vb_kb(args.csharp_vb_kb)
        consolidator.load_userguide_kb(args.userguide_kb)

        # Merge and validate
        consolidator.merge_all()

        if not consolidator.validate_structure():
            logger.error("Validation failed")
            return 1

        # Save output
        consolidator.save_v7_kb()

        logger.info("KB consolidation completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Error during consolidation: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
