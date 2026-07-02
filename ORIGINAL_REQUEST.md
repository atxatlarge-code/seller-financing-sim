# Original User Request

## 2026-06-29T12:38:46Z

Redesign the "Be The Bank" Simulator main page to establish a clear visual hierarchy. Currently, all information is weighted equally, so the goal is to emphasize the most important data points and guide the user's attention effectively. Note that the primary user of this simulator is the "Student" (the Buyer).

Working directory: /Users/jaketrigg/Projects/REI/seller financing
Integrity mode: benchmark

## Requirements

### R1. Establish Visual Hierarchy
Overhaul the visual hierarchy of the simulator. The agent team must identify the primary hero metrics—optimizing for the Student's perspective—and emphasize them visually over secondary data.

### R2. Complete Visual Overhaul
Implement a complete visual overhaul using a new layout paradigm, modern UI patterns, and animations to make it feel premium.

## Acceptance Criteria

### Visual Hierarchy (Programmatic)
- [ ] A script (e.g., using Puppeteer/Playwright or simple DOM parsing) verifies that the primary metric element has a significantly larger font size and visual weight than secondary metrics.

### Modernization (Programmatic & Agent)
- [ ] The CSS contains at least one explicit animation (`@keyframes` or `transition`) applied to elements.
- [ ] (Agent-as-judge) An independent evaluator agent confirms the layout uses a modern paradigm (e.g., Grid/Flexbox) and looks like a premium production app rather than a basic prototype.
