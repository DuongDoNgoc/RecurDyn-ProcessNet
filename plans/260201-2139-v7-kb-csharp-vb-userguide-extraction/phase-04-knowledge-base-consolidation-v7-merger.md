# Phase 4: Knowledge Base Consolidation - v7 Merger

## Context

- **Plan:** [v7 KB: C#/VB API + User Guide Extraction](plan.md)
- **Date:** 2026-02-01
- **Status:** Completed (2026-02-21)
- **Effort:** 1.5h
- **Dependencies:** Phase 1, Phase 2, Phase 3

## Overview

Merge all extracted content into a unified v7 knowledge base:
1. **Python API** (existing v6): 1,830 classes, 6,773 methods
2. **C#/VB API** (Phase 1): ~21,000 API members
3. **User Guides** (Phases 2-3): 34 guide files

Output: `output/processnet-knowledge-v7.json`

## Key Insights

### Input Sources

| Source | File | Content |
|--------|------|---------|
| Python API | `output/processnet-knowledge-v6.json` | Classes, methods, properties, examples |
| C#/VB API | `output/processnet-csharp-vb-api.json` | Dual-language API members |
| User Guides | `output/processnet-userguide.json` | Word + Sphinx guides |

### Namespace Mapping

Python and C#/VB APIs share the same logical namespaces but differ in implementation:

| Python Namespace | C#/VB Namespace |
|------------------|-----------------|
| ProcessNet | FunctionBay.RecurDyn.ProcessNet |
| ProcessNet.Geometry | FunctionBay.RecurDyn.ProcessNet.Geometry |
| - | FunctionBay.Post.ProcessNet (Post-processing only) |

### Merge Strategy

1. **Keep separate API sections:** Don't merge Python into C#/VB (different method signatures)
2. **Unified index:** Single method/class index spanning all APIs
3. **Add guides section:** New top-level key for user guides
4. **Preserve backward compatibility:** Existing query patterns work unchanged

## Requirements

1. Load Python KB (v6), C#/VB KB, and User Guide KB
2. Create unified JSON structure with all content
3. Build cross-API indices (method, class, interface)
4. Add user guides as separate section
5. Update metadata with v7 statistics
6. Maintain backward compatibility for query interface
7. Output: `output/processnet-knowledge-v7.json`

## Architecture

### v7 JSON Schema

```json
{
  "metadata": {
    "source": "RecurDyn ProcessNet API",
    "version": "v7",
    "extraction_date": "2026-02-01T...",
    "content_sources": {
      "python_api": "processnet-knowledge-v6.json",
      "csharp_vb_api": "processnet-csharp-vb-api.json",
      "user_guides": "processnet-userguide.json"
    },
    "statistics": {
      "python_classes": 1830,
      "python_methods": 6773,
      "csharp_vb_members": 21274,
      "guide_sections": 50,
      "total_searchable_items": 28000
    }
  },

  "python_api": {
    "namespaces": {
      "ProcessNet": { ... }
    }
  },

  "csharp_vb_api": {
    "namespaces": {
      "FunctionBay.RecurDyn.ProcessNet": { ... },
      "FunctionBay.Post.ProcessNet": { ... }
    }
  },

  "user_guides": {
    "word_guides": [ ... ],
    "sphinx_guides": { ... }
  },

  "unified_index": {
    "methods": {
      "save": {
        "python": ["ProcessNet"],
        "csharp_vb": ["FunctionBay.RecurDyn.ProcessNet"]
      }
    },
    "classes": { ... },
    "interfaces": { ... },
    "guide_sections": {
      "getting started": ["43.1", "word_guide_1_section_2"]
    }
  }
}
```

### KBConsolidator Class

```python
class KBConsolidator:
    """Merge multiple KBs into unified v7."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.python_kb = None
        self.csharp_vb_kb = None
        self.userguide_kb = None
        self.unified_kb = {}

    def load_python_kb(self, path: Path):
        """Load existing v6 Python KB."""

    def load_csharp_vb_kb(self, path: Path):
        """Load C#/VB API from Phase 1."""

    def load_userguide_kb(self, path: Path):
        """Load user guides from Phases 2-3."""

    def build_unified_index(self):
        """Create cross-API search indices."""

    def merge_metadata(self):
        """Combine statistics and source info."""

    def validate_structure(self) -> bool:
        """Verify all required keys present."""

    def save_v7_kb(self):
        """Write unified KB to JSON."""
```

## Implementation Steps

### Step 1: Create consolidator skeleton (15 min)

```python
# src/kb-consolidator-v7-merger.py
#!/usr/bin/env python3
"""
Knowledge Base Consolidator - v7 Merger

Merges Python API, C#/VB API, and User Guides into unified KB.
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)
```

### Step 2: Implement KB loaders (20 min)

```python
def load_python_kb(self, path: Path):
    """Load v6 Python KB."""
    logger.info(f"Loading Python KB from {path}")
    with open(path, 'r', encoding='utf-8') as f:
        self.python_kb = json.load(f)
    logger.info(f"Loaded {len(self.python_kb.get('namespaces', {}))} namespaces")

def load_csharp_vb_kb(self, path: Path):
    """Load C#/VB KB from Phase 1."""
    logger.info(f"Loading C#/VB KB from {path}")
    with open(path, 'r', encoding='utf-8') as f:
        self.csharp_vb_kb = json.load(f)
    logger.info(f"Loaded {len(self.csharp_vb_kb.get('namespaces', {}))} namespaces")

def load_userguide_kb(self, path: Path):
    """Load User Guide KB from Phases 2-3."""
    logger.info(f"Loading User Guide KB from {path}")
    with open(path, 'r', encoding='utf-8') as f:
        self.userguide_kb = json.load(f)
```

### Step 3: Implement unified index builder (30 min)

```python
def build_unified_index(self):
    """Create cross-API search indices."""
    methods_index = {}
    classes_index = {}
    interfaces_index = {}
    guide_index = {}

    # Index Python methods
    for ns_name, ns_data in self.python_kb.get('namespaces', {}).items():
        for cls in ns_data.get('classes', []):
            cls_name = cls.get('name', '').lower()
            if cls_name:
                if cls_name not in classes_index:
                    classes_index[cls_name] = {'python': [], 'csharp_vb': []}
                classes_index[cls_name]['python'].append(ns_name)

            for method in cls.get('methods', []):
                method_name = method.get('name', '').lower()
                if method_name:
                    if method_name not in methods_index:
                        methods_index[method_name] = {'python': [], 'csharp_vb': []}
                    if ns_name not in methods_index[method_name]['python']:
                        methods_index[method_name]['python'].append(ns_name)

    # Index C#/VB members
    for ns_name, ns_data in self.csharp_vb_kb.get('namespaces', {}).items():
        for member in ns_data.get('members', []):
            name = member.get('name', '').lower()
            entity_type = member.get('entity_type', '')

            if entity_type in ('class', 'interface'):
                if name not in classes_index:
                    classes_index[name] = {'python': [], 'csharp_vb': []}
                classes_index[name]['csharp_vb'].append(ns_name)

            elif entity_type == 'method':
                if name not in methods_index:
                    methods_index[name] = {'python': [], 'csharp_vb': []}
                if ns_name not in methods_index[name]['csharp_vb']:
                    methods_index[name]['csharp_vb'].append(ns_name)

    # Index user guide sections
    if self.userguide_kb:
        for guide in self.userguide_kb.get('word_guides', []):
            for section in guide.get('sections', []):
                title_lower = section.get('title', '').lower()
                words = title_lower.split()
                for word in words:
                    if len(word) > 3:
                        if word not in guide_index:
                            guide_index[word] = []
                        guide_index[word].append(section.get('section_id', ''))

    self.unified_kb['unified_index'] = {
        'methods': methods_index,
        'classes': classes_index,
        'interfaces': interfaces_index,
        'guide_sections': guide_index
    }
```

### Step 4: Implement merge and save (25 min)

```python
def merge_all(self):
    """Combine all KBs into unified structure."""
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
            'entity_index': self.csharp_vb_kb.get('entity_index', {})
        },
        'user_guides': {
            'word_guides': self.userguide_kb.get('word_guides', []),
            'sphinx_guides': self.userguide_kb.get('sphinx_guides', {})
        }
    }

    self.build_unified_index()

def _build_metadata(self) -> dict:
    """Create v7 metadata."""
    python_stats = self.python_kb.get('metadata', {})
    csharp_stats = self.csharp_vb_kb.get('statistics', {})

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
            'python_classes': len(self.python_kb.get('class_index', {})),
            'python_methods': len(self.python_kb.get('method_index', {})),
            'csharp_vb_members': csharp_stats.get('total_members', 0),
            'csharp_vb_namespaces': len(self.csharp_vb_kb.get('namespaces', {})),
            'guide_word_count': sum(
                g.get('word_count', 0)
                for g in self.userguide_kb.get('word_guides', [])
            ),
            'guide_sections': len(
                self.userguide_kb.get('sphinx_guides', {}).get('sections', {})
            ) + sum(
                len(g.get('sections', []))
                for g in self.userguide_kb.get('word_guides', [])
            )
        }
    }

def save_v7_kb(self):
    """Write unified KB to JSON."""
    logger.info(f"Saving v7 KB to {self.output_path}")
    with open(self.output_path, 'w', encoding='utf-8') as f:
        json.dump(self.unified_kb, f, indent=2, ensure_ascii=False)

    size_mb = self.output_path.stat().st_size / (1024 * 1024)
    logger.info(f"v7 KB saved: {size_mb:.1f} MB")
```

## Output Verification

```python
def validate_structure(self) -> bool:
    """Verify all required keys present."""
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

    # Verify indices have content
    if not self.unified_kb['unified_index']['methods']:
        logger.warning("Method index is empty")

    return True
```

## Todo List

- [x] Create `src/kb-consolidator-v7-merger.py`
- [x] Implement `load_python_kb()` v6 loader
- [x] Implement `load_csharp_vb_kb()` Phase 1 loader
- [x] Implement `load_userguide_kb()` Phase 2-3 loader
- [x] Implement `_build_metadata()` statistics
- [x] Implement `build_unified_index()` cross-API index
- [x] Implement `merge_all()` combiner
- [x] Implement `validate_structure()` verifier
- [x] Implement `save_v7_kb()` writer
- [x] Test with all three input files
- [x] Verify query interface compatibility

## Success Criteria

1. All three KBs merged without data loss
2. Unified index contains entries from all sources
3. Backward compatibility: v6 query patterns work
4. Output JSON <50 MB
5. Metadata statistics accurate
6. Validation passes

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Name collisions | Medium | Low | Separate API sections |
| Memory usage | Low | Medium | Load one KB at a time |
| Query interface breaks | Low | High | Integration test |
| Missing input file | Medium | High | Graceful fallback |

## Related Code

- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/output/processnet-knowledge-v6.json` - Python KB
- `/mnt/d/Vibecoding/RecurDyn-ProcessNet/src/processnet-query-interface.py` - Query interface
