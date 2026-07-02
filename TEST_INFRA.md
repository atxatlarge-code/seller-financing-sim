# Test Infrastructure & Rules

This document outlines the test philosophy, feature inventory, architecture, and verification workflows for the E2E visual hierarchy test suite.

---

## Test Philosophy
Our E2E tests follow these fundamental guidelines:
- **Opaque-box Verification**: The tests run directly on the source files (`game.html`) without spinning up a live browser or heavy automation servers (like Selenium/Playwright). This keeps checks fast, reproducible, and robust.
- **Requirement-driven**: Checks map directly to visual design guidelines, ensuring that critical contrast ratios, typographic scales, and class structures are preserved.
- **Standard-library Based**: The testing harness uses only Python's standard library modules (`re`, `html.parser`, `sys`, `os`). This ensures that the test runner has zero external dependencies, making it extremely fast, portable, and reliable.

---

## Feature Inventory

### 1. Typographic Metrics Hierarchy Rules
To maintain strong visual hierarchy and readability, the typographic styles must respect these rules:
- **Font Size**:
  - The font size of `.hero-metric-val` must be strictly greater than that of `.secondary-metric-val`.
  - The font size of `.secondary-metric-val` must be strictly greater than that of tertiary elements (`.tertiary-metric-val` and `.card-note`).
- **Font Weight**:
  - The font weight (boldness) of `.hero-metric-val` must be greater than or equal to that of `.secondary-metric-val`.

### 2. HTML Class Presence Checks
- The HTML `<body>` must contain elements with the classes:
  - `.hero-metric-val` (e.g., main KPI value)
  - `.secondary-metric-val` (e.g., secondary dashboard metrics)
- The HTML `<body>` must contain elements with at least one of the tertiary classes:
  - `.card-note` (e.g., footnotes, details)
  - `.tertiary-metric-val` (e.g., sub-kpi values)

### 3. Modernization & Animation Requirements
- The stylesheet must contain at least one `@keyframes` block or `transition` property declaration to ensure modern CSS animations/transitions are utilized for UI feedback.

---

## Test Architecture

The testing script `verify_hierarchy.py` processes `game.html` using the following steps:

1. **HTML Style Extraction (`StyleExtractor`)**
   - Implements a subclass of `html.parser.HTMLParser` that monitors the start and end of `<style>` tags.
   - Extracts all CSS text declared in `<style>` blocks.

2. **CSS Text Parsing (`parse_css_text`)**
   - Cleans the raw CSS content by removing CSS comments (`/* ... */`) and normalizing whitespaces.
   - Parses the CSS blocks into structured rule dictionaries containing selectors, media queries, and style properties.
   - Handles nested blocks such as `@media` queries and filters out irrelevant declarations.

3. **CSS Variable Resolution (`resolve_variables`)**
   - Identifies any CSS custom properties (variables starting with `--`).
   - Recursively resolves occurrences of `var(--var-name)` up to a depth limit of 5 nested resolutions to find final values.

4. **Unit Normalization (`convert_unit`, `parse_font_size`, `parse_font_weight`)**
   - Parses font size strings (e.g. `2.5rem`, `24px`, `150%`, `14pt`).
   - Normalizes all sizes to a baseline pixel value (assuming `1rem = 16px`, `1em = 16px`, `100% = 16px`, and `1pt = 1.333px`).
   - Normalizes font weight names (e.g. `normal` to `400`, `bold` to `700`) and parses numeric font weights directly.

5. **HTML Element Parsing (`ClassVerifier`)**
   - Implements a subclass of `html.parser.HTMLParser` that tracks classes on all tags within the HTML `<body>` tags.
   - Aggregates the unique set of classes present in the layout.

6. **Visual Hierarchy Test Suite Execution**
   - Maps resolved CSS styles to active classes found in the HTML body.
   - Performs assertion checks comparing font-sizes and font-weights, failing the build (exiting with code `1`) if any constraint is violated.

---

## Real-World Application Scenarios (Tier 4)
This verification harness is designed to validate the **Visual Hierarchy Redesign (Tier 4)**. 
- During visual redesigns, typography scales are often refactored.
- This opaque-box harness guarantees that updates to variables or new styling blocks do not inadvertently flatten the visual hierarchy, compress typography contrast, or break classes used in layout markup.
- It acts as a gatekeeper in the CI/CD pipeline, catching style regressions before code is pushed to production.

---

## Coverage Thresholds
- **Class Coverage**: 100% of defined target visual hierarchy classes (`.hero-metric-val`, `.secondary-metric-val`, `.tertiary-metric-val`, `.card-note`) must be evaluated.
- **Variable Resolution**: 100% of variables used in font sizing must be successfully resolved to a concrete unit.
- **Execution Success**: Zero failing assertions are tolerated. Any visual hierarchy mismatch or missing animations will cause a test failure.
