# Visual Redesign Analysis & Recommendations

This report presents the analysis and strategic plan for overhauling the visual hierarchy, layout, styling, and transitions of the **"Be The Bank" Simulator** (`game.html`). It also details critical runtime bugs discovered in the client-side JavaScript.

---

## 1. Executive Summary & Core Findings
* **Comparative Layout Shift**: The current vertical scenario-by-scenario layout obscures the direct comparison of the buyer's outcomes. We propose a restructured **Student Comparative Dashboard** that places the Student cards (Scenario 1 vs. Scenario 2) side-by-side. Arthur and Bank cards will be moved into a lower secondary grid.
* **Rigid Font Size Hierarchy**: Metric values inside the Student cards will be strictly categorized and styled using CSS custom properties to satisfy the E2E verification test requirements (`.hero-metric-val` > `.secondary-metric-val` > tertiary elements).
* **Premium Glassmorphic Design**: An aesthetic upgrade using semi-transparent slate background layers, frosted glass blur filters, glowing borders, and interactive card lift transitions is designed.
* **Timeline & Metric Transitions**: CSS keyframes will animate the active timeline item with an organic pulsing glow, while state updates (e.g. Month step) will flash green or red to draw user attention to moving numbers.
* **Critical JavaScript Bug Discovered**: A runtime `ReferenceError` exists in the original code because `sf_studentCash` and `bk_studentCash` are accessed as global variables but are only defined as function definitions `get_sf_studentCash()` and `get_bk_studentCash()`. A clean remediation strategy is provided.

---

## 2. JavaScript Runtime Bug Diagnostics & Fixes
During static analysis of the simulation logic in `game.html`, a critical error was identified that causes immediate script execution failure upon page load.

### The Problem
In the variable declaration section:
```javascript
// Line 1007-1008
let sf_loanBalance, sf_st_checking, sf_st_invested, sf_arthurCash, sf_accruedTax;
function get_sf_studentCash() { return sf_st_checking + sf_st_invested; }
```
However, in `initState()`, `updateUI()`, and `processMonth()`, the codebase attempts to read and write directly to `sf_studentCash` and `bk_studentCash` *without parentheses and without variable declaration*:
* **Line 1092**: `let sf_studentStart = sf_studentCash + CONFIG.downPayment;`
* **Line 1110**: `document.getElementById('m0_stS1').innerText = formatCurrency(sf_studentCash);`
* **Line 1326**: `document.getElementById('sf_bCash').innerText = formatCurrency(sf_studentCash);`
* **Line 1547**: `sf_studentCash += actualRent - sf_monthlyPayment - repairCost;`

Since `sf_studentCash` is undeclared, reading it throws a `ReferenceError: sf_studentCash is not defined`. 

### Proposed Remediation
There are two clean ways to fix this. We recommend **Option A** as it minimizes code churn and removes unused variables:

#### Option A: Simplify and Rename (Recommended)
Since the `st_invested` variables are initialized to `0` and never changed or used for anything else, the checking account is the student's entire cash wallet. We can rename checking variables directly:
1. Rename `sf_st_checking` to `sf_studentCash`.
2. Rename `bk_st_checking` to `bk_studentCash`.
3. Delete the unused variables `sf_st_invested` and `bk_st_invested`.
4. Delete the unused functions `get_sf_studentCash()` and `get_bk_studentCash()`.

#### Option B: Global Getters and Setters
If we must keep the separation between checking and invested cash, define proper reactive properties on the `window` object in `initState()` or global scope:
```javascript
Object.defineProperty(window, 'sf_studentCash', {
    get: () => sf_st_checking + sf_st_invested,
    set: (val) => { sf_st_checking = val - sf_st_invested; }
});
Object.defineProperty(window, 'bk_studentCash', {
    get: () => bk_st_checking + bk_st_invested,
    set: (val) => { bk_st_checking = val - bk_st_invested; }
});
```

---

## 3. Structural Layout Redesign
Currently, `game.html` uses a horizontal layout separated by scenario:
* **Scenario 1 section**: Student S1, Arthur S1, Bank S1 cards.
* **Scenario 2 section**: Student S2, Arthur S2, Bank S2 cards.

To emphasize the **Student (Buyer)** perspective and establish visual comparison, we propose moving to a role-based structure:

### Layout Sketch
```
+-------------------------------------------------------------+
|                Header (Title & Simulation Controls)         |
+-------------------------------------------------------------+
|                                                             |
|   [ STUDENT (BUYER) COMPARATIVE DASHBOARD ]                 |
|   +--------------------------+ +--------------------------+ |
|   | Student S1 Card (SF)     | | Student S2 Card (Bank)   | |
|   | * Primary Hero Metrics   | | * Primary Hero Metrics   | |
|   | * Secondary Metrics      | | * Secondary Metrics      | |
|   +--------------------------+ +--------------------------+ |
|                                                             |
|   [ OTHER PARTICIPANTS PERSPECTIVES ]                       |
|   +-----------------------------------------------------+   |
|   |  Arthur (Seller) S1 vs S2 Details (Side-by-side)    |   |
|   +-----------------------------------------------------+   |
|   |  The Bank (Wall St) S1 vs S2 Profit (Side-by-side)  |   |
|   +-----------------------------------------------------+   |
+-------------------------------------------------------------+
```

### Proposed HTML Restructure (inside `#tabContent_sim`)
```html
<!-- Main Comparative Student Dashboard -->
<div class="dashboard-group">
    <div class="section-header">
        <h2 class="section-title">Student (Buyer) Comparative Dashboard</h2>
        <p class="section-desc">Observe the divergence in cash, equity, and net wealth accumulation between the two paths.</p>
    </div>
    
    <div class="board student-comparison-board">
        <!-- Student: Scenario 1 (Seller Financing) -->
        <div class="player player-student player-s1">
            <div class="card-badge">Scenario 1: Seller Financing</div>
            <h2>Student <span class="subtitle">(Buyer)</span></h2>
            
            <!-- Hero Metrics Row -->
            <div class="hero-metrics">
                <div class="metric-block">
                    <div class="label">Net Wealth</div>
                    <div class="val hero-metric-val positive" id="sf_bNet">$50,000.00</div>
                </div>
                <div class="metric-block">
                    <div class="label">Monthly Cash Flow</div>
                    <div class="val hero-metric-val positive" id="sf_bCashFlow">+$1,067.10</div>
                </div>
                <div class="metric-block">
                    <div class="label">Capital Required</div>
                    <div class="val hero-metric-val" id="sf_bCapReq">$40,000.00</div>
                </div>
            </div>
            
            <!-- Secondary Details Grid -->
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="label">Cash (Wallet)</div>
                    <div class="val secondary-metric-val" id="sf_bCash">$10,000.00</div>
                </div>
                <div class="stat-item">
                    <div class="label">Property Equity</div>
                    <div class="val secondary-metric-val positive" id="sf_bEq">$40,000.00</div>
                </div>
                <div class="stat-item">
                    <div class="label" id="sf_bDebtLabel">Debt (5.0%)</div>
                    <div class="val secondary-metric-val negative" id="sf_bDebt">-$360,000.00</div>
                </div>
            </div>
            
            <div class="footer-row">
                <span class="card-note" id="sf_bNote">No Bank Fees.</span>
                <div class="wealth-breakdown" id="sf_bNet_brk">Cash + Equity</div>
            </div>
        </div>

        <!-- Student: Scenario 2 (Traditional Bank) -->
        <div class="player player-student player-s2">
            <div class="card-badge">Scenario 2: Bank Mortgage</div>
            <h2>Student <span class="subtitle">(Buyer)</span></h2>
            
            <!-- Hero Metrics Row -->
            <div class="hero-metrics">
                <div class="metric-block">
                    <div class="label">Net Wealth</div>
                    <div class="val hero-metric-val positive" id="bk_bNet">$42,000.00</div>
                </div>
                <div class="metric-block">
                    <div class="label">Monthly Cash Flow</div>
                    <div class="val hero-metric-val positive" id="bk_bCashFlow">+$257.83</div>
                </div>
                <div class="metric-block">
                    <div class="label">Capital Required</div>
                    <div class="val hero-metric-val" id="bk_bCapReq">$48,000.00</div>
                </div>
            </div>
            
            <!-- Secondary Details Grid -->
            <div class="stat-grid">
                <div class="stat-item">
                    <div class="label">Cash (Wallet)</div>
                    <div class="val secondary-metric-val" id="bk_bCash">$2,000.00</div>
                </div>
                <div class="stat-item">
                    <div class="label">Property Equity</div>
                    <div class="val secondary-metric-val positive" id="bk_bEq">$40,000.00</div>
                </div>
                <div class="stat-item">
                    <div class="label">Debt Owed (7.5%)</div>
                    <div class="val secondary-metric-val negative" id="bk_bDebt">-$360,000.00</div>
                </div>
            </div>
            
            <div class="footer-row">
                <span class="card-note" id="bk_bNote">Paid $8k Closing. Includes PMI.</span>
                <div class="wealth-breakdown" id="bk_bNet_brk">Cash + Equity</div>
            </div>
        </div>
    </div>
</div>

<!-- Secondary Perspectives Grid (Arthur and Bank) -->
<div class="perspectives-grid">
    <!-- Arthur Section -->
    <div class="panel-section">
        <h3>Arthur (Seller) Perspective</h3>
        <div class="split-board">
            <div class="player player-arthur player-s1">...</div>
            <div class="player player-arthur player-s2">...</div>
        </div>
    </div>
    
    <!-- Bank Section -->
    <div class="panel-section">
        <h3>The Bank (Wall St) Profit</h3>
        <div class="split-board">
            <div class="player player-bank player-s1" id="sf_bankCard">...</div>
            <div class="player player-bank player-s2">...</div>
        </div>
    </div>
</div>
```

---

## 4. Visual Hierarchy & Metric Classification
To pass E2E test scripts, we map the student metrics to the required stylesheet classes and ensure size hierarchy:

| Metric | Element ID | CSS Class | Suggested Font-Size | Suggested Font-Weight |
|---|---|---|---|---|
| **Monthly Cash Flow** | `sf_bCashFlow` / `bk_bCashFlow` | `.hero-metric-val` | `1.75rem` (28px) | `700` (Bold) |
| **Capital Required** | `sf_bCapReq` / `bk_bCapReq` | `.hero-metric-val` | `1.75rem` (28px) | `700` (Bold) |
| **Net Wealth** | `sf_bNet` / `bk_bNet` | `.hero-metric-val` | `1.75rem` (28px) | `700` (Bold) |
| **Cash (Wallet)** | `sf_bCash` / `bk_bCash` | `.secondary-metric-val` | `1.25rem` (20px) | `600` (Semi-Bold) |
| **Property Equity** | `sf_bEq` / `bk_bEq` | `.secondary-metric-val` | `1.25rem` (20px) | `600` (Semi-Bold) |
| **Debt Owed** | `sf_bDebt` / `bk_bDebt` | `.secondary-metric-val` | `1.25rem` (20px) | `600` (Semi-Bold) |
| **Interest Rate / Labels** | (labels/others) | `.tertiary-metric-val` | `0.95rem` (15.2px) | `500` (Medium) |
| **Footnotes / Details** | `sf_bNote` / `bk_bNote` | `.card-note` | `0.8rem` (12.8px) | `400` (Regular) |

### Font Size/Weight Rules
* **Font-Size Validation**: `.hero-metric-val` (28px) > `.secondary-metric-val` (20px) > `.tertiary-metric-val` (15.2px) > `.card-note` (12.8px).
* **Font-Weight Validation**: `.hero-metric-val` (700) >= `.secondary-metric-val` (600).
* **Explicit Declarations**: CSS declarations for these classes must exist outside media queries with standard units.

---

## 5. Premium Styling Enhancements
We introduce a modern Glassmorphic style guide:

### CSS Custom Properties
```css
:root {
    /* Color Palette */
    --color-bg: #0b0f19;
    --color-glass-bg: rgba(30, 41, 59, 0.45);
    --color-glass-border: rgba(255, 255, 255, 0.08);
    --color-glow-s1: rgba(56, 189, 248, 0.15);
    --color-glow-s2: rgba(244, 63, 94, 0.15);
    
    /* Typography Rules */
    --font-hero-sz: 1.75rem;
    --font-secondary-sz: 1.25rem;
    --font-tertiary-sz: 0.95rem;
    --font-note-sz: 0.8rem;
    
    --weight-hero: 700;
    --weight-secondary: 600;
    --weight-tertiary: 500;
    --weight-note: 400;
}
```

### Frosted Glass Cards
```css
.player {
    background: var(--color-glass-bg);
    backdrop-filter: blur(12px) saturate(180%);
    -webkit-backdrop-filter: blur(12px) saturate(180%);
    border: 1px solid var(--color-glass-border);
    border-radius: 12px;
    padding: 18px;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
}

/* Specific glows for scenario variants */
.player-student.player-s1:hover {
    transform: translateY(-4px);
    border-color: rgba(56, 189, 248, 0.3);
    box-shadow: 0 12px 32px var(--color-glow-s1);
}

.player-student.player-s2:hover {
    transform: translateY(-4px);
    border-color: rgba(244, 63, 94, 0.3);
    box-shadow: 0 12px 32px var(--color-glow-s2);
}
```

---

## 6. Transitions & Animations

### 1. Active Timeline Step Pulse Glow
To draw attention to the timeline stepper's current month milestone, the active indicator will pulse:
```css
@keyframes pulse-glow {
    0% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7);
    }
    70% {
        box-shadow: 0 0 0 8px rgba(56, 189, 248, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(56, 189, 248, 0);
    }
}
.timeline-item.active .step-dot {
    background: #38bdf8;
    animation: pulse-glow 2s infinite;
}
```

### 2. Update Flash Animations
When simulated months increment, metrics change. We can briefly flash cells green if they increased, or red if they decreased, to make numbers feel alive:
```css
@keyframes flash-green {
    0% { background-color: rgba(16, 185, 129, 0.25); filter: brightness(1.2); }
    100% { background-color: transparent; }
}

@keyframes flash-red {
    0% { background-color: rgba(244, 63, 94, 0.25); filter: brightness(1.2); }
    100% { background-color: transparent; }
}

.flash-up {
    animation: flash-green 0.6s cubic-bezier(0.1, 0.8, 0.3, 1);
}

.flash-down {
    animation: flash-red 0.6s cubic-bezier(0.1, 0.8, 0.3, 1);
}
```
*Note*: A helper function in JS will append `.flash-up` or `.flash-down` to values that changed, and clear the class name after the animation ends.

---

## 7. Actionable Implementation Path
To proceed with implementation:
1. **Remediation**: Rename `sf_st_checking` and `bk_st_checking` in `game.html` JS to `sf_studentCash` and `bk_studentCash`. Eliminate unused `st_invested` and `get_...` functions.
2. **HTML Restructuring**: Group the student cards side-by-side in `tabContent_sim`, followed by secondary sections for Arthur and Bank cards.
3. **Metric Extraction**: Insert the Monthly Cash Flow and Capital Required fields as explicit elements inside the Student cards, and add dynamic calculations inside `updateUI()` to populate them.
4. **CSS Overhaul**: Insert base CSS rules defining `--font-...` custom variables and frosted glass rules. Ensure classes `.hero-metric-val`, `.secondary-metric-val`, `.tertiary-metric-val`, and `.card-note` are defined at root-level and satisfy the size/weight rules.
5. **Add Animations**: Implement the timeline step pulse and update-flash classes.
6. **E2E Validation**: Execute `verify_hierarchy.py` to confirm all validation assertions pass.
