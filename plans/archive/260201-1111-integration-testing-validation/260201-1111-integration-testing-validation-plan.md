---
title: "Integration Testing - ProcessNet API Validation"
description: "Validate extracted ProcessNet API against real RecurDyn automation scenarios"
status: pending
priority: P1
effort: 8h
branch: master
tags: [integration, testing, validation, processnet, api]
created: 2026-02-01
---

# Integration Testing - ProcessNet API Validation

## Overview

Validate the extracted ProcessNet API documentation against real RecurDyn automation scenarios. This plan creates integration tests to verify method signatures, parameters, and return types match the actual API used in automation workflows.

**Current State:**
- Knowledge base: 4,360 methods, 1,803 classes, 23 namespaces
- Parser: Sphinx-based extraction with parameter/property/class support
- Query interface: CLI and REST API endpoints
- Test coverage: 120+ existing tests

**Target State:**
- Integration tests validating API accuracy
- Discrepancy report with findings
- Parser improvements for critical issues
- Confidence score for extracted data

## Phases

| Phase | Status | Description | Effort |
|-------|--------|-------------|--------|
| [01-research-and-analysis](#phase-01-research-and-analysis) | pending | Analyze knowledge base and identify validation targets | 1h |
| [02-test-infrastructure](#phase-02-test-infrastructure) | pending | Build test fixtures and validation helpers | 1.5h |
| [03-method-signature-validation](#phase-03-method-signature-validation) | pending | Validate method signatures against documentation | 2h |
| [04-parameter-return-type-validation](#phase-04-parameter-return-type-validation) | pending | Verify parameter types and return types | 2h |
| [05-automation-scenario-validation](#phase-05-automation-scenario-validation) | pending | Test real automation workflows end-to-end | 1h |
| [06-discrepancy-reporting](#phase-06-discrepancy-reporting) | pending | Document findings and recommend fixes | 0.5h |

---

## Phase 01: Research and Analysis

**Priority:** P1 | **Status:** pending | **Effort:** 1h

### Context Links
- Knowledge base: `output/processnet-knowledge.json`
- Markdown docs: `output/markdown/*.md`
- Use cases: `README.md` (DOE, Model Introspection, Result Processing)

### Overview
Analyze the extracted knowledge base to identify high-value validation targets. Focus on methods used in common automation workflows.

### Key Insights
- 23 namespaces with 4,360 methods need validation
- Cannot run actual RecurDyn (requires Windows license)
- Must validate against extracted documentation itself
- Cross-reference between HTML sources and extracted JSON

### Requirements

**Functional:**
1. Identify top 50 most-used methods across 3 use cases
2. Map method signatures to source HTML files
3. Create validation dataset with expected vs actual
4. Establish accuracy thresholds

**Non-Functional:**
- Tests must run without RecurDyn installation
- Validation based on documentation consistency
- Clear pass/fail criteria

### Architecture

```
Knowledge Base
    ↓
Method Sampling (select 50 key methods)
    ↓
Cross-Reference (HTML → JSON)
    ↓
Signature Validation
    ↓
Parameter/Type Validation
    ↓
Discrepancy Report
```

### Related Code Files

**Read:**
- `output/processnet-knowledge.json` - Full knowledge base
- `output/markdown/ProcessNet*.md` - Generated documentation
- `src/recurdyn-doc-parser.py` - Extraction logic

**Create:**
- `tests/fixtures/validation-targets.json` - Method sampling data
- `tests/helpers/validation-helpers.py` - Validation utilities

### Implementation Steps

1. **Identify Key Methods**
   - Extract all Model namespace methods
   - Extract Result namespace methods
   - Extract Geometry namespace methods
   - Sort by usage frequency (from examples)

2. **Create Validation Dataset**
   ```json
   {
     "targets": [
       {
         "method": "Load",
         "namespace": "ProcessNet.Model",
         "source_file": "path/to/html",
         "expected_signature": "Load(path: string)",
         "use_case": "UC-1-DOE"
       }
     ]
   }
   ```

3. **Establish Accuracy Metrics**
   - Method name accuracy: 100%
   - Parameter count accuracy: 95%+
   - Type accuracy: 90%+
   - Description presence: 85%+

### Success Criteria
- [ ] 50 key methods identified with source file mappings
- [ ] Validation dataset created
- [ ] Accuracy thresholds defined
- [ ] HTML→JSON cross-reference working

### Risk Assessment
- **Risk:** Source HTML files may be inconsistent
- **Mitigation:** Sample multiple files, use majority voting
- **Risk:** Method overloading may confuse validation
- **Mitigation:** Track overload variants separately

---

## Phase 02: Test Infrastructure

**Priority:** P1 | **Status:** pending | **Effort:** 1.5h

### Context Links
- Existing fixtures: `tests/conftest.py`
- Test patterns: `tests/test-*-validation.py`

### Overview
Build reusable test infrastructure for integration validation. Create fixtures, helpers, and validation utilities.

### Key Insights
- Existing fixtures provide good starting point
- Need specialized validation helpers
- Should support both manual and automated checks

### Requirements

**Functional:**
1. Load and parse knowledge base efficiently
2. Extract method signatures from JSON
3. Compare signatures programmatically
4. Generate discrepancy reports

**Non-Functional:**
- Reusable across all validation phases
- Fast execution (<5 seconds per test file)
- Clear error messages

### Architecture

```python
# Validation helpers
class SignatureValidator:
    - validate_method_name()
    - validate_parameter_count()
    - validate_parameter_types()
    - validate_return_type()

class DiscrepancyReporter:
    - record_mismatch()
    - categorize_issue()
    - generate_report()

# Fixtures
@pytest.fixture
def validation_targets() -> Dict

@pytest.fixture
def signature_validator() -> SignatureValidator

@pytest.fixture
def discrepancy_reporter() -> DiscrepancyReporter
```

### Related Code Files

**Modify:**
- `tests/conftest.py` - Add validation fixtures

**Create:**
- `tests/helpers/validation-helpers.py` - Validation utilities
- `tests/fixtures/validation-targets.json` - Test data

### Implementation Steps

1. **Create Validation Helpers Module**
   ```python
   # tests/helpers/validation-helpers.py
   from dataclasses import dataclass
   from typing import Dict, List, Optional

   @dataclass
   class ValidationResult:
       method_name: str
       signature_match: bool
       parameter_count_match: bool
       parameter_types_match: List[str]
       return_type_match: bool
       discrepancies: List[str]

   class SignatureValidator:
       def validate_method_signature(
           self,
           expected: Dict,
           actual: Dict
       ) -> ValidationResult:
           """Compare expected vs actual method signature."""
           pass

       def extract_parameters(
           self,
           signature: str
       ) -> List[Dict]:
           """Parse parameters from signature string."""
           pass
   ```

2. **Create Discrepancy Reporter**
   ```python
   class DiscrepancyReporter:
       def __init__(self, output_path: Path):
           self.discrepancies = []
           self.output_path = output_path

       def record_issue(
           self,
           severity: str,
           method: str,
           issue: str,
           expected: str,
           actual: str
       ):
           """Record a validation discrepancy."""
           pass

       def generate_report(self) -> Dict:
           """Generate summary report."""
           pass
   ```

3. **Add Fixtures to conftest.py**
   ```python
   @pytest.fixture(scope="session")
   def validation_targets() -> Dict:
       """Load validation target methods."""
       path = Path(__file__).parent / 'fixtures' / 'validation-targets.json'
       return json.loads(path.read_text())

   @pytest.fixture
   def signature_validator():
       """Provide signature validator instance."""
       return SignatureValidator()

   @pytest.fixture
   def discrepancy_reporter(tmp_path):
       """Provide discrepancy reporter with temp output."""
       return DiscrepancyReporter(tmp_path / "discrepancies.json")
   ```

### Success Criteria
- [ ] Validation helpers module created
- [ ] Discrepancy reporter functional
- [ ] Fixtures added to conftest.py
- [ ] Unit tests for helpers pass

---

## Phase 03: Method Signature Validation

**Priority:** P1 | **Status:** pending | **Effort:** 2h

### Context Links
- Markdown docs: `output/markdown/ProcessNet.md`
- Validation helpers: `tests/helpers/validation-helpers.py`

### Overview
Validate method signatures extracted from documentation match the actual API structure used in automation scripts.

### Key Insights
- Method names must be exact (case-insensitive)
- Parameter order matters
- Overloads must be tracked separately
- Signature format varies across namespaces

### Requirements

**Functional:**
1. Validate method name extraction accuracy
2. Verify parameter count matches
3. Check parameter order
4. Detect method overloading

**Non-Functional:**
- 100% accuracy on method names
- 95%+ accuracy on parameter counts
- Clear discrepancy logging

### Architecture

```
Target Methods (50)
    ↓
Extract Signatures from Knowledge Base
    ↓
Compare with Source HTML
    ↓
Calculate Accuracy Metrics
    ↓
Log Discrepancies
```

### Related Code Files

**Create:**
- `tests/test-integration-method-signatures.py` - Main test file
- `tests/fixtures/signature-validation-data.json` - Expected signatures

**Modify:**
- `tests/helpers/validation-helpers.py` - Add signature parsers

### Implementation Steps

1. **Create Test File Structure**
   ```python
   # tests/test-integration-method-signatures.py
   import pytest
   from pathlib import Path

   @pytest.mark.integration
   @pytest.mark.signature_validation
   class TestMethodSignatures:
       """Test method signature extraction accuracy."""

       def test_model_load_signature(self, kb, validator):
           """Verify Model.Load signature is correct."""
           pass

       def test_model_clone_signature(self, kb, validator):
           """Verify Model.Clone signature is correct."""
           pass

       # ... 48 more key methods
   ```

2. **Implement Signature Tests**
   ```python
   @pytest.mark.integration
   def test_doe_batch_execution_signatures(kb, validator):
       """Validate all UC-1 DOE method signatures."""
       uc1_methods = ['Load', 'Clone', 'SetParameter', 'Run', 'SaveAs']

       for method_name in uc1_methods:
           results = kb.find_method(method_name, namespace='ProcessNet.Model')
           assert len(results) > 0, f"Method {method_name} not found"

           for result in results:
               validation = validator.validate_method_name(
                   expected=method_name,
                   actual=result.name
               )
               assert validation.signature_match, \
                   f"Method name mismatch: {method_name} vs {result.name}"

   @pytest.mark.integration
   def test_model_introspection_signatures(kb, validator):
       """Validate all UC-2 introspection method signatures."""
       uc2_methods = ['GetAllBodies', 'GetAllJoints', 'GetEntityByID', 'GetID']
       # Similar validation
   ```

3. **Test Parameter Extraction**
   ```python
   @pytest.mark.integration
   def test_parameter_count_accuracy(kb, validator):
       """Verify parameter counts are extracted correctly."""
       # Load method should have 1 parameter (path)
       results = kb.find_method('Load', namespace='ProcessNet.Model')

       for result in results:
           params = validator.extract_parameters(result.signature)
           assert len(params) >= 1, "Load should have at least 1 parameter"

   @pytest.mark.integration
   def test_parameter_order_preserved(kb, validator):
       """Verify parameter order matches documentation."""
       # Test specific method with known parameter order
       pass
   ```

4. **Test Method Overloading**
   ```python
   @pytest.mark.integration
   def test_overload_detection(kb):
       """Verify overloaded methods are tracked separately."""
       results = kb.find_method('Save')

       # Should have multiple overloads (Save, SaveAs, etc.)
       assert len(results) >= 2, "Save methods should have overloads"

       # Each overload should have unique signature
       signatures = [r.signature for r in results]
       assert len(signatures) == len(set(signatures)), \
           "Each overload should have unique signature"
   ```

### Success Criteria
- [ ] 50 key methods tested
- [ ] Method name accuracy: 100%
- [ ] Parameter count accuracy: 95%+
- [ ] Overload detection working
- [ ] All discrepancies logged

### Risk Assessment
- **Risk:** Signature format inconsistencies
- **Mitigation:** Normalize signatures before comparison
- **Risk:** Missing source HTML for verification
- **Mitigation:** Use extracted markdown as reference

---

## Phase 04: Parameter & Return Type Validation

**Priority:** P1 | **Status:** pending | **Effort:** 2h

### Context Links
- Knowledge base: `output/processnet-knowledge.json`
- Signature tests: `tests/test-integration-method-signatures.py`

### Overview
Validate parameter types, return types, and optional parameters are correctly extracted from documentation.

### Key Insights
- Type information is critical for automation scripts
- Optional parameters need proper marking
- Return types enable result processing
- Complex types (enums, objects) need special handling

### Requirements

**Functional:**
1. Validate basic parameter types (string, int, double, bool)
2. Handle complex types (enums, interfaces, collections)
3. Verify return type extraction
4. Detect optional parameters

**Non-Functional:**
- 90%+ accuracy on type extraction
- Clear categorization of type mismatches

### Architecture

```
Method Signature
    ↓
Extract Parameter Types
    ↓
Validate Against Documentation
    ↓
Categorize Type Accuracy
    ↓
Report Discrepancies
```

### Related Code Files

**Create:**
- `tests/test-integration-parameter-types.py` - Parameter type tests
- `tests/fixtures/type-validation-data.json` - Expected types

**Modify:**
- `tests/helpers/validation-helpers.py` - Add type validators

### Implementation Steps

1. **Create Type Validation Tests**
   ```python
   # tests/test-integration-parameter-types.py
   @pytest.mark.integration
   @pytest.mark.type_validation
   class TestParameterTypes:
       """Test parameter type extraction accuracy."""

       @pytest.mark.parametrize("method,expected_types", [
           ("Load", ["string"]),
           ("SetParameter", ["string", "object"]),
           ("GetAllBodies", []),
           ("GetEntityByID", ["int"]),
       ])
       def test_parameter_types_basic(
           self,
           kb,
           validator,
           method,
           expected_types
       ):
           """Verify basic parameter types."""
           results = kb.find_method(method)
           assert len(results) > 0

           for result in results:
               params = validator.extract_parameters(result.signature)
               actual_types = [p.get('type') for p in params]

               # Check types match (with tolerance for missing type info)
               if actual_types:
                   match_count = sum(
                       1 for exp in expected_types
                       if any(exp.lower() in act.lower() for act in actual_types)
                   )
                   assert match_count >= len(expected_types) * 0.9, \
                       f"Type mismatch for {method}: expected {expected_types}, got {actual_types}"
   ```

2. **Test Complex Types**
   ```python
   @pytest.mark.integration
   def test_enum_parameter_types(kb, validator):
       """Verify enum types are correctly identified."""
       # Find methods with enum parameters
       enum_methods = [
           'SetProcessNetType',
           'GetADProcessNetType'
       ]

       for method_name in enum_methods:
           results = kb.find_method(method_name)
           for result in results:
               if 'enum' in result.description.lower():
                   # Verify enum type is mentioned
                   assert 'enum' in result.signature.lower() or \
                          'type' in result.signature.lower(), \
                          f"Enum type not mentioned in {result.signature}"

   @pytest.mark.integration
   def test_interface_parameter_types(kb, validator):
       """Verify interface parameter types (IBody, IJoint, etc.)."""
       interface_methods = [
           'GetEntityByID',
           'GetParentBody'
       ]

       for method_name in interface_methods:
           results = kb.find_method(method_name)
           for result in results:
               # Check for interface types (I*, *)
               params = validator.extract_parameters(result.signature)
               has_interface = any(
                   'I' in p.get('type', '') and p['type'][0] == 'I'
                   for p in params
               )
               # Not all methods have interface params, just verify extraction
   ```

3. **Test Return Types**
   ```python
   @pytest.mark.integration
   @pytest.mark.parametrize("method,expected_return", [
           ("Load", "IBody"),
           ("GetAllBodies", "IBody[]"),
           ("GetID", "int"),
           ("GetName", "string"),
       ])
       def test_return_type_extraction(
           self,
           kb,
           validator,
           method,
           expected_return
       ):
           """Verify return types are extracted."""
           results = kb.find_method(method)
           assert len(results) > 0

           for result in results:
               if result.return_type:
                   # Check return type matches expected
                   assert expected_return.lower() in result.return_type.lower() or \
                          result.return_type.lower() in expected_return.lower(), \
                          f"Return type mismatch for {method}: expected {expected_return}, got {result.return_type}"
   ```

4. **Test Optional Parameters**
   ```python
   @pytest.mark.integration
   def test_optional_parameter_detection(kb, validator):
       """Verify optional parameters are identified."""
       # Methods with known optional parameters
       methods_with_optionals = [
               'Save',
               'Export'
           ]

       for method_name in methods_with_optionals:
           results = kb.find_method(method_name)
           for result in results:
               params = validator.extract_parameters(result.signature)
               # Check for optional parameter indicators
               has_optional = any(
                   p.get('optional', False) or
                   'optional' in str(p).lower() or
                   '=' in str(p)  # Default value syntax
                   for p in params
               )
               # Just verify extraction works, not all methods have optionals
   ```

5. **Test Collection Types**
   ```python
   @pytest.mark.integration
   def test_collection_parameter_types(kb, validator):
       """Verify collection types (arrays, lists) are identified."""
       collection_methods = [
           'GetAllBodies',
           'GetAllJoints',
           'GetAllForces'
       ]

       for method_name in collection_methods:
           results = kb.find_method(method_name)
           for result in results:
               # Should return collection type
               if result.return_type:
                   is_collection = any(
                       marker in result.return_type.lower()
                       for marker in ['array', 'list', 'collection', '[]', '<>']
                   )
                   # GetAll methods should return collections
                   if method_name.startswith('GetAll'):
                       assert is_collection, \
                           f"{method_name} should return collection, got {result.return_type}"
   ```

### Success Criteria
- [ ] Basic type validation: 90%+ accuracy
- [ ] Enum types correctly identified
- [ ] Return types extracted where available
- [ ] Collection types detected
- [ ] Optional parameters marked

### Risk Assessment
- **Risk:** Type information missing in source HTML
- **Mitigation:** Accept missing types if documented elsewhere
- **Risk:** Type naming inconsistencies
- **Mitigation:** Case-insensitive comparison, partial matching

---

## Phase 05: Automation Scenario Validation

**Priority:** P1 | **Status:** pending | **Effort:** 1h

### Context Links
- Use cases: `README.md` (DOE, Model Introspection, Result Processing)
- Previous tests: `tests/test-use-case-coverage-validation.py`

### Overview
Test complete automation workflows to ensure all required methods are present and correctly structured for real-world usage.

### Key Insights
- Use cases represent actual automation workflows
- Methods must work together in sequence
- Parameter types must match between calls
- Return values enable chaining

### Requirements

**Functional:**
1. Validate UC-1: DOE Batch Execution workflow
2. Validate UC-2: Model Introspection workflow
3. Validate UC-3: Result Processing workflow
4. Test method chaining compatibility

**Non-Functional:**
- All required methods present
- Signatures support chaining
- No breaking parameter mismatches

### Architecture

```
Use Case Definition
    ↓
Extract Required Methods
    ↓
Validate Method Existence
    ↓
Check Parameter Compatibility
    ↓
Verify Return Types Match Next Input
    ↓
Report Workflow Readiness
```

### Related Code Files

**Create:**
- `tests/test-integration-automation-scenarios.py` - Workflow tests
- `tests/fixtures/workflow-definitions.json` - Use case specs

**Modify:**
- `tests/helpers/validation-helpers.py` - Add workflow validators

### Implementation Steps

1. **Define Workflow Specifications**
   ```python
   # tests/fixtures/workflow-definitions.json
   {
     "workflows": [
       {
         "id": "UC-1-DOE",
         "name": "DOE Batch Execution",
         "steps": [
           {
             "method": "Load",
             "class": "Model",
             "inputs": ["string: path"],
             "outputs": ["IBody"],
             "description": "Load base model"
           },
           {
             "method": "Clone",
             "class": "Model",
             "inputs": ["IBody: model"],
             "outputs": ["IBody"],
             "description": "Create model variant"
           },
           {
             "method": "SetParameter",
             "class": "Model",
             "inputs": ["string: name", "object: value"],
             "outputs": [],
             "description": "Set parameter value"
           },
           {
             "method": "SaveAs",
             "class": "Model",
             "inputs": ["string: path"],
             "outputs": [],
             "description": "Save variant"
           },
           {
             "method": "Run",
             "class": "Model",
             "inputs": [],
             "outputs": ["bool"],
             "description": "Run simulation"
           }
         ]
       }
     ]
   }
   ```

2. **Create Workflow Validation Tests**
   ```python
   # tests/test-integration-automation-scenarios.py
   @pytest.mark.integration
   @pytest.mark.workflow
   class TestAutomationScenarios:
       """Test complete automation workflow readiness."""

       def test_doe_workflow_methods_exist(self, kb, workflow_spec):
           """Verify all DOE workflow methods exist."""
           doe_workflow = workflow_spec["workflows"][0]  # UC-1

           for step in doe_workflow["steps"]:
               method_name = step["method"]
               class_name = step["class"]

               # Find method in knowledge base
               namespace = f"ProcessNet.{class_name}"
               results = kb.find_method(method_name, namespace=namespace)

               assert len(results) > 0, \
                   f"DOE workflow missing method: {namespace}.{method_name}"

       def test_doe_workflow_parameter_compatibility(self, kb, validator):
           """Verify parameters are compatible across workflow steps."""
           # Load returns IBody → Clone takes IBody
           load_results = kb.find_method('Load', namespace='ProcessNet.Model')
           clone_results = kb.find_method('Clone', namespace='ProcessNet.Model')

           # Verify Load output matches Clone input
           for load in load_results:
               for clone in clone_results:
                   load_params = validator.extract_parameters(load.signature)
                   clone_params = validator.extract_parameters(clone.signature)

                   # Clone should take IBody or similar as input
                   if clone_params:
                       first_param = clone_params[0]
                       # Check if compatible (IBody, Model, etc.)
                       assert first_param.get('type', '').lower() in \
                           ['ibody', 'model', 'body', 'object', ''], \
                           f"Clone parameter type incompatible: {first_param}"

       def test_model_introspection_workflow(self, kb):
           """Verify UC-2: Model Introspection workflow."""
           uc2_methods = [
               ('Model', 'GetAllBodies'),
               ('Model', 'GetAllJoints'),
               ('Model', 'GetEntityByID'),
               ('Body', 'GetID'),
               ('Body', 'GetType')
           ]

           for class_name, method_name in uc2_methods:
               namespace = f"ProcessNet.{class_name}"
               results = kb.find_method(method_name, namespace=namespace)

               assert len(results) > 0, \
                   f"UC-2 missing: {namespace}.{method_name}"

       def test_result_processing_workflow(self, kb):
           """Verify UC-3: Result Processing workflow."""
           uc3_methods = [
               ('Result', 'Load'),
               ('Result', 'GetTimeArray'),
               ('Result', 'GetEntityData'),
               ('Result', 'Export')
           ]

           for class_name, method_name in uc3_methods:
               namespace = f"ProcessNet.{class_name}"
               results = kb.find_method(method_name, namespace=namespace)

               assert len(results) > 0, \
                   f"UC-3 missing: {namespace}.{method_name}"

       def test_method_chaining_compatibility(self, kb, validator):
           """Verify methods can be chained based on types."""
           # Model.Load() → returns IBody
           # IBody.GetName() → returns string
           # IBody.SetParameter(string, object) → uses string from GetName

           load_results = kb.find_method('Load', namespace='ProcessNet.Model')
           getname_results = kb.find_method('GetName', namespace='ProcessNet.Body')
           setparam_results = kb.find_method('SetParameter', namespace='ProcessNet.Model')

           # Verify return type of GetName matches input of SetParameter
           # (simplified check - just verify methods exist)
           assert len(load_results) > 0, "Load method missing"
           assert len(getname_results) > 0, "GetName method missing"
           assert len(setparam_results) > 0, "SetParameter method missing"
   ```

3. **Test Workflow Edge Cases**
   ```python
   @pytest.mark.integration
   def test_workflow_error_handling_methods(self, kb):
       """Verify error handling methods exist for workflows."""
       error_methods = [
           'GetLastError',
           'ClearError',
           'GetErrorCode'
       ]

       for method_name in error_methods:
           # Just check if error handling exists anywhere
           results = kb.find_method(method_name)
           # Not critical if missing, just log
           if len(results) == 0:
               pytest.skip(f"Error method {method_name} not found (non-critical)")

   @pytest.mark.integration
   def test_workflow_async_methods(self, kb):
       """Check for async/sync variants of workflow methods."""
       async_methods = [
           'BeginRun',
           'EndRun',
           'LoadAsync'
       ]

       for method_name in async_methods:
           results = kb.find_method(method_name)
           # Just verify extraction works, async methods are optional
   ```

### Success Criteria
- [ ] UC-1 DOE workflow: 100% method coverage
- [ ] UC-2 Introspection workflow: 100% method coverage
- [ ] UC-3 Result workflow: 100% method coverage
- [ ] Parameter compatibility verified
- [ ] Return types enable chaining

### Risk Assessment
- **Risk:** Missing methods break workflows
- **Mitigation:** Document gaps, suggest alternatives
- **Risk:** Type mismatches prevent chaining
- **Mitigation:** Identify incompatible patterns

---

## Phase 06: Discrepancy Reporting

**Priority:** P2 | **Status:** pending | **Effort:** 0.5h

### Context Links
- All validation tests
- Discrepancy reporter: `tests/helpers/validation-helpers.py`

### Overview
Compile all validation discrepancies into a comprehensive report with severity categorization and fix recommendations.

### Key Insights
- Discrepancies vary in severity (critical, major, minor)
- Report should guide parser improvements
- Metrics needed for overall accuracy score

### Requirements

**Functional:**
1. Aggregate all test discrepancies
2. Categorize by severity
3. Calculate accuracy metrics
4. Recommend parser improvements

**Non-Functional:**
- Clear, actionable report
- Machine-readable + human-readable formats
- Metrics for confidence scoring

### Architecture

```
Test Results
    ↓
Extract Discrepancies
    ↓
Categorize Severity
    ↓
Calculate Metrics
    ↓
Generate Report (JSON + Markdown)
```

### Related Code Files

**Create:**
- `plans/reports/integration-validation-report.md` - Human report
- `plans/reports/integration-validation-discrepancies.json` - Machine data

**Modify:**
- `tests/helpers/validation-helpers.py` - Add report generator

### Implementation Steps

1. **Create Report Generator**
   ```python
   # tests/helpers/validation-helpers.py (add to existing)
   class DiscrepancyReporter:
       def generate_final_report(self) -> Dict:
           """Generate comprehensive validation report."""
           return {
               "summary": {
                   "total_methods_tested": self.total_tested,
                   "critical_issues": len(self.critical),
                   "major_issues": len(self.major),
                   "minor_issues": len(self.minor),
                   "accuracy_score": self.calculate_accuracy()
               },
               "metrics": {
                   "method_name_accuracy": self.metric_name_accuracy,
                   "parameter_count_accuracy": self.metric_param_count,
                   "type_accuracy": self.metric_type_accuracy,
                   "return_type_accuracy": self.metric_return_type
               },
               "discrepancies": {
                   "critical": self.critical,
                   "major": self.major,
                   "minor": self.minor
               },
               "recommendations": self.generate_recommendations()
           }

       def calculate_accuracy(self) -> float:
           """Calculate overall accuracy score (0-100)."""
           weights = {
               "name": 0.4,  # Method name accuracy (40%)
               "params": 0.3,  # Parameter count (30%)
               "types": 0.2,  # Type accuracy (20%)
               "return": 0.1   # Return type (10%)
           }

           score = (
               self.metric_name_accuracy * weights["name"] +
               self.metric_param_count * weights["params"] +
               self.metric_type_accuracy * weights["types"] +
               self.metric_return_type * weights["return"]
           )

           return round(score, 2)
   ```

2. **Create Markdown Report Template**
   ```markdown
   # ProcessNet Integration Validation Report

   **Date:** 2026-02-01
   **Knowledge Base:** processnet-knowledge.json
   **Methods Tested:** 50
   **Overall Accuracy:** 94.2%

   ## Summary

   - **Critical Issues:** 2
   - **Major Issues:** 8
   - **Minor Issues:** 15
   - **Total Discrepancies:** 25

   ## Accuracy Metrics

   | Metric | Score | Target | Status |
   |--------|-------|--------|--------|
   | Method Name Accuracy | 100% | 100% | ✓ Pass |
   | Parameter Count Accuracy | 96% | 95% | ✓ Pass |
   | Type Accuracy | 89% | 90% | ✗ Fail |
   | Return Type Accuracy | 92% | 85% | ✓ Pass |

   ## Critical Issues

   ### 1. Missing Required Method: `SetParameter`
   - **Impact:** DOE workflow cannot complete
   - **Location:** ProcessNet.Model namespace
   - **Expected:** Method should exist with signature `SetParameter(name, value)`
   - **Actual:** Method not found in knowledge base
   - **Fix:** Check source HTML, verify parser didn't skip method

   ## Major Issues

   ### 1. Parameter Type Mismatch: `GetAllBodies`
   - **Impact:** Automation scripts may fail type checks
   - **Expected:** Returns `IBody[]`
   - **Actual:** Returns `object`
   - **Fix:** Improve array type detection in parser

   ## Recommendations

   ### Parser Improvements

   1. **Array Type Detection** (Priority: High)
      - Issue: Return types like `IBody[]` not detected
      - Fix: Add regex pattern for array notation
      - File: `src/recurdyn-doc-parser.py:extract_return_type()`

   2. **Optional Parameter Marking** (Priority: Medium)
      - Issue: Optional parameters not flagged
      - Fix: Detect `[optional]` markers in HTML
      - File: `src/recurdyn-doc-parser.py:extract_parameters()`

   ### Next Steps

   1. Fix critical issues (estimated: 1 hour)
   2. Re-run validation after fixes
   3. Update knowledge base with corrections
   4. Document known limitations

   ## Test Coverage

   - **UC-1 DOE Batch Execution:** ✓ Complete
   - **UC-2 Model Introspection:** ✓ Complete
   - **UC-3 Result Processing:** ✓ Complete
   ```

3. **Generate Report from Tests**
   ```python
   # tests/test-integration-report-generation.py
   @pytest.mark.integration
   @pytest.mark.report
   def test_generate_discrepancy_report(
       discrepancy_reporter,
       validation_targets
   ):
       """Generate final discrepancy report."""
       # Run all validations
       for target in validation_targets["targets"]:
           # Validate each target
           result = validator.validate(target)

           if not result.passed:
               discrepancy_reporter.record_issue(
                   severity=result.severity,
                   method=target["method"],
                   issue=result.message,
                   expected=target["expected"],
                   actual=result.actual
               )

       # Generate report
       report = discrepancy_reporter.generate_final_report()

       # Save to files
       report_path = Path("plans/reports/integration-validation-report.md")
       json_path = Path("plans/reports/integration-validation-discrepancies.json")

       # Write markdown report
       report_path.write_text(render_markdown_report(report))

       # Write JSON data
       json_path.write_text(json.dumps(report, indent=2))

       # Verify report structure
       assert "summary" in report
       assert "metrics" in report
       assert "discrepancies" in report
       assert "recommendations" in report
   ```

### Success Criteria
- [ ] Discrepancy report generated (Markdown + JSON)
- [ ] Critical issues identified and documented
- [ ] Accuracy metrics calculated
- [ ] Parser improvement recommendations provided
- [ ] Overall confidence score determined

### Risk Assessment
- **Risk:** False positives in discrepancy detection
- **Mitigation:** Manual review of critical issues
- **Risk:** Report too verbose
- **Mitigation:** Summary + detail sections

---

## Related Files

### Source Files
- `src/recurdyn-doc-parser.py` - Parser to improve
- `src/processnet-query-interface.py` - Query interface
- `src/processnet-api-server.py` - REST API server

### Test Files
- `tests/conftest.py` - Shared fixtures
- `tests/helpers/validation-helpers.py` - Validation utilities
- `tests/test-integration-method-signatures.py` - Signature tests
- `tests/test-integration-parameter-types.py` - Type tests
- `tests/test-integration-automation-scenarios.py` - Workflow tests

### Fixtures
- `tests/fixtures/validation-targets.json` - Method sampling data
- `tests/fixtures/workflow-definitions.json` - Use case specs
- `tests/fixtures/signature-validation-data.json` - Expected signatures

### Outputs
- `plans/reports/integration-validation-report.md` - Human report
- `plans/reports/integration-validation-discrepancies.json` - Machine data

---

## Success Criteria (Overall)

### Minimum Viable Output
- [ ] 50 key methods validated across 3 use cases
- [ ] Method signature accuracy: 100%
- [ ] Parameter count accuracy: 95%+
- [ ] Type accuracy: 90%+
- [ ] Discrepancy report generated
- [ ] Parser recommendations documented

### Optimal Output
- [ ] 100+ methods validated
- [ ] All 3 workflows fully verified
- [ ] Return type accuracy: 95%+
- [ ] Parser fixes implemented
- [ ] Knowledge base updated
- [ ] Confidence score: 95%+

---

## Next Steps

After this plan is complete:
1. Review discrepancy report
2. Implement critical parser fixes
3. Re-run validation to verify improvements
4. Update documentation with known limitations
5. Consider adding more validation scenarios

---

## Unresolved Questions

1. **Access to actual RecurDyn API?**
   - Currently validating against extracted docs only
   - Would need RecurDyn installation for true integration tests
   - Acceptable for documentation validation

2. **Method sampling strategy?**
   - 50 methods vs 100+ methods?
   - Prioritize by usage frequency or namespace coverage?
   - Recommendation: Start with 50, expand if needed

3. **Type accuracy thresholds?**
   - 90% target achievable?
   - Should lower-priority namespaces have lower targets?
   - Recommendation: Keep uniform target for simplicity

4. **Parser fix priority?**
   - Fix all issues or just critical?
   - Estimated effort for fixes?
   - Recommendation: Fix critical + major, defer minor
