# Scope: 'Be The Bank' Simulator Visual Redesign

## Architecture
- **Application**: Single-file web application (`game.html`) containing CSS styles and interactive layout.
- **Goal**: Reorganize the dashboard layout to prioritize the Student (Buyer) perspective, establish a clear visual hierarchy of metrics, and add premium styling/animations.
- **Target Verification**: E2E test suite `verify_hierarchy.py`.

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | Layout Overhaul (S1 vs S2) | Restructure `game.html` to place Student cards side-by-side in a comparative dashboard container, with Arthur and Bank cards as smaller details below or secondary. | None | PLANNED |
| 2 | Visual Hierarchy Metric Inversion | Classify and style primary hero metrics (Monthly Cash Flow, Capital Required, Net Wealth) using `.hero-metric-val`; secondary metrics using `.secondary-metric-val`; and others using `.tertiary-metric-val` or `.card-note`. Ensure font scaling rules pass `verify_hierarchy.py`. | M1 | PLANNED |
| 3 | Premium Styles & Interactions | Add modern UI design variables, frosted-glass styles, hover transitions, active timeline step pulsing, and flash effects on updates. | M2 | PLANNED |

## Interface Contracts
- **Class Hierarchy**:
  - Hero Metrics (`.hero-metric-val`): Font size > Secondary, font weight >= Secondary.
  - Secondary Metrics (`.secondary-metric-val`): Font size > Tertiary.
  - Tertiary / Notes (`.tertiary-metric-val` / `.card-note`).
- **Required Styles**:
  - Must declare base styles for `.hero-metric-val`, `.secondary-metric-val`, `.tertiary-metric-val`, and `.card-note` with explicit `font-size` and `font-weight`.
  - Must use `@keyframes` or `transition`.
