# ProcessNet Hybrid Verification Workflow

## Strategy Overview

**Objective:** Validate Python extraction logic (Option 2) using browser-based spot-checks (Option 1) before committing to full extraction.

**Benefits:**
- ✅ Catch parser errors early with <5 sample files
- ✅ Verify extraction accuracy interactively
- ✅ Adjust parser logic based on actual HTML structure
- ✅ Total cost: ~$1-2 for verification vs $18-36 for full browser extraction

**Process Flow:**
```
Step 1: Sample Extraction (Python) → 3-5 representative files
Step 2: Browser Validation (Claude in Chrome) → Compare extracted vs actual
Step 3: Parser Adjustment → Fix issues found
Step 4: Full Extraction (Python) → Process all files
Step 5: Spot-Check Validation (Browser) → Verify 5-10 random results
```

---

## Phase 1: Smart Sampling Strategy

### Step 1.1: Identify Representative Files

**Goal:** Pick 3-5 files that represent different documentation patterns.

**Selection Criteria:**
```python
# Sample file selection strategy
representative_samples = {
    "index": "index.html",                    # Overview/table of contents
    "namespace": "ProcessNet.Geometry.html",  # Namespace-level doc
    "class": "class_Body.html",               # Class definition
    "methods": "methods_create.html",         # Method reference
    "examples": "examples_tutorial.html"      # Code examples
}
```

**Manual Selection Process:**
1. Open documentation folder in File Explorer
2. Sort by file size → pick small (index), medium (namespace), large (method reference)
3. Look for different HTML templates (some docs have multiple layouts)
4. Note any special files: tutorial.html, quickstart.html, api_reference.html

**Output for Verification:**
```bash
# Create sample list file
echo "C:\RecurDyn\Help\ProcessNet\index.html" > sample_files.txt
echo "C:\RecurDyn\Help\ProcessNet\namespace_geometry.html" >> sample_files.txt
echo "C:\RecurDyn\Help\ProcessNet\class_Body.html" >> sample_files.txt
echo "C:\RecurDyn\Help\ProcessNet\method_CreateArc.html" >> sample_files.txt
echo "C:\RecurDyn\Help\ProcessNet\examples.html" >> sample_files.txt
```

### Step 1.2: Run Sample Extraction (Python)

**Create test script:**
```python
# test_sample_extraction.py
"""
Test extraction on sample files only.
"""
from pathlib import Path
from recurdyn_doc_parser import ProcessNetDocParser
import json

def test_sample_extraction():
    # Read sample file list
    sample_files = Path('sample_files.txt').read_text().splitlines()
    
    parser = ProcessNetDocParser(Path(sample_files[0]).parent)
    
    results = {}
    for sample_path in sample_files:
        print(f"\n{'='*60}")
        print(f"Processing: {Path(sample_path).name}")
        print('='*60)
        
        try:
            content = parser.parse_html_file(Path(sample_path))
            
            # Show extraction results
            print(f"Title: {content['title']}")
            print(f"Namespace: {content['namespace']}")
            print(f"Classes found: {len(content['classes'])}")
            print(f"Methods found: {len(content['methods'])}")
            print(f"Properties found: {len(content['properties'])}")
            print(f"Examples found: {len(content['examples'])}")
            
            # Show sample methods
            if content['methods']:
                print("\nSample Methods:")
                for method in content['methods'][:3]:
                    print(f"  - {method['signature']}")
            
            # Show sample classes
            if content['classes']:
                print("\nSample Classes:")
                for cls in content['classes'][:3]:
                    print(f"  - {cls['name']}")
            
            results[Path(sample_path).name] = content
            
        except Exception as e:
            print(f"ERROR: {e}")
            results[Path(sample_path).name] = {"error": str(e)}
    
    # Save results for comparison
    output_path = Path('sample_extraction_results.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n\nResults saved to: {output_path}")
    print("\nReady for browser validation!")

if __name__ == '__main__':
    test_sample_extraction()
```

**Run test:**
```bash
python test_sample_extraction.py
```

**Expected Output:**
```
============================================================
Processing: index.html
============================================================
Title: ProcessNet API Reference
Namespace: ProcessNet
Classes found: 0
Methods found: 12
Properties found: 0
Examples found: 2

Sample Methods:
  - GetVersion()
  - Initialize(config)
  - Shutdown()

============================================================
Processing: class_Body.html
============================================================
Title: Body Class
Namespace: ProcessNet.Model
Classes found: 1
Methods found: 15
Properties found: 8
Examples found: 3

Sample Methods:
  - GetMass()
  - SetMass(value)
  - GetPosition()

Results saved to: sample_extraction_results.json
Ready for browser validation!
```

---

## Phase 2: Browser-Based Verification

### Step 2.1: Prepare Verification Checklist

**Create verification document:**
```markdown
# Verification Checklist

## File: index.html
**Python extracted:**
- Title: ProcessNet API Reference
- Namespace: ProcessNet
- Methods: 12
- Examples: 2

**Browser validation questions:**
1. Does page title match "ProcessNet API Reference"?
2. Count visible methods in page - is it ~12?
3. Are there code example blocks - count them?
4. Are methods listed as:
   - GetVersion()
   - Initialize(config)
   - Shutdown()

---

## File: class_Body.html
**Python extracted:**
- Title: Body Class
- Methods: 15 (GetMass, SetMass, GetPosition...)
- Properties: 8
- Examples: 3

**Browser validation questions:**
1. Does page show "Body" as class name?
2. Count method signatures - approximately 15?
3. Count property listings - approximately 8?
4. Count code example sections - exactly 3?
5. Verify method signatures match:
   - GetMass()
   - SetMass(value)
   - GetPosition()

---

[Continue for each sample file]
```

### Step 2.2: Claude in Chrome Verification Session

**Instructions for Claude in Chrome:**

```
I need you to verify Python extraction results against actual HTML documentation.

Context:
- I've extracted API documentation using a Python script
- Need to verify the extraction accuracy before processing 500+ files
- You'll compare Python results vs what you see in browser

Process:
1. I'll give you the Python extraction results (JSON)
2. Open each sample HTML file in browser
3. Verify counts match (methods, classes, examples)
4. Check if extracted signatures are correct
5. Report discrepancies

Sample files to verify:
1. file:///C:/RecurDyn/Help/ProcessNet/index.html
2. file:///C:/RecurDyn/Help/ProcessNet/class_Body.html
3. [... other samples]

Python extraction results:
[paste sample_extraction_results.json]

Please verify each file systematically.
```

**Verification Template for Claude:**

For each file, Claude should report:
```
File: index.html
Status: ✓ PASS / ✗ FAIL

Verification Results:
- Title match: ✓ (Both show "ProcessNet API Reference")
- Method count: ✓ (Python: 12, Browser: 12 visible methods)
- Example count: ✗ (Python: 2, Browser: 3 code blocks found)
  → Issue: Parser may be missing one example section

Method Signature Verification:
- GetVersion(): ✓ Found in browser
- Initialize(config): ✓ Found in browser
- Shutdown(): ✓ Found in browser

Discrepancies:
1. Example count mismatch - check if one example is in different HTML structure
2. [any other issues]

Recommended Parser Adjustments:
- Check for example sections in <div class="example"> vs <section class="code-sample">
```

### Step 2.3: Interactive Verification Script

**For systematic verification:**

```markdown
## Verification Protocol

### File 1: index.html

**Step 1:** Open file in browser
```
Action: Navigate to file:///C:/RecurDyn/Help/ProcessNet/index.html
```

**Step 2:** Verify title
```
Python says: "ProcessNet API Reference"
Browser shows: [Claude reports what it sees]
Match: ✓/✗
```

**Step 3:** Count methods
```
Python says: 12 methods
Action: Find all method signatures on page
Browser count: [Claude counts and reports]
Match: ✓/✗
```

**Step 4:** Inspect first method
```
Python extracted: GetVersion()
Action: Find GetVersion in browser
Browser shows: [Claude reports exact text/signature]
Match: ✓/✗
```

**Step 5:** Count examples
```
Python says: 2 examples
Action: Find all code blocks with <pre> or <code>
Browser count: [Claude counts]
Match: ✓/✗
```

[Repeat for each file]
```

---

## Phase 3: Parser Adjustment Based on Findings

### Step 3.1: Analyze Discrepancies

**Common discrepancy patterns:**

**Pattern 1: Count Mismatches**
```
Python: 12 methods
Browser: 15 methods

Root Cause Analysis:
- Parser might be missing methods in tables vs lists
- Some methods might be in collapsed sections
- Method overloads might be counted differently

Fix:
- Add table-based method extraction
- Check for expandable sections (<details>, <summary>)
- Update method counting logic
```

**Pattern 2: Signature Format Differences**
```
Python extracted: CreateArc(center, radius, angle)
Browser shows: CreateArc(center: Vector3, radius: float, startAngle: float, endAngle: float)

Root Cause:
- Parser not capturing full parameter details
- Type hints are in separate elements

Fix:
- Extract parameter types from adjacent <span> or <td> elements
- Parse parameter tables if method signature is incomplete
```

**Pattern 3: Missing Content**
```
Python: 0 examples
Browser: 3 examples visible

Root Cause:
- Examples might be in <div class="highlight"> instead of <pre>
- Code might be syntax-highlighted with complex HTML

Fix:
- Add extraction for <div class="highlight"> blocks
- Handle syntax-highlighted code (multiple <span> elements)
```

### Step 3.2: Update Parser Logic

**Create adjustment script:**
```python
# parser_adjustments.py
"""
Apply fixes based on verification findings.
"""

def add_table_method_extraction(soup):
    """
    Fix: Extract methods from table layouts
    """
    methods = []
    
    # New pattern: table-based method documentation
    method_tables = soup.find_all('table', class_=['methods', 'api-table'])
    
    for table in method_tables:
        for row in table.find_all('tr')[1:]:  # Skip header
            cells = row.find_all('td')
            if len(cells) >= 2:
                signature = cells[0].get_text(strip=True)
                description = cells[1].get_text(strip=True)
                
                methods.append({
                    'signature': signature,
                    'description': description
                })
    
    return methods


def extract_highlighted_examples(soup):
    """
    Fix: Extract syntax-highlighted code examples
    """
    examples = []
    
    # Original pattern: <pre><code>
    for pre in soup.find_all('pre'):
        code = pre.find('code')
        if code:
            examples.append(code.get_text())
    
    # New pattern: <div class="highlight">
    for div in soup.find_all('div', class_='highlight'):
        code_text = div.get_text(strip=True)
        if code_text:
            examples.append(code_text)
    
    return examples


# Test adjusted parser on same samples
def test_adjusted_parser():
    # Re-run extraction with fixes
    # Compare new results with browser verification
    pass
```

### Step 3.3: Re-test on Samples

```bash
# Apply fixes to parser
# Re-run sample extraction
python test_sample_extraction.py

# Compare new results
# Should now match browser verification
```

---

## Phase 4: Full Extraction with Confidence

### Step 4.1: Pre-Flight Checklist

Before running full extraction:

- [ ] Sample extraction matches browser verification (±5%)
- [ ] All 5 sample files parse successfully
- [ ] Parser adjustments tested and working
- [ ] Extraction logic handles:
  - [ ] Multiple HTML layout patterns
  - [ ] Table-based method docs
  - [ ] Syntax-highlighted code
  - [ ] Nested namespace structures
- [ ] Error handling tested with malformed file

### Step 4.2: Run Full Extraction

```bash
# Full extraction with verified parser
python recurdyn_doc_parser.py "C:\RecurDyn\Help\ProcessNet" \
    --output processnet_knowledge.json \
    --markdown ./processnet_docs_md \
    --log extraction_log.txt \
    --verbose
```

### Step 4.3: Monitor Progress

**Look for:**
- Consistent success rate across files
- No sudden drop in extraction counts
- Similar patterns in namespace distribution

**Red flags:**
- Success rate drops below 85%
- Large namespaces have 0 methods
- Extraction speed suddenly slows (malformed HTML)

---

## Phase 5: Post-Extraction Spot Checks

### Step 5.1: Random Sampling Strategy

**After full extraction, verify 5-10 random files:**

```python
# random_validation_samples.py
import random
from pathlib import Path

def select_random_samples(knowledge_base, n=10):
    """
    Select random files from extraction for spot-check validation.
    """
    all_files = []
    
    for ns_data in knowledge_base['namespaces'].values():
        all_files.extend(ns_data['files'])
    
    # Stratified sampling: pick from different namespaces
    samples_per_ns = {}
    for ns_name, ns_data in knowledge_base['namespaces'].items():
        if ns_data['files']:
            sample = random.choice(ns_data['files'])
            samples_per_ns[ns_name] = sample
    
    # Random samples from remaining
    remaining = [f for f in all_files if f not in samples_per_ns.values()]
    additional = random.sample(remaining, min(n - len(samples_per_ns), len(remaining)))
    
    all_samples = list(samples_per_ns.values()) + additional
    
    return all_samples[:n]
```

### Step 5.2: Quick Browser Spot-Check

**For each random sample:**

```markdown
File: [random_file.html]

Quick Checks:
1. ✓/✗ Title exists in JSON
2. ✓/✗ Method count approximately correct (±20%)
3. ✓/✗ At least one method signature matches exactly
4. ✓/✗ Class name (if any) matches

If all ✓ → Extraction validated
If 2+ ✗ → Investigate specific namespace/pattern
```

**Browser verification command:**
```
Claude, quick spot-check for these 5 files:
1. Open file in browser
2. Count methods (rough count, ±2 is OK)
3. Verify first method signature matches JSON
4. Report any obvious discrepancies

Files to check:
- file:///C:/RecurDyn/Help/ProcessNet/[file1.html]
- file:///C:/RecurDyn/Help/ProcessNet/[file2.html]
...

JSON data for comparison:
[paste relevant excerpts from processnet_knowledge.json]
```

---

## Phase 6: Validation Metrics & Sign-Off

### Success Criteria

**Extraction Quality Metrics:**
```
Sample Verification (Phase 2):
- Accuracy: 5/5 files match browser (100%)
- Method signatures: 45/45 correct (100%)
- Example extraction: 12/13 (92%) - acceptable

Full Extraction (Phase 4):
- Files processed: 847/847 (100%)
- Parsing success: 835/847 (98.6%)
- Average methods per namespace: 85 (reasonable)

Random Spot-Check (Phase 5):
- Sample validation: 9/10 correct (90%)
- Critical namespaces verified: ProcessNet.Model ✓, ProcessNet.Geometry ✓

Overall Assessment: ✅ PASS - Ready for production use
```

### Sign-Off Checklist

- [ ] Sample verification: ≥90% accuracy
- [ ] Full extraction: ≥95% success rate
- [ ] Random spot-check: ≥85% accuracy
- [ ] Critical namespaces extracted completely
- [ ] Query interface returns expected results
- [ ] Use case validation: All 3 target workflows have required methods

**When all checked → Knowledge base is production-ready**

---

## Cost & Time Breakdown

### Hybrid Approach Costs

**Phase 1-3 (Sample + Verification + Adjustment):**
- Python extraction: 5 files × 2 sec = 10 seconds (FREE)
- Browser verification: 5 files × 10 tool calls × $0.01 = **$0.50**
- Parser adjustment: LOCAL (FREE)
- Re-test: LOCAL (FREE)

**Phase 4 (Full Extraction):**
- Python extraction: 847 files × 0.5 sec = ~7 minutes (FREE)

**Phase 5 (Spot-Check Validation):**
- Browser spot-check: 10 files × 5 tool calls × $0.01 = **$0.50**

**Total Cost: ~$1.00**  
**Total Time: ~20 minutes (including browser sessions)**

**Compare to:**
- Pure Option 1 (Browser-only): $18-36, 60 minutes
- Pure Option 2 (Python-only, no validation): $0, but unknown accuracy

**Hybrid = Best value: $1, 20 minutes, validated accuracy**

---

## Troubleshooting Guide

### Issue: Browser verification shows 0 methods but Python found 12

**Diagnosis:**
- Check if browser page is fully loaded (JavaScript rendering?)
- Verify file path is correct
- Try opening in different browser

**Resolution:**
- If JavaScript-rendered: Original HTML may not have methods, they're loaded dynamically
- Solution: Parser is correct, browser sees rendered page (ignore discrepancy)

### Issue: Python extraction is too slow (>10 sec per file)

**Diagnosis:**
- Large HTML files with complex structure
- BeautifulSoup parsing overhead

**Resolution:**
- Use `lxml` parser instead of `html.parser`: `BeautifulSoup(html, 'lxml')`
- Add caching for repeated elements

### Issue: Browser verification impossible (can't open local files)

**Diagnosis:**
- Browser security settings block file:/// URLs
- Files are in network location

**Resolution:**
- Start local HTTP server: `python -m http.server 8000`
- Access via: `http://localhost:8000/path/to/file.html`
- Or adjust browser settings to allow local files

---

## Template: Verification Report

**After completing all phases, generate report:**

```markdown
# ProcessNet Extraction Verification Report

**Date:** 2026-01-28
**Extraction Method:** Hybrid (Python + Browser validation)

## Phase 1: Sample Extraction
- Files tested: 5
- Success rate: 5/5 (100%)
- Issues found: Example extraction missed 1 case

## Phase 2: Browser Verification
- Verification method: Claude in Chrome
- Accuracy: 95% (47/50 checks passed)
- Discrepancies: Example count in 3 files
- Cost: $0.50

## Phase 3: Parser Adjustments
- Adjustments made: 2
  1. Added <div class="highlight"> example extraction
  2. Enhanced table-based method parsing
- Re-test results: 100% match with browser

## Phase 4: Full Extraction
- Total files: 847
- Processed: 847
- Success: 835 (98.6%)
- Failed: 12 (1.4%) - see error_report.txt
- Duration: 7 minutes

## Phase 5: Random Spot-Check
- Files verified: 10
- Match rate: 9/10 (90%)
- Critical namespaces: All verified ✓
- Cost: $0.50

## Validation Metrics
- Method extraction accuracy: 98%
- Class extraction accuracy: 97%
- Example extraction accuracy: 92%
- Overall confidence: HIGH

## Use Case Validation
✅ DOE automation: All required methods present
✅ Model introspection: Navigation methods found
✅ Result processing: Result.* namespace complete

## Sign-Off
- Extraction quality: PASS
- Ready for production: YES
- Total cost: $1.00
- Total time: 23 minutes

**Approved for use in Claude Code automation development.**
```

---

## Quick Reference: Verification Commands

### Phase 2: Browser Verification
```bash
# In Claude chat (claude.ai)
"I need to verify Python extraction results for ProcessNet documentation.
Files: 5 samples in C:\RecurDyn\Help\ProcessNet\
Python results: [paste JSON]
Please open each file in browser and verify extraction accuracy."
```

### Phase 5: Spot-Check
```bash
# In Claude chat
"Quick spot-check for 10 random files from full extraction.
For each file: rough method count + verify one signature.
Files: [list]
JSON excerpts: [paste]"
```

---

**End of Hybrid Verification Workflow**
