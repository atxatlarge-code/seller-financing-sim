# Visual Hierarchy E2E Verification Design & Analysis

## Overview
This document analyzes the E2E verification requirements for the "Be The Bank" Simulator Redesign and provides the design specifications and complete implementation details for `verify_hierarchy.py`.

---

## 1. Verification Requirements

From the project specifications (`PROJECT.md`) and initial request (`ORIGINAL_REQUEST.md`), the E2E verification script must enforce the following constraints:

1. **Element Hierarchy**:
   - Primary metric elements must be styled with the class `.hero-metric-val`.
   - Secondary metric elements must be styled with the class `.secondary-metric-val`.
   - Tertiary elements must use `.card-note` or `.tertiary-metric-val`.
   
2. **Visual Hierarchy Rules**:
   - **Font Size**: `.hero-metric-val` > `.secondary-metric-val` > (`.card-note` / `.tertiary-metric-val`).
   - **Font Weight**: `.hero-metric-val` >= `.secondary-metric-val`.

3. **Modernization & Polish**:
   - The stylesheet must contain at least one `@keyframes` rule (for explicit CSS animations) or `transition` declaration (for hover transitions).

4. **HTML Body Presence**:
   - The verified classes must actually exist in the `<body>` of the `game.html` document.

---

## 2. Technical Design of `verify_hierarchy.py`

To satisfy these rules using only standard Python libraries (`re`, `html.parser`), the script is structured around three key parsing tasks: HTML element traversal, CSS rules extraction, and CSS value normalization.

### 2.1 CSS Rule Extraction
Instead of third-party packages (like `tinycss2` or `cssutils`), we parse the stylesheet using a custom depth-tracking tokenizer. This allows us to correctly handle complex media queries (`@media`) and keyframes:
- **Brace Level Scanner**: By keeping track of character indices and brace depths (`{` and `}`), we can isolate base rules, media-nested rules, and keyframes blocks.
- **Selector Separation**: Comma-separated selectors (e.g. `.class-a, .class-b`) are split to map individual styles to their selectors.
- **Custom Property Resolution**: If styles use CSS variables (e.g., `var(--font-size-hero)`), the script scans all parsed properties starting with `--`, stores them in a variables map, and recursively replaces them (up to 5 levels of nesting).

### 2.2 Property Value Normalization
CSS uses diverse units for font sizes and weights. We programmatically normalize them to standard numeric values for logical comparisons.
- **Font Sizes**: Standard units are converted to absolute pixels (assuming a standard base of `16px` for `rem`, `em`, and `%`):
  - `px` / unitless $\to$ float value.
  - `rem` / `em` $\to$ float value $\times\ 16.0$.
  - `%` $\to$ (float value $/ 100.0$) $\times\ 16.0$.
  - `pt` $\to$ float value $\times\ 1.333$.
  - *Complex Expressions* (e.g., `clamp()`, `calc()`): The script extracts the first matching numeric term as a fallback value.
- **Font Weights**: Keywords are mapped to numeric weights:
  - `normal`, `initial`, `inherit` $\to$ `400`
  - `bold` $\to$ `700`
  - `bolder` $\to$ `800`
  - `lighter` $\to$ `300`
  - Digits (e.g. `600`, `700`) $\to$ `int` value.

### 2.3 HTML Body Parsing
Using Python's standard `html.parser.HTMLParser`:
- `StyleExtractor` gathers all CSS content inside `<style>` tags.
- `ClassVerifier` records all class attributes applied to elements inside the `<body>` tags (ignoring header blocks and metadata).

---

## 3. Implementation Recommendations for the Redesign

To ensure the redesigned `game.html` successfully passes the E2E verification, the implementer agent should execute the following layout changes:

### 3.1 Applying Classes to Player Cards
The redesign target is to prioritize the Student (Buyer) card metrics. We recommend structuring the metrics within the card as follows:

*   **Primary Hero Metric** (`.hero-metric-val`):
    *   **Candidate**: **Net Wealth** (e.g. `$50,000.00`) or **Cash Flow** (e.g. `+$1,067/mo`). Since Net Wealth is the ultimate scorecard metric for the Student, styling this as the hero metric fits the UX.
*   **Secondary Metrics** (`.secondary-metric-val`):
    *   **Candidates**: **Cash (Wallet)**, **Property Equity**, and **Debt**. These details support the Net Wealth metric.
*   **Tertiary Metrics/Notes** (`.card-note` or `.tertiary-metric-val`):
    *   **Candidates**: Individual breakdown explanations, tax notes, or transaction details (e.g., "Paid $8k Closing").

### 3.2 Recommended Stylesheet Configuration
A standard compliant stylesheet set of metrics styles would be:

```css
:root {
  --font-size-hero: 1.5rem;          /* 24px */
  --font-weight-hero: 700;
  
  --font-size-secondary: 1.1rem;     /* 17.6px */
  --font-weight-secondary: 600;
  
  --font-size-tertiary: 0.8rem;      /* 12.8px */
}

/* Applied styles */
.hero-metric-val {
  font-size: var(--font-size-hero);
  font-weight: var(--font-weight-hero);
}

.secondary-metric-val {
  font-size: var(--font-size-secondary);
  font-weight: var(--font-weight-secondary);
}

.card-note, .tertiary-metric-val {
  font-size: var(--font-size-tertiary);
  font-weight: normal; /* default 400 */
}
```

### 3.3 Adding Micro-Interactions (Animations/Transitions)
To pass the premium polish requirement:
*   Add a transition to interactive buttons or cards:
    ```css
    .player {
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .player:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    ```
*   Add a pulsing fade-in keyframe animation for warning alerts or target values:
    ```css
    @keyframes pulse-glow {
      0% { opacity: 0.8; }
      50% { opacity: 1; filter: brightness(1.2); }
      100% { opacity: 0.8; }
    }
    ```

---

## 4. Verification Script Source Code
The script design is fully realized and stored in `.agents/explorer_e2e_verify/proposed_verify_hierarchy.py`. The implementer can copy this script directly to the project root to run checks.
