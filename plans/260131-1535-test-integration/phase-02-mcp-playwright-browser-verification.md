---
parent: ./plan.md
dependencies: [phase-01-test-infrastructure-setup.md]
---

# Phase 2: MCP Playwright Browser Verification

**Date:** 2026-01-31
**Status:** Pending
**Priority:** P0
**Implementation:** Not Started
**Review:** Not Started

## Context

Integrate MCP Playwright for true browser-based verification as described in hybrid workflow Phases 2 & 5. Enables visual verification, element counting, and screenshot capture.

## Key Insights

From workflow doc:
- Browser verification compares extracted data vs rendered page
- Element counting: methods, properties, examples visible on page
- Signature verification: find exact text in DOM
- Screenshot capture for debugging discrepancies

## Requirements

1. Setup MCP Playwright server connection
2. Implement page navigation to local HTML files
3. Count visible elements (methods, classes, examples)
4. Extract text content for signature matching
5. Capture screenshots for verification reports

## Architecture

```python
# test-browser-verification.py structure
import pytest
from playwright.sync_api import Page

class TestBrowserVerification:
    @pytest.fixture
    def browser_page(self, playwright_mcp):
        """Get page from MCP Playwright."""
        return playwright_mcp.new_page()

    def test_navigate_to_local_html(self, browser_page, sample_file):
        """Open local HTML file in browser."""
        browser_page.goto(f"file://{sample_file}")
        assert browser_page.title()

    def test_count_method_elements(self, browser_page, sample_file):
        """Count method definitions visible on page."""
        browser_page.goto(f"file://{sample_file}")
        methods = browser_page.locator("dt:has-text('()')").count()
        return methods

    def test_extract_signatures(self, browser_page, sample_file):
        """Extract method signatures from rendered DOM."""
        browser_page.goto(f"file://{sample_file}")
        signatures = browser_page.locator("dt").all_text_contents()
        return [s for s in signatures if '(' in s]

    def test_capture_verification_screenshot(self, browser_page, sample_file):
        """Capture screenshot for manual review."""
        browser_page.goto(f"file://{sample_file}")
        browser_page.screenshot(path=f"screenshots/{sample_file.stem}.png")

class TestExtractedVsBrowser:
    def test_method_count_matches(self, extraction_results, browser_counts):
        """Compare extracted count vs browser-visible count."""
        for file, extracted in extraction_results.items():
            browser = browser_counts[file]
            tolerance = browser * 0.2  # ±20%
            assert abs(extracted['methods'] - browser['methods']) <= tolerance

    def test_signature_found_in_browser(self, extraction_results, browser_page):
        """Verify extracted signature exists in rendered page."""
        for method in extraction_results['methods'][:3]:
            locator = browser_page.locator(f"text={method['name']}")
            assert locator.count() > 0
```

## MCP Playwright Integration

### Server Setup

```json
// .mcp/servers.json addition
{
  "playwright": {
    "command": "npx",
    "args": ["@anthropic/mcp-server-playwright"]
  }
}
```

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `playwright_navigate` | Open URL/file in browser |
| `playwright_screenshot` | Capture page screenshot |
| `playwright_click` | Interact with elements |
| `playwright_fill` | Input text (if needed) |
| `playwright_evaluate` | Run JS to extract DOM data |

### Element Selectors for RecurDyn Docs

```python
SELECTORS = {
    "methods": "dt:has-text('()')",  # Method signatures
    "classes": "dl.class dt.sig",     # Class definitions
    "properties": "dl.attribute dt",  # Properties
    "examples": "div.highlight pre",  # Code examples
    "title": "h1, title",             # Page title
}
```

## Related Code Files

- `ProcessNet_Hybrid_Verification_Workflow.md:165-270` - Browser verification protocol
- `ProcessNet_Hybrid_Verification_Workflow.md:525-550` - Spot-check commands

## Implementation Steps

1. Install MCP Playwright server
2. Configure `.mcp/servers.json`
3. Create pytest fixtures for MCP connection
4. Implement navigation tests
5. Implement element counting tests
6. Implement signature extraction tests
7. Implement screenshot capture
8. Add comparison tests (extracted vs browser)

## Todo

- [ ] Install MCP Playwright: `npm install @anthropic/mcp-server-playwright`
- [ ] Configure MCP server in project
- [ ] Create test-browser-verification.py
- [ ] Implement page navigation fixture
- [ ] Add element counting tests
- [ ] Add signature matching tests
- [ ] Add screenshot capture
- [ ] Add extracted vs browser comparison

## Success Criteria

- [ ] MCP Playwright connects successfully
- [ ] Local HTML files open in browser
- [ ] Element counts match expected (±20%)
- [ ] Signatures found in rendered DOM
- [ ] Screenshots captured for 5 sample files

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|------------|
| MCP connection issues | High | Fallback to file-based tests |
| File:// URL blocked | Medium | Use local HTTP server |
| JS-rendered content | Medium | Wait for page load complete |
| Selector mismatches | Medium | Inspect actual DOM structure |

## Security Considerations

- Only access local files (no external URLs)
- Screenshots stored locally only
- No sensitive data in test files

## Next Steps

→ Phase 3: Sample extraction tests with browser verification
