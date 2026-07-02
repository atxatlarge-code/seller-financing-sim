# Redesign Plan: "Be The Bank" Simulator Hierarchy

## Goals
1. Establish a clear visual hierarchy prioritizing the "Student" (Buyer) perspective.
2. Emphasize primary hero metrics visually over secondary data.
3. Overhaul the page layout using modern CSS Grid/Flexbox design paradigms.
4. Add CSS transitions/animations for a premium feel.
5. Create a programmatic verification script checking font size and visual weight differences, and checking for animations.

## Milestones

### Milestone 1: Exploration & Proposal (Current)
- **Objective**: Analyze current `game.html` layout, extract existing metrics, and propose hero/secondary metric hierarchy and modern layout.
- **Verification**: Review explorer findings.

### Milestone 2: E2E Verification Script Setup
- **Objective**: Write the verification script that parses `game.html` (and/or loaded CSS) to check font sizes/weights of metrics and verifies the presence of transitions/animations.
- **Verification**: Run the test script on the original `game.html` to confirm it fails (as expected) or establishes a baseline.

### Milestone 3: Redesign Implementation
- **Objective**: Overhaul the CSS and HTML layout of `game.html` using CSS Grid/Flexbox and CSS transitions/animations.
- **Verification**: Build/run locally and confirm layout updates.

### Milestone 4: Review, Challenge & Audit
- **Objective**: Run reviewer, challenger, and forensic auditor agents to ensure visual appeal, programmatic test pass, and integrity.
- **Verification**: Reviewer verdicts, Challenger confirmation, and Auditor clean report.
