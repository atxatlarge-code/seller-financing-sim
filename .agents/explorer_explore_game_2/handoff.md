# Handoff Report — Visual Redesign Explorer (Explorer 2)

This handoff report summarizes the findings of our read-only layout, CSS, and structural investigation of `game.html`, and provides a roadmap for the visual hierarchy overhaul implementation.

---

## 1. Observation
*   **Vertical Layout and Code References**: In `/Users/jaketrigg/Projects/REI/seller financing/game.html`, Scenario 1 and Scenario 2 are currently defined as separate, vertically-stacked containers in the live simulator tab (`tabContent_sim`, lines 607–782):
    *   *Scenario 1*: `Scenario 1: Seller Financing (The "Be The Bank" Way)` (line 609).
    *   *Scenario 2*: `Scenario 2: Traditional Bank Mortgage` (line 697).
    Each board uses a 3-column grid structure (line 242): `.board { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }` where the Student, Arthur, and Bank cards are given equal weight and visual size.
*   **Metric Footnotes**: The Buyer's monthly cash flow is a hardcoded text note in the card footer:
    *   `No Bank Fees. Cash flow: +$1,067/mo` (line 630).
    *   `Paid $8k Closing. Cash flow: +$257/mo` (line 718).
*   **Undeclared Variables Bug**: On line 1007, the global variables are declared as:
    `let sf_loanBalance, sf_st_checking, sf_st_invested, sf_arthurCash, sf_accruedTax;`
    `let bk_loanBalance, bk_st_checking, bk_st_invested, bk_arthurCash, bk_accruedTax;`
    On line 1008 and 1015, the getter functions return checking + invested:
    `function get_sf_studentCash() { return sf_st_checking + sf_st_invested; }`
    `function get_bk_studentCash() { return bk_st_checking + bk_st_invested; }`
    However, on line 1092 and 1094:
    `let sf_studentStart = sf_studentCash + CONFIG.downPayment;`
    `let bk_studentStart = bk_studentCash + CONFIG.downPayment;`
    And inside `processMonth` (line 1547 and 1616):
    `sf_studentCash += actualRent - sf_monthlyPayment - repairCost;`
    `bk_studentCash += actualRent - bk_monthlyPayment - bk_pmi - repairCost;`
    Since `sf_studentCash` and `bk_studentCash` are never declared as variables in the `let` statement or properties, this causes a `ReferenceError` on boot.
*   **E2E Test Hierarchy Requirements**: In `/Users/jaketrigg/Projects/REI/seller financing/verify_hierarchy.py`, the following rules are checked (lines 273–290):
    *   `primary_el` (must use `.hero-metric-val`) font size > `secondary_el` (must use `.secondary-metric-val`) font size.
    *   `secondary_el` font size > `tertiary_el` (must use `.card-note` or `.tertiary-metric-val`) font size.
    *   `primary_el` font weight >= `secondary_el` font weight.
    *   Style blocks must contain at least one `@keyframes` or `transition` (line 295–306).

---

## 2. Logic Chain
1.  **Observation on Stacked Cards**: The current layout separates the Student's S1 card and S2 card vertically, making quick comparisons impossible.
2.  **Comparative Proposal**: Restructuring the HTML to place the S1 Student card and S2 Student card side-by-side in a prominent 2-column comparative container (`.comparison-dashboard`) will allow immediate contrast. Arthur and Bank cards can be combined into sub-panels inside a secondary grid below.
3.  **Observation on Metrics Placement**: Critical metrics like cash flow are currently buried inside small footer notes, violating visual hierarchy rules.
4.  **Metric Classification**: We must classify Monthly Cash Flow, Capital Required, and Net Wealth as **Primary Hero Metrics** (using `.hero-metric-val`). Wallet Cash, Property Equity, and Debt Owed are classified as **Secondary Metrics** (using `.secondary-metric-val`). Dynamic footnotes and breakdowns are classified as **Tertiary Metrics** (using `.tertiary-metric-val` or `.card-note`).
5.  **Observation on Undeclared Variables**: The previous refactoring of `studentCash` into checking and invested was left incomplete, leaving `sf_studentCash` and `bk_studentCash` undeclared, resulting in a ReferenceError on load.
6.  **Code Correction Proposal**: Declare `sf_studentCash` and `bk_studentCash` in the global scope (add them to the `let` declaration block) and initialize them in `initState()` to immediately fix the boot crash.
7.  **Observation on Verification Script**: `verify_hierarchy.py` requires size and weight constraints for base CSS selectors.
8.  **CSS Scale Resolution**: Defining base rules for `.hero-metric-val` (`22px`, font-weight `700`), `.secondary-metric-val` (`16px`, font-weight `600`), and `.tertiary-metric-val` (`12px`, font-weight `400`) in the base CSS stylesheet will guarantee the tests pass successfully.

---

## 3. Caveats
*   The actual layout restructuring and styling overrides are out of scope for the Explorer agent and must be executed by the Implementer agent.
*   This report assumes the standard browser font size is 16px (where 1rem = 16px).
*   Any browser caching or local storage that references old state formats should be reset using the "Play Again" or "Reset & Apply" buttons.

---

## 4. Conclusion
The Visual Redesign Explorer recommends:
1.  Fixing the undeclared global variable bugs (`sf_studentCash` / `bk_studentCash`) by declaring and initializing them properly.
2.  Redesigning the HTML to put the two Student cards side-by-side inside a comparative container (`.comparison-dashboard`), and moving Arthur and Bank details to secondary cards below.
3.  Applying `.hero-metric-val`, `.secondary-metric-val`, and `.tertiary-metric-val` / `.card-note` classes to structure the visual hierarchy of the metrics.
4.  Introducing a glassmorphism stylesheet, timeline pulse keyframes, and update flash selectors for premium polish.

---

## 5. Verification Method
1.  Verify the details of this strategy in `/Users/jaketrigg/Projects/REI/seller financing/.agents/explorer_explore_game_2/analysis.md`.
2.  Once changes are implemented by the Implementer, execute `python3 verify_hierarchy.py` from the project root.
3.  Load `game.html` in a web browser to verify there are no ReferenceErrors in the console and that the cards are rendered correctly side-by-side with glassmorphism.
