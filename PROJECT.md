# Project: "Be The Bank" Simulator Redesign

## Architecture
- **Application Type**: Single-file web application (`game.html`).
- **Data Flow**: Internal simulation logic runs inside client-side JavaScript. UI reads current simulation state and renders participant cards (Student, Arthur, Bank).
- **Redesign Target**: Overhaul the layout and CSS of `game.html` to establish visual hierarchy, prioritizing the Student (Buyer) card metrics.
- **Verification Target**: Programmatic validation of CSS styles and HTML elements using a custom script (`verify_hierarchy.py`).

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | E2E Test Suite | Create `verify_hierarchy.py` and publish `TEST_READY.md` | none | DONE |
| 2 | Redesign Implementation | Implement layout overhaul, premium styles, and animations in `game.html` | M1 | DONE |
| 3 | Verification & Review | Pass E2E verification script, run reviewer/challenger/auditor verification | M1, M2 | DONE |

## Code Layout
- `game.html`: Main simulator web page.
- `verify_hierarchy.py`: E2E test script to verify font sizes, weights, and animations.

## Interface Contracts
- **Visual Hierarchy Verification**:
  - The primary metric elements must have the class `.hero-metric-val`.
  - The secondary metric elements must have the class `.secondary-metric-val`.
  - The tertiary metric elements must have the class `.card-note` or `.tertiary-metric-val`.
  - The computed font sizes must satisfy: `.hero-metric-val` > `.secondary-metric-val` > tertiary elements.
  - The computed font weights must satisfy: `.hero-metric-val` >= `.secondary-metric-val`.
  - The CSS block must contain at least one explicit animation (`@keyframes` or `transition`).
