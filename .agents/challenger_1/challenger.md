# Challenge Report: Visual Redesign & Simulator Logic Verification

## Challenge Summary

**Overall risk assessment**: CRITICAL

The interactive simulator logic in `game.html` has severe runtime and logical defects that break the core user experience. Specifically, there is a blocking JavaScript reference error that crashes the page immediately on load, a logic bug that leaves the student cash metrics static throughout the simulation, and multiple string interpolation syntax bugs that render raw code in UI text strings.

---

## Challenges

### [Critical] Challenge 1: Unhandled Reference Error (`get_sf_studentCash` and `get_bk_studentCash` Not Defined)

- **Assumption challenged**: The page loads and runs interactive simulation steps correctly.
- **Attack scenario**: The browser loads the page and executes `window.onload`, which calls `initState()`.
- **Blast radius**: The execution immediately throws `ReferenceError: get_sf_studentCash is not defined` and aborts. This stops chart initialization, prevents any initial data rendering, and breaks all buttons ("Next Month", "Fast Forward", "Run Full Simulation") because they rely on state initialized by `initState()`.
- **Proof in Code**:
  - In `initState()` (lines 1309-1310):
    ```javascript
    document.getElementById('m0_stS1').innerText = formatCurrency(get_sf_studentCash());
    document.getElementById('m0_stS2').innerText = formatCurrency(get_bk_studentCash());
    ```
  - In `processMonth()` (lines 1864-1865):
    ```javascript
    stS1: get_sf_studentCash() + (propValue - sf_loanBalance), 
    stS2: get_bk_studentCash() + (propValue - bk_loanBalance),
    ```
  - Nowhere in the script block is `get_sf_studentCash()` or `get_bk_studentCash()` defined.
- **Mitigation**: Define the helper functions in the script block (e.g., around line 1216):
  ```javascript
  function get_sf_studentCash() { return sf_st_checking + sf_st_invested; }
  function get_bk_studentCash() { return bk_st_checking + bk_st_invested; }
  ```

### [High] Challenge 2: Static Student Cash in UI Rendering

- **Assumption challenged**: The UI metrics (cash, net wealth) reflect active changes in the simulation.
- **Attack scenario**: The simulation progresses through months, adding rent income, subtracting mortgage payments/repairs, and compounding HYSA interest.
- **Blast radius**: In `processMonth()`, student checking and investment balances (`sf_st_checking`, `sf_st_invested`, `bk_st_checking`, `bk_st_invested`) are updated correctly. However, in `updateUI()`, the displays read from the static variables `sf_studentCash` and `bk_studentCash`, which are never modified during simulation months. Consequently:
  - The displayed "Leftover Cash" (`sf_bCash` / `bk_bCash`) remains stuck at the initial value (e.g., $10,000 / $2,000).
  - The displayed "Net Wealth" (`sf_bNet` / `bk_bNet`) only changes when property equity changes, ignoring all compounded checking/invested cash.
- **Proof in Code**:
  - In `updateUI()` (lines 1544, 1547, 1608, 1611):
    ```javascript
    setAndFlash('sf_bCash', formatCurrency(sf_studentCash));
    ...
    setAndFlash('sf_bNet', formatCurrency(sf_studentCash + sf_studentEquity));
    ...
    setAndFlash('bk_bCash', formatCurrency(bk_studentCash));
    ...
    setAndFlash('bk_bNet', formatCurrency(bk_studentCash + bk_studentEquity));
    ```
- **Mitigation**: Update `updateUI()` to read from the computed getters instead of static variables:
  ```javascript
  setAndFlash('sf_bCash', formatCurrency(get_sf_studentCash()));
  setAndFlash('sf_bNet', formatCurrency(get_sf_studentCash() + sf_studentEquity));
  setAndFlash('bk_bCash', formatCurrency(get_bk_studentCash()));
  setAndFlash('bk_bNet', formatCurrency(get_bk_studentCash() + bk_studentEquity));
  ```

### [Medium] Challenge 3: Syntax Interpolation Anomalies in UI Message Strings

- **Assumption challenged**: UI text displays variables properly formatted to the user.
- **Attack scenario**: The simulation reaches its end or fast-forwards.
- **Blast radius**: Text displayed in the UI contains raw template literals and code constructs because double quotes are used instead of backticks, or because concatenation was mixed up inside template backticks.
- **Proof in Code**:
  - **Double Quote Issue 1 (line 1976)**:
    `updateUI("🏁 Month ${CONFIG.simulationYears * 12} reached! Simulator finished.");`
    Renders as: `🏁 Month ${CONFIG.simulationYears * 12} reached! Simulator finished.`
  - **Double Quote Issue 2 (line 1986)**:
    `updateUI("🏁 Full ${CONFIG.simulationYears}-year simulation complete! Review the results below.");`
    Renders as: `🏁 Full ${CONFIG.simulationYears}-year simulation complete! Review the results below.`
  - **Concatenation Mix-up (line 1750)**:
    ```javascript
    `Student is ${formatCurrency(studentDelta)} wealthier using seller financing over " + CONFIG.simulationYears + " years.`
    ```
    Renders as: `Student is $123,456.78 wealthier using seller financing over " + CONFIG.simulationYears + " years.`
- **Mitigation**:
  - Convert double quotes to backticks for lines 1976 and 1986.
  - Fix line 1750 to use `${CONFIG.simulationYears}`:
    ```javascript
    `Student is ${formatCurrency(studentDelta)} wealthier using seller financing over ${CONFIG.simulationYears} years.`
    ```

---

## Stress Test Results

- **Boot Run (Page Load)** → Expect chart initialization and Year 0 values to load → **FAIL** (Throws `ReferenceError: get_sf_studentCash is not defined` immediately).
- **Interactive Steps (clicking Next Month)** → Expect step execution and UI update → **FAIL** (State uninitialized, throws ReferenceError).
- **Metric Verification (checking student cash)** → Expect cash to compound over time → **FAIL** (Metrics bound to static `sf_studentCash` variable which never changes).

---

## Unchallenged Areas

- **Visual Layout and CSS Styling Rules** — Reason not challenged: Static analysis confirms that classes (`.hero-metric-val`, `.secondary-metric-val`, `.tertiary-metric-val`, `.card-note`), typographic scaling (24px > 17px > 13px > 11px), weights (700 >= 600), and keyframes/transitions are present and properly declared, matching the E2E verification criteria of `verify_hierarchy.py`.
