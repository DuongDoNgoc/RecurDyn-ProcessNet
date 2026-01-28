# API Documentation Knowledge Base: JSON Design Best Practices

## Executive Summary
Research identifies four core strategies for structuring ProcessNet API documentation in JSON: hierarchical schema with namespaces, indexed flat-file design for query performance, structured parameter definitions following JSON Schema Draft 2020-12, and embedded code examples with language variants. Fuzzy-search capability requires pre-indexed term variations and Levenshtein-distance algorithms.

---

## 1. JSON Schema Design Patterns

### Hierarchical Structure
Organize API documentation in 3-4 levels:
- **Level 1**: Namespaces (e.g., `dynamics`, `solver`, `materials`)
- **Level 2**: Classes (e.g., `RigidBody`, `Material`)
- **Level 3**: Methods/Properties (e.g., `set_mass()`, `color`)
- **Level 4**: Parameters & Return types

**Example structure:**
```json
{
  "namespaces": [
    {
      "name": "dynamics",
      "description": "Core dynamics simulation",
      "classes": [
        {
          "name": "RigidBody",
          "methods": [...],
          "properties": [...]
        }
      ]
    }
  ]
}
```

**Key principle**: Flatten search indices while maintaining hierarchy for documentation navigation. Create separate "flat" index collection for queries.

---

## 2. Indexing for Fast Lookups

### Multi-Index Strategy
Implement 3 separate indices:

1. **Exact Match Index**: Map `namespace.class.method` → document ID
   ```json
   {"index": {"dynamics.RigidBody.set_mass": "doc_001"}}
   ```

2. **Full-Text Index**: Pre-computed word tokens from descriptions
   ```json
   {"tokens": ["mass", "weight", "inertia"]}
   ```

3. **Fuzzy Index**: Pre-computed character variations (Levenshtein ≤1)
   - Store both "color" and "colour"
   - Cache common typos

### Performance Optimization
- **Caching**: Recent queries (reduces load ~40%)
- **Pre-computation**: Store method aliases and synonyms
- **Token normalization**: Lowercase, stem terms (e.g., "setting" → "set")

**Recommended library**: Fuse.js (lightweight fuzzy search) or uFuzzy for efficient matching without external database.

---

## 3. Parameter Type Definition

### JSON Schema Specification
Follow JSON Schema Draft 2020-12 for all parameter definitions:

```json
{
  "parameters": [
    {
      "name": "mass",
      "type": "number",
      "format": "float",
      "minimum": 0.0,
      "description": "Body mass in kilograms",
      "required": true,
      "default": null
    },
    {
      "name": "color",
      "type": "string",
      "enum": ["red", "blue", "green"],
      "description": "Visual color identifier"
    }
  ]
}
```

### Best Practices for Parameter Naming
- Use **consistent names** across all methods (not `start_date` + `begin_date`)
- Avoid redundant type information in names (`recipientEmails`, not `recipientEmailsArray`)
- Be **concise but descriptive**: `max_iterations` not `maximum_number_of_iterations`
- Include **format hints** for strings: `date` (ISO-8601), `uuid`, `regex`

### Return Type Documentation
```json
{
  "returns": {
    "type": "object",
    "properties": {
      "status": {"type": "string"},
      "result": {"type": "array", "items": {"type": "number"}}
    }
  }
}
```

---

## 4. Code Examples Storage

### Multi-Language Example Structure
Store examples separately from API definitions with language tagging:

```json
{
  "examples": [
    {
      "id": "ex_001",
      "method_ref": "dynamics.RigidBody.set_mass",
      "language": "python",
      "code": "body.set_mass(10.5)",
      "description": "Set body mass",
      "tags": ["basic", "initialization"]
    },
    {
      "id": "ex_002",
      "method_ref": "dynamics.RigidBody.set_mass",
      "language": "c++",
      "code": "body->setMass(10.5);",
      "tags": ["basic", "initialization"]
    }
  ]
}
```

### Organization Tips
- Store examples in separate collection (don't duplicate in method definition)
- Use `method_ref` foreign key for cross-referencing
- Tag examples: `basic`, `advanced`, `edge_case`, `error_handling`
- Include **output/result** for each example when applicable
- Version examples with API version tags

---

## 5. Query Architecture Design

### Three Query Patterns

**Pattern 1: Exact Match**
```
Query: "dynamics.RigidBody.set_mass"
→ Direct lookup in exact-match index
→ O(1) performance
```

**Pattern 2: Full-Text Search**
```
Query: "set body mass"
→ Tokenize: ["set", "body", "mass"]
→ Search full-text index
→ Rank by relevance (TF-IDF)
```

**Pattern 3: Fuzzy Search**
```
Query: "setmass" (typo/missing underscore)
→ Levenshtein distance calculation
→ Returns "set_mass" with confidence score
```

### Implementation Options
- **Client-side**: Fuse.js (no backend needed, good for <10k docs)
- **Server-side**: Redis + RediSearch (scales to millions)
- **Hybrid**: SQLite FTS (full-text search) + Levenshtein UDF

---

## 6. ProcessNet-Specific Recommendations

### Suggested JSON Structure
```json
{
  "api_version": "1.0",
  "timestamp": "2026-01-28",
  "namespaces": [
    {
      "id": "ns_001",
      "name": "dynamics",
      "description": "...",
      "classes": [
        {
          "id": "cls_001",
          "name": "RigidBody",
          "inherits": "DynamicBody",
          "methods": [
            {
              "id": "mth_001",
              "name": "set_mass",
              "description": "...",
              "parameters": [...],
              "returns": {...},
              "example_ids": ["ex_001", "ex_002"],
              "tags": ["setter", "basic"]
            }
          ],
          "properties": [...]
        }
      ]
    }
  ],
  "indices": {
    "exact_match": {},
    "full_text": {},
    "fuzzy": {}
  },
  "examples": [...]
}
```

### Index Generation (Build-time)
```python
# Pseudocode
def build_indices(api_json):
    exact_match = {}
    for ns in api_json["namespaces"]:
        for cls in ns["classes"]:
            for method in cls["methods"]:
                key = f"{ns.name}.{cls.name}.{method.name}"
                exact_match[key] = method.id

    full_text = {}
    for method in all_methods:
        tokens = tokenize(method.description)
        for token in tokens:
            full_text.setdefault(token, []).append(method.id)

    return {"exact_match": exact_match, "full_text": full_text}
```

---

## 7. Performance Considerations

| Query Type | Best Performance | Strategy |
|-----------|-----------------|----------|
| Exact match | O(1) | Hash map/dict lookup |
| Description search | O(n) → O(log n) | Pre-computed inverted index |
| Fuzzy search | O(n) | Pre-cache variations; limit edit distance to ≤1 |
| Combined query | O(log n) | Two-pass: fuzzy → filter → rank |

**File size estimates for 500 API items:**
- Base JSON (hierarchy): ~300 KB
- Exact-match index: ~50 KB
- Full-text index: ~200 KB
- Fuzzy variants: ~150 KB
- **Total**: ~700 KB (in-memory, negligible)

---

## 8. Tools & Libraries

| Task | Recommended | Notes |
|------|-------------|-------|
| Fuzzy search (JS/Python) | Fuse.js / rapidfuzz | Lightweight, no DB needed |
| Full-text indexing | MiniSearch (JS) / whoosh (Python) | In-memory, good for <100k docs |
| Schema validation | jsonschema (Python) / Ajv (JS) | Enforce structure |
| Example storage | SQLite or JSON file + index | Simple, portable |

---

## Key Takeaways

1. **Separate concerns**: Keep definition hierarchy separate from search indices
2. **Indexed parameters**: Pre-compute all searchable variations at build time
3. **Type clarity**: Use JSON Schema Draft 2020-12 for all parameters
4. **Example versioning**: Store examples separately with language/version tags
5. **Fuzzy + exact**: Support both perfect match and typo-tolerant search
6. **Build-time optimization**: Generate indices once; serve pre-computed results

---

## Unresolved Questions

- Should examples be versioned by API version or merged into single collection with version tags?
- What edit-distance threshold for fuzzy search (≤1 or ≤2)?
- Will ProcessNet need semantic search (description similarity) or just lexical matching?
- Should namespace/class inheritance be explicitly tracked in schema?

---

## Sources

- [JSON Schema Official Documentation](https://json-schema.org/)
- [OpenAPI Basics: Crafting JSON Schemas](https://www.theneo.io/blog/openapi-basics-crafting-json-schemas-for-seamless-api-documentation)
- [Elegant APIs with JSON Schema](https://brandur.org/elegant-apis)
- [Redis JSON Indexing and Full-Text Search](https://redis.io/blog/index-and-query-json-docs-with-redis/)
- [Fuse.js - Lightweight Fuzzy Search](https://www.fusejs.io/)
- [uFuzzy - Efficient Fuzzy Matching](https://github.com/leeoniya/uFuzzy)
- [Fuzzy Search Comprehensive Guide](https://www.meilisearch.com/blog/fuzzy-search)
- [OpenAPI Schema Best Practices](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/plugins-api-schema-best-practices.html)
- [Pydantic JSON Schema](https://docs.pydantic.dev/latest/concepts/json_schema/)
- [Documenting Python APIs - LSST Guide](https://developer.lsst.io/python/numpydoc.html)
- [Hierarchical Knowledge Base Patterns](https://github.com/zadam/trilium/wiki/Patterns-of-personal-knowledge-base)
