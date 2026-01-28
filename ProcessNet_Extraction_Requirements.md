# ProcessNet Knowledge Base Extraction - Requirements Document

## Project Overview

**Objective:** Extract complete ProcessNet API documentation from RecurDyn installation folder and build structured knowledge base for automation workflows.

**Source:** CHM/HTML documentation files from RecurDyn installation directory  
**Target Output:** 
- JSON knowledge base (processnet_knowledge.json)
- Markdown reference docs (one file per namespace)
- Query interface module (processnet_query.py)

**Estimated Time:** 5-10 minutes execution  
**Cost:** $0 (runs locally)

---

## Phase 1: Environment Setup

### Prerequisites
```bash
# Python 3.8+
# Required libraries
pip install beautifulsoup4 lxml
```

### Documentation Location
```
Typical path: C:\Program Files\FunctionBay\RecurDyn\Help\ProcessNet\
Alternative: C:\RecurDyn\Documentation\ProcessNet\

Structure expected:
ProcessNet/
├── index.html
├── namespace_*.html
├── class_*.html
└── _static/
```

---

## Phase 2: HTML Parser Implementation

### Core Requirements

#### Script 1: `recurdyn_doc_parser.py`

**Functionality:**
1. **Recursive HTML Discovery** (CRITICAL - Must Loop All Files)
   
   **Requirements:**
   ```python
   # Must recursively scan ALL subdirectories
   # Process every .html, .htm, .chm file found
   # NO files should be skipped except explicitly excluded patterns
   ```
   
   **Implementation Pattern:**
   ```python
   from pathlib import Path
   
   def discover_all_documentation_files(root_path: Path) -> List[Path]:
       """
       Recursively find ALL documentation files in directory tree.
       
       Returns:
           List of all .html, .htm, .chm files found
       """
       all_files = []
       
       # Patterns to INCLUDE
       include_extensions = ['.html', '.htm', '.chm']
       
       # Patterns to EXCLUDE (only for specific folders/files)
       exclude_patterns = [
           '_static',    # Static assets
           '_images',    # Image directories
           'assets',     # Asset directories
           'css',        # Stylesheet directories
           'js',         # JavaScript directories
           '_sources',   # Sphinx source files
           '.git',       # Version control
           '__pycache__' # Python cache
       ]
       
       # Recursive walk through entire directory tree
       for path in root_path.rglob('*'):
           # Check if file has documentation extension
           if path.suffix.lower() in include_extensions:
               # Check if path contains any excluded patterns
               skip = False
               for pattern in exclude_patterns:
                   if pattern in str(path):
                       skip = True
                       break
               
               if not skip:
                   all_files.append(path)
       
       return sorted(all_files)  # Sort for deterministic processing
   ```
   
   **CHM File Handling:**
   ```python
   # If CHM files are found, they must be extracted first
   def extract_chm_file(chm_path: Path, output_dir: Path):
       """
       Extract CHM to HTML files before processing.
       
       Note: CHM is a compiled HTML help format.
       Use library like 'pychm' or system tool 'hh.exe -decompile'
       """
       import subprocess
       
       # Windows: Use hh.exe (built-in)
       subprocess.run([
           'hh.exe', 
           '-decompile', 
           str(output_dir),
           str(chm_path)
       ])
       
       # Alternative: Use pychm library
       # from chm.chm import CHMFile
       # chm = CHMFile(str(chm_path))
       # for name in chm.GetTopicsTree():
       #     content = chm.RetrieveObject(name)
       #     output_path = output_dir / name
       #     output_path.parent.mkdir(parents=True, exist_ok=True)
       #     output_path.write_bytes(content)
   ```
   
   **Verification Steps:**
   - Log total files discovered before processing
   - Log processing progress: "Processing file X of Y"
   - Log skipped files with reasons
   - Final summary: "Processed X files, skipped Y files"
   
   **Example Output:**
   ```
   [INFO] Discovering documentation files...
   [INFO] Found 347 HTML files
   [INFO] Found 2 CHM files
   [INFO] Extracting CHM: ProcessNet.chm -> temp/processnet_extracted/
   [INFO] Extracting CHM: RecurDyn_API.chm -> temp/recurdyn_extracted/
   [INFO] Total files to process: 847
   
   [INFO] Processing (1/847): index.html
   [INFO] Processing (2/847): namespace_geometry.html
   ...
   [INFO] Processing (847/847): examples_advanced.html
   
   [SUCCESS] Processed 847 files
   [WARNING] Skipped 12 files (see error_report.txt)
   ```

2. **Content Extraction per File**
   Extract following elements:
   
   **A. Page Metadata**
   - Title (from `<title>` or `<h1>`)
   - Namespace path (pattern: `ProcessNet.Namespace.SubNamespace`)
   - File path (relative to root)
   
   **B. Class Definitions**
   - Class name
   - Description paragraph (usually first `<p>` after class header)
   - Inheritance chain (look for "inherits from", "derived from", "base class")
   - Access modifiers (public, protected, private if documented)
   
   **C. Method Signatures**
   - Full signature with parameters
   - Method name extraction
   - Parameter list with types (parse from signature or following table)
   - Return type (from signature or "Returns:" section)
   - Description (paragraph following method header)
   
   **D. Properties/Fields**
   - Property name
   - Data type
   - Read-only flag (look for "read-only", "get only")
   - Description
   
   **E. Code Examples**
   - Section title ("Example:", "Usage:", "Sample Code:")
   - Code block content (from `<pre>`, `<code>`)
   - Language hint (assume Python/IronPython for ProcessNet)
   
   **F. Related References**
   - "See also" links
   - Cross-references to other classes/methods

3. **Parsing Strategies**

   **Strategy A: Definition Lists** (`<dl>`, `<dt>`, `<dd>`)
   ```html
   <dt>CreateArc(center, radius, start_angle, end_angle)</dt>
   <dd>Creates a circular arc with specified parameters...</dd>
   ```
   
   **Strategy B: Table-Based** (common in API docs)
   ```html
   <table class="methods">
     <tr><th>Method</th><th>Description</th></tr>
     <tr><td>CreateArc(...)</td><td>Creates arc...</td></tr>
   </table>
   ```
   
   **Strategy C: Heading + Paragraph**
   ```html
   <h3>CreateArc</h3>
   <pre>CreateArc(center, radius, start_angle, end_angle)</pre>
   <p>Creates a circular arc...</p>
   ```

4. **Special ProcessNet Patterns**

   **Pattern Detection:**
   - ProcessNet uses IronPython syntax
   - Look for namespace declarations: `ProcessNet.*`
   - Method signatures may include .NET type hints: `List[Body]`, `Vector3`, `bool`
   - Properties use get/set notation: `Body.Mass { get; set; }`
   - Events use delegate pattern: `OnSimulationStep(sender, args)`

5. **Data Validation**
   - Skip navigation elements (sidebar, header, footer)
   - Ignore boilerplate text (copyright, license)
   - Validate method signatures (must contain parentheses)
   - Check for duplicate entries (same method appears in multiple pages)

6. **Output Structure**
   ```json
   {
     "metadata": {
       "source": "RecurDyn ProcessNet API",
       "version": "extracted_from_path",
       "extraction_date": "ISO8601",
       "total_files_processed": 0,
       "extraction_duration_seconds": 0
     },
     "namespaces": {
       "ProcessNet.Geometry": {
         "full_name": "ProcessNet.Geometry",
         "description": "Geometry creation and manipulation",
         "files": ["geometry.html", "curve.html"],
         "classes": [
           {
             "name": "Curve",
             "description": "Represents a curve entity",
             "inheritance": "GeometricEntity",
             "methods": [...],
             "properties": [...],
             "source_file": "curve.html"
           }
         ],
         "standalone_methods": [
           {
             "name": "CreateArc",
             "signature": "CreateArc(center, radius, start_angle, end_angle)",
             "parameters": [
               {
                 "name": "center",
                 "type": "Vector3",
                 "description": "Arc center point"
               }
             ],
             "returns": "CurveID",
             "description": "Creates circular arc",
             "example_code": "arc = CreateArc([0,0,0], 50, 0, 90)",
             "source_file": "geometry.html"
           }
         ],
         "examples": [
           {
             "title": "Creating Basic Curves",
             "code": "...",
             "language": "python",
             "source_file": "examples.html"
           }
         ]
       }
     },
     "method_index": {
       "createarc": ["ProcessNet.Geometry"],
       "getallbodies": ["ProcessNet.Model"]
     },
     "class_index": {
       "curve": ["ProcessNet.Geometry"],
       "body": ["ProcessNet.Model", "ProcessNet.Subsystem"]
     }
   }
   ```

7. **Error Handling**
   - Log files that fail to parse (with error reason)
   - Continue processing on individual file errors
   - Generate warnings for:
     - Methods without descriptions
     - Parameters without type hints
     - Missing examples in core namespaces
   - Output error summary at end

8. **Performance Optimization**
   - Use streaming parsing for large files
   - Cache parsed content to avoid re-processing
   - Parallel processing if >100 files (use multiprocessing)

---

## Phase 3: Query Interface Implementation

### Script 2: `processnet_query.py`

**Requirements:**

1. **Load Knowledge Base**
   - Read JSON file
   - Build in-memory search indices:
     - Method name → namespace mapping
     - Class name → namespace mapping
     - Keyword → method/class mapping
   - Validate structure integrity

2. **Search Functions**

   **A. Exact Method Lookup**
   ```python
   def find_method(method_name: str, namespace: Optional[str] = None) -> List[MethodInfo]
   ```
   - Case-insensitive exact match
   - Optional namespace filter
   - Return all overloads if exist

   **B. Fuzzy Method Search**
   ```python
   def search_method_fuzzy(query: str, threshold: float = 0.6) -> List[MethodInfo]
   ```
   - Use difflib for similarity matching
   - Return top 5 matches above threshold
   - Sort by similarity score

   **C. Description Search**
   ```python
   def search_by_description(keywords: str) -> List[MethodInfo]
   ```
   - Search in method descriptions
   - Support multiple keywords (AND logic)
   - Highlight matching keywords in results

   **D. Namespace Exploration**
   ```python
   def list_namespace_contents(namespace: str) -> Dict
   ```
   - Return all classes and methods in namespace
   - Include count statistics
   - Sort alphabetically

   **E. Example Finder**
   ```python
   def find_examples(keyword: Optional[str] = None) -> List[Dict]
   ```
   - Find code examples
   - Filter by keyword in code or title
   - Return with context (namespace, related methods)

3. **Output Formats**

   **Console Format:**
   ```
   Method: CreateArc
   Namespace: ProcessNet.Geometry
   Signature: CreateArc(center: Vector3, radius: float, start_angle: float, end_angle: float) -> CurveID
   Description: Creates a circular arc with specified parameters
   
   Parameters:
     - center (Vector3): Arc center point in 3D space
     - radius (float): Arc radius in model units
     - start_angle (float): Start angle in degrees
     - end_angle (float): End angle in degrees
   
   Returns: CurveID - Identifier for created arc
   
   Example:
     arc = CreateArc([0,0,0], 50, 0, 90)
   ```

   **JSON Format:**
   ```json
   {
     "name": "CreateArc",
     "namespace": "ProcessNet.Geometry",
     "signature": "...",
     "parameters": [...],
     "returns": {...},
     "examples": [...]
   }
   ```

   **Markdown Format:** (for Skills)
   ```markdown
   ## CreateArc
   
   **Namespace:** ProcessNet.Geometry
   
   **Signature:** `CreateArc(center, radius, start_angle, end_angle)`
   
   Creates a circular arc with specified parameters.
   
   ### Parameters
   - `center` (Vector3): Arc center point
   - `radius` (float): Arc radius
   
   ### Returns
   `CurveID` - Identifier for created arc
   
   ### Example
   ```python
   arc = CreateArc([0,0,0], 50, 0, 90)
   ```
   ```

4. **Interactive CLI Mode**
   ```bash
   $ python processnet_query.py
   ProcessNet Knowledge Query Interface
   
   Commands:
     search <method_name>       - Find method by name
     describe <method_name>     - Show detailed method info
     list <namespace>           - List namespace contents
     example <keyword>          - Find examples
     export <namespace> <file>  - Export namespace to markdown
     help                       - Show this help
     quit                       - Exit
   
   > search CreateArc
   Found 2 matches:
     1. ProcessNet.Geometry.CreateArc
     2. ProcessNet.Curve.CreateArc
   
   > describe 1
   [detailed output]
   ```

5. **Integration Helpers**

   **Claude Code Import Function:**
   ```python
   def load_processnet_knowledge(kb_path: str = "processnet_knowledge.json") -> ProcessNetKnowledge:
       """
       Load knowledge base for Claude Code integration.
       
       Usage in Claude Code:
           from processnet_query import load_processnet_knowledge
           kb = load_processnet_knowledge()
           methods = kb.find_method("CreateArc")
           print(methods[0].signature)
       """
   ```

   **Auto-completion Data Export:**
   ```python
   def export_autocomplete_data(output_file: str):
       """
       Export method signatures for IDE autocomplete.
       Format: JSON with all signatures for IntelliSense.
       """
   ```

---

## Phase 4: Markdown Export Implementation

### Script 3: Integrated in `recurdyn_doc_parser.py`

**Requirements:**

1. **Generate Namespace Files**
   - One .md file per namespace
   - Filename: `ProcessNet_Namespace_SubNamespace.md`
   - Clean, readable structure

2. **Markdown Template**
   ```markdown
   # ProcessNet.Namespace
   
   > [Brief namespace description]
   
   ## Overview
   
   **Total Classes:** X
   **Total Methods:** Y
   **Total Examples:** Z
   
   ## Classes
   
   ### ClassName
   
   [Class description]
   
   **Inherits from:** BaseClass
   
   #### Methods
   
   ##### `MethodSignature(params)`
   
   [Method description]
   
   **Parameters:**
   - `param1` (type) - Description
   
   **Returns:** ReturnType - Description
   
   **Example:**
   ```python
   [code]
   ```
   
   ## Standalone Methods
   
   [Same structure as class methods]
   
   ## Examples
   
   ### Example Title
   
   ```python
   [code]
   ```
   
   ## See Also
   
   - Related namespace links
   ```

3. **Cross-References**
   - Link to related classes: `[ClassName](#classname)`
   - Link to methods: `[MethodName](#methodname)`
   - External links to original HTML if preserved

4. **Table of Contents**
   - Auto-generate TOC for files >500 lines
   - Nested structure following namespace hierarchy

---

## Phase 5: Validation & Testing

### Test Cases

**Test 1: Sample File Parsing**
```python
# Test on single HTML file
test_file = "C:/RecurDyn/Help/ProcessNet/geometry.html"
content = parser.parse_html_file(test_file)

assert content['namespace'] is not None
assert len(content['methods']) > 0
print(f"Extracted {len(content['methods'])} methods")
```

**Test 2: Full Extraction**
```python
# Run on full documentation
kb = parser.parse_all_docs()

print(f"Namespaces: {len(kb['namespaces'])}")
for ns, data in kb['namespaces'].items():
    print(f"  {ns}: {len(data['methods'])} methods, {len(data['classes'])} classes")
```

**Test 3: Query Interface**
```python
# Test search functionality
kb_query = ProcessNetKnowledge("processnet_knowledge.json")

# Test exact match
results = kb_query.find_method("CreateArc")
assert len(results) > 0

# Test fuzzy match
results = kb_query.search_method_fuzzy("createark")  # Typo
assert len(results) > 0

# Test description search
results = kb_query.search_by_description("circular arc")
assert len(results) > 0
```

**Test 4: Use Case Validation**

For each of the 3 target automation workflows:

**Use Case 1: DOE Batch Execution**
```python
# Verify methods exist:
assert kb_query.find_method("Model.Load")
assert kb_query.find_method("Model.Clone")
assert kb_query.find_method("SetParameter")
assert kb_query.find_method("Run")
```

**Use Case 2: Model Introspection**
```python
# Verify navigation methods:
assert kb_query.find_method("GetAllBodies")
assert kb_query.find_method("GetAllJoints")
assert kb_query.find_method("GetEntityByID")
assert kb_query.find_method("GetID")
```

**Use Case 3: Result Processing**
```python
# Verify result handling:
assert kb_query.find_method("Result.Load")
assert kb_query.find_method("GetTimeArray")
assert kb_query.find_method("GetEntityData")
```

---

## Phase 6: Deliverables Checklist

### Required Outputs

- [ ] `recurdyn_doc_parser.py` - Main extraction script
- [ ] `processnet_query.py` - Query interface module
- [ ] `processnet_knowledge.json` - Full knowledge base
- [ ] `processnet_docs_md/` - Markdown reference files (one per namespace)
- [ ] `extraction_log.txt` - Processing log with statistics
- [ ] `error_report.txt` - Files that failed to parse (if any)
- [ ] `README.md` - Usage instructions

### Statistics to Report

```
Extraction Summary:
==================
Total HTML files processed: X
Successful: Y
Failed: Z

Namespaces discovered: N
Total classes: C
Total methods: M
Total properties: P
Total examples: E

Top 5 largest namespaces:
  1. ProcessNet.Namespace1: M1 methods
  2. ProcessNet.Namespace2: M2 methods
  ...

Extraction duration: X seconds
Output file size: Y MB
```

---

## Phase 7: Claude Code Integration Guide

### Usage in Claude Code

**Step 1: Load Knowledge Base**
```python
# At start of Claude Code session
from processnet_query import load_processnet_knowledge

kb = load_processnet_knowledge("path/to/processnet_knowledge.json")
print(f"Loaded {len(kb.list_namespaces())} namespaces")
```

**Step 2: Query During Coding**
```python
# When writing automation script:

# Find method
methods = kb.find_method("CreateArc", namespace="Geometry")
print(methods[0].signature)
print(methods[0].description)

# Get all methods in namespace
geom_methods = kb.get_namespace_methods("ProcessNet.Geometry")
for m in geom_methods:
    print(f"  - {m.name}")

# Search by description
doe_methods = kb.search_by_description("design of experiments")
```

**Step 3: Generate Code with Context**
```python
# Example: Generate DOE script with method lookup

# Query relevant methods
model_methods = kb.find_method("Model.Load")
param_methods = kb.search_by_description("set parameter")

# Use signatures to generate correct code
# (Claude Code can now autocomplete based on actual API)
```

---

## Expected Command Line Usage

### Extraction Phase
```bash
# Basic extraction
python recurdyn_doc_parser.py "C:\RecurDyn\Help\ProcessNet"

# With all outputs
python recurdyn_doc_parser.py "C:\RecurDyn\Help\ProcessNet" \
    --output processnet_knowledge.json \
    --markdown ./processnet_docs_md \
    --log extraction_log.txt

# Verbose mode
python recurdyn_doc_parser.py "C:\RecurDyn\Help\ProcessNet" \
    --output processnet_knowledge.json \
    --verbose \
    --validate
```

### Query Phase
```bash
# Interactive mode
python processnet_query.py

# Direct query
python processnet_query.py --search "CreateArc"

# Export namespace
python processnet_query.py --export "ProcessNet.Geometry" --format markdown
```

---

## Error Handling Requirements

### Critical Errors (Stop Execution)
- Documentation path not found
- No HTML files in directory
- Cannot create output directory
- Insufficient disk space for output

### Warnings (Continue with Logging)
- Individual file parsing failures
- Malformed HTML structure
- Missing expected sections (methods, examples)
- Encoding issues

### Validation Warnings
- Methods without descriptions
- Parameters without type information
- Classes without examples
- Duplicate method names across namespaces

---

## Performance Targets

- **Extraction Speed:** <5 minutes for 500 HTML files
- **Memory Usage:** <500 MB peak during extraction
- **Output Size:** Expect 5-50 MB JSON depending on documentation size
- **Query Response:** <100ms for any lookup operation

---

## Success Criteria

### Minimum Viable Output
- ✅ At least 80% of HTML files successfully parsed
- ✅ All major namespaces identified (ProcessNet.Model, ProcessNet.Geometry, etc.)
- ✅ Method signatures extracted with >90% accuracy
- ✅ Query interface returns correct results for test cases

### Optimal Output
- ✅ >95% parsing success rate
- ✅ Complete parameter type information
- ✅ All code examples extracted
- ✅ Cross-references preserved
- ✅ Markdown output is clean and readable

---

## Post-Extraction Next Steps

After successful extraction, use knowledge base for:

1. **Create Claude Code Skills** for common ProcessNet workflows
2. **Build automation templates** for 3 target use cases
3. **Generate API cheat sheets** for quick reference
4. **Develop testing framework** for RecurDyn automation scripts

---

## Target Use Cases (For Validation)

### Use Case 1: DOE Batch Execution
**Required Methods:**
- Model loading/saving
- Parameter manipulation
- Model cloning
- Batch simulation execution
- File naming/organization

**Example Workflow:**
```python
# Load base model
model = ProcessNet.Model.Load("base_model.rdyn")

# Create design variations
for mass in [100, 150, 200]:
    for stiffness in [1000, 2000, 3000]:
        variant = model.Clone()
        variant.SetParameter("body_mass", mass)
        variant.SetParameter("spring_k", stiffness)
        variant.SaveAs(f"doe_m{mass}_k{stiffness}.rdyn")
        variant.Run()
```

### Use Case 2: Model Introspection
**Required Methods:**
- Entity enumeration (bodies, joints, forces)
- ID retrieval
- Property inspection
- Hierarchy navigation
- Entity creation from templates

**Example Workflow:**
```python
# Read model structure
model = ProcessNet.Model.Load("existing_model.rdyn")

# Map all entities
entity_map = {
    "bodies": [b.GetID() for b in model.GetAllBodies()],
    "joints": [j.GetID() for j in model.GetAllJoints()],
    "forces": [f.GetID() for f in model.GetAllForces()]
}

# Create similar entities
for body_id in entity_map["bodies"]:
    body = model.GetEntityByID(body_id)
    if body.GetType() == "RigidBody":
        # Create duplicate with offset
        new_body = model.CreateBodyLike(body)
        new_body.SetPosition(body.GetPosition() + offset)
```

### Use Case 3: Result Post-Processing
**Required Methods:**
- Result file loading (without opening GUI)
- Time series data extraction
- Entity-specific data retrieval
- Data export formats
- Batch result processing

**Example Workflow:**
```python
# Process results without opening RecurDyn
result = ProcessNet.Result.Load("sim_output.rsl")

# Extract data
time = result.GetTimeArray()
force_magnitude = result.GetEntityData("Force_1", "Magnitude")
displacement = result.GetEntityData("Body_2", "Displacement_X")

# Export for analysis
import pandas as pd
df = pd.DataFrame({
    "Time": time,
    "Force": force_magnitude,
    "Displacement": displacement
})
df.to_csv("processed_results.csv")
```

---

## Notes for Claude Code

- Prioritize extraction accuracy over speed
- Log verbosely to aid debugging
- Use type hints for all functions
- Include docstrings with examples
- Handle edge cases gracefully (malformed HTML, missing sections)
- Provide progress feedback during long operations
- Make scripts modular for easy customization

**If documentation structure is different than expected, adapt parser heuristics rather than failing hard.**

**Critical:** The scripts should be production-ready with proper error handling, logging, and user feedback. This is a foundational tool that will be used repeatedly for automation development.

---

## File Structure After Completion

```
project/
├── recurdyn_doc_parser.py       # Main extraction script
├── processnet_query.py          # Query interface
├── processnet_knowledge.json    # Full knowledge base
├── extraction_log.txt           # Processing log
├── error_report.txt             # Errors encountered
├── README.md                    # Usage guide
├── processnet_docs_md/          # Markdown exports
│   ├── ProcessNet_Geometry.md
│   ├── ProcessNet_Model.md
│   ├── ProcessNet_Analysis.md
│   └── ...
└── test_extraction.py           # Validation tests
```

---

## Quality Checklist

Before considering extraction complete, verify:

- [ ] All namespaces from documentation are represented
- [ ] Method signatures are syntactically valid
- [ ] Parameter names and types are extracted (where available)
- [ ] Code examples are properly formatted
- [ ] Cross-references between classes are preserved
- [ ] Query interface returns accurate results
- [ ] Markdown output is readable and well-formatted
- [ ] No critical parsing errors in log
- [ ] JSON structure validates against schema
- [ ] Test cases pass for all 3 use cases

---

## Appendix A: File Discovery Verification Protocol

### CRITICAL: Ensuring Complete Coverage

**Problem Statement:** Documentation may be scattered across:
- Root HTML files
- Subdirectory hierarchies (namespace folders)
- Multiple CHM archives
- Mixed encoding files

**Solution: Multi-Stage Discovery Process**

#### Stage 1: Initial Scan
```python
def verify_complete_discovery(root_path: Path):
    """
    Verify all documentation files are discovered.
    """
    print(f"Scanning: {root_path}")
    
    # Stage 1a: Count all potential files
    html_files = list(root_path.rglob('*.html'))
    htm_files = list(root_path.rglob('*.htm'))
    chm_files = list(root_path.rglob('*.chm'))
    
    print(f"  HTML files (.html): {len(html_files)}")
    print(f"  HTM files (.htm): {len(htm_files)}")
    print(f"  CHM files (.chm): {len(chm_files)}")
    
    # Stage 1b: Show directory structure depth
    max_depth = max(len(f.relative_to(root_path).parts) for f in html_files + htm_files)
    print(f"  Maximum directory depth: {max_depth}")
    
    # Stage 1c: List all unique subdirectories containing docs
    unique_dirs = set(f.parent for f in html_files + htm_files)
    print(f"  Unique directories: {len(unique_dirs)}")
    for d in sorted(unique_dirs)[:10]:  # Show first 10
        print(f"    - {d.relative_to(root_path)}")
    if len(unique_dirs) > 10:
        print(f"    ... and {len(unique_dirs) - 10} more")
    
    return html_files + htm_files, chm_files
```

#### Stage 2: Pre-Processing Checklist
```python
# Before starting extraction, verify:
checklist = {
    "Total files discovered": len(all_files),
    "Root-level files": len([f for f in all_files if f.parent == root_path]),
    "Nested files": len([f for f in all_files if f.parent != root_path]),
    "CHM files to extract": len(chm_files),
    "Estimated extraction time": f"{len(all_files) * 0.5} seconds"
}

for item, value in checklist.items():
    print(f"✓ {item}: {value}")

# User confirmation
response = input("\nProceed with extraction? (yes/no): ")
if response.lower() != 'yes':
    print("Aborted by user")
    exit(0)
```

#### Stage 3: Processing Loop with Progress
```python
def process_all_files_with_progress(file_list: List[Path]):
    """
    Process ALL files with detailed progress tracking.
    """
    total = len(file_list)
    successful = 0
    failed = 0
    skipped = 0
    
    print(f"\nProcessing {total} files...")
    print("=" * 60)
    
    for idx, file_path in enumerate(file_list, start=1):
        # Progress indicator
        percent = (idx / total) * 100
        print(f"[{percent:5.1f}%] ({idx:4d}/{total:4d}) {file_path.name}", end='')
        
        try:
            content = parse_html_file(file_path)
            
            # Validate extraction
            if content['methods'] or content['classes']:
                successful += 1
                print(" ✓")
            else:
                skipped += 1
                print(" ⚠ (no content)")
                
        except Exception as e:
            failed += 1
            print(f" ✗ ({str(e)[:30]}...)")
            log_error(file_path, e)
    
    print("=" * 60)
    print(f"Summary: {successful} successful, {skipped} skipped, {failed} failed")
    
    # Alert if too many failures
    if failed > total * 0.1:  # >10% failure rate
        print("\n⚠ WARNING: High failure rate detected!")
        print("  Check error_report.txt for details")
```

#### Stage 4: Post-Processing Verification
```python
def verify_extraction_completeness(knowledge_base: Dict, original_file_count: int):
    """
    Verify extraction captured all expected content.
    """
    print("\nExtraction Verification:")
    print("-" * 60)
    
    # Count processed files
    total_processed = sum(
        len(ns['files']) 
        for ns in knowledge_base['namespaces'].values()
    )
    
    # Check coverage
    coverage = (total_processed / original_file_count) * 100
    print(f"File coverage: {total_processed}/{original_file_count} ({coverage:.1f}%)")
    
    if coverage < 90:
        print("⚠ WARNING: Coverage below 90%")
        print("  Some files may not have been processed correctly")
    else:
        print("✓ Good coverage achieved")
    
    # Verify namespace distribution
    print("\nNamespace Distribution:")
    for ns_name, ns_data in knowledge_base['namespaces'].items():
        method_count = len(ns_data.get('methods', []))
        class_count = len(ns_data.get('classes', []))
        print(f"  {ns_name}:")
        print(f"    Classes: {class_count}")
        print(f"    Methods: {method_count}")
        
        if method_count == 0 and class_count == 0:
            print(f"    ⚠ WARNING: Empty namespace - check parsing")
    
    # Verify expected namespaces exist
    expected_namespaces = [
        'ProcessNet.Model',
        'ProcessNet.Geometry',
        'ProcessNet.Analysis',
        'ProcessNet.Control',
        'ProcessNet.Result'
    ]
    
    print("\nExpected Namespace Check:")
    for expected in expected_namespaces:
        found = any(expected in ns for ns in knowledge_base['namespaces'].keys())
        status = "✓" if found else "✗ MISSING"
        print(f"  {status} {expected}")
```

### VERIFICATION CHECKLIST FOR USER

After running extraction, manually verify:

- [ ] Total processed files matches discovered file count (±5%)
- [ ] All major subdirectories appear in namespace list
- [ ] No empty namespaces (unless expected)
- [ ] Method count seems reasonable (>10 methods per major namespace)
- [ ] Example code blocks were extracted (check JSON)
- [ ] error_report.txt has <10% of total files
- [ ] Generated markdown files are readable
- [ ] Query interface can find known methods (e.g., "CreateArc")

### TROUBLESHOOTING

**If coverage is low (<80%):**
1. Check file encoding (try utf-8, cp1252, latin-1)
2. Inspect sample files manually - are they actual documentation?
3. Check for JavaScript-rendered content (may need browser-based extraction)
4. Verify CHM files were extracted successfully

**If namespaces are missing:**
1. Check namespace detection regex patterns
2. Look for alternative namespace naming conventions
3. Manually grep for "ProcessNet." in HTML files

**If methods are not extracted:**
1. Inspect HTML structure of sample file
2. Adjust parsing strategies (add new patterns)
3. Check for table-based vs list-based layouts

---

**End of Requirements Document**

**Version:** 1.0  
**Date:** 2026-01-28  
**Author:** Dương (with Claude assistance)  
**Purpose:** Claude Code instruction set for ProcessNet knowledge extraction
