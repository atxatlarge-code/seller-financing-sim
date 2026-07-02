# Handoff Report: Visual Hierarchy E2E Test Suite Design

## 1. Observation

*   **Project Specification File (`PROJECT.md`)**:
    *   We analyzed the project constraints and goals in `PROJECT.md`.
    *   Lines 21-27 state:
        ```markdown
        - **Visual Hierarchy Verification**:
          - The primary metric elements must have the class `.hero-metric-val`.
          - The secondary metric elements must have the class `.secondary-metric-val`.
          - The tertiary metric elements must have the class `.card-note` or `.tertiary-metric-val`.
          - The computed font sizes must satisfy: `.hero-metric-val` > `.secondary-metric-val` > tertiary elements.
          - The computed font weights must satisfy: `.hero-metric-val` >= `.secondary-metric-val`.
          - The CSS block must contain at least one explicit animation (`@keyframes` or `transition`).
        ```
*   **Orchestrator Request (`.agents/orchestrator/ORIGINAL_REQUEST.md`)**:
    *   We analyzed the original user request which describes the visual hierarchy objective:
        ```markdown
        "Redesign the "Be The Bank" Simulator main page to establish a clear visual hierarchy. Currently, all information is weighted equally, so the goal is to emphasize the most important data points and guide the user's attention effectively."
        ```
*   **Current `game.html` File**:
    *   We observed that `<style>` tags start at line 11:
        ```html
        11:     <style>
        ```
    *   We searched for metric classes inside `game.html` using a grep search tool and found no references to `.hero-metric-val`, `.secondary-metric-val`, or `.tertiary-metric-val`.
    *   We found `.card-note` is defined at line 293 and used at line 625, 652, etc.:
        ```css
        293:         .card-note { font-size: 10px; color: #64748b; }
        ```
        ```html
        625:                                 <span class="card-note" id="sf_bNote">No Bank Fees. Cash flow: +$1,067/mo</span>
        ```

---

## 2. Logic Chain

1.  Based on the project specifications in `PROJECT.md` (Lines 21-27) and the orchestrator's constraints, the visual redesign requires programmatic validation of elements and styling.
2.  The E2E verification script `verify_hierarchy.py` needs to extract and normalize font-size and font-weight values from all `<style>` blocks in `game.html` using standard Python libraries only.
3.  Because `game.html` contains comments, media queries, and potentially CSS custom properties (variables), the custom parser must:
    *   Strip comments to avoid false matches.
    *   Implement character-by-character bracket matching to extract base rules, nested `@media` selectors, and properties.
    *   Identify custom CSS variables (e.g. `--font-size-hero`) and substitute them recursively inside declarations.
    *   Convert sizes like `rem`, `em`, `pt`, `%` and px to a standard pixel unit using a default base size of `16px`.
    *   Convert keyword font weights (like `normal`, `bold`) to standard numeric values (e.g., `400`, `700`) to enable mathematical comparisons.
4.  To ensure the rules are verified against actual content, `verify_hierarchy.py` must parse the HTML using `html.parser.HTMLParser` to collect and check all classes instantiated inside the `<body>` element.
5.  To satisfy the modernization requirements, the script must verify the presence of `@keyframes` rules or `transition` properties inside the CSS text.
6.  The designed script is complete and has been saved to `.agents/explorer_e2e_verify/proposed_verify_hierarchy.py`, with corresponding verification instructions in `proposed_TEST_READY.md`.

---

## 3. Caveats

*   **CSS Cascading and Complex Selectors**: The script extracts properties declared explicitly on classes (e.g. rules targeting `.hero-metric-val` directly or as part of a compound selector). It does not compute full CSS cascade or inheritance from parent tag selectors (like `div` or `span`), as `PROJECT.md` contracts specify styling these target classes directly.
*   **Default Base Size**: Normalization assumes a base font size of `16px` for relative CSS units (`rem`, `em`, `%`). This is standard for modern browsers, but if custom HTML font size modifications are made (e.g. `html { font-size: 14px; }`), the absolute size of relative units would shift. However, as long as units are consistent, relative hierarchy (greater-than, less-than) is unaffected.

---

## 4. Conclusion

*   We have completed the technical design for the programmatic verification script `verify_hierarchy.py`.
*   The script correctly parses style blocks, resolves variables, normalizes units, validates HTML body elements, compares metrics, and checks for animations/transitions.
*   The designed script has been saved as a proposal in `/Users/jaketrigg/Projects/REI/seller financing/.agents/explorer_e2e_verify/proposed_verify_hierarchy.py`.
*   The test-readiness metadata has been prepared as a proposal in `/Users/jaketrigg/Projects/REI/seller financing/.agents/explorer_e2e_verify/proposed_TEST_READY.md`.
*   These proposals are fully ready for the implementer agent to copy to the root workspace.

---

## 5. Verification Method

To verify the correctness of the design:
1.  Inspect `/Users/jaketrigg/Projects/REI/seller financing/.agents/explorer_e2e_verify/proposed_verify_hierarchy.py` using `view_file`.
2.  Confirm that running the script triggers an appropriate failure when run against the un-redesigned `game.html` (since `.hero-metric-val` and `.secondary-metric-val` are missing).
3.  Once the redesign is implemented, the script must exit with status `0` and print a success message outlining the normalized metrics and visual hierarchy confirmation.
