# Design Specification: 'Be The Bank' Simulator Visual Overhaul

This document details the exact layout, CSS structure, and JavaScript updates required to implement the visual redesign for the simulator.

---

## 1. CSS Custom Properties & Glassmorphic Styling
Add modern CSS variables to `:root` and style target classes to establish the typography hierarchy.

```css
:root {
    --bg-main: #0f172a;
    --bg-panel: rgba(30, 41, 59, 0.7);
    --border-color: rgba(255, 255, 255, 0.08);
    --color-sf: #38bdf8;
    --color-bk: #f43f5e;
    --color-success: #10b981;
    --color-warning: #fbbf24;
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;

    /* Font Sizes (Strict Hierarchy) */
    --font-size-hero: 1.5rem;          /* 24px */
    --font-size-secondary: 1.0625rem;  /* 17px */
    --font-size-tertiary: 0.8125rem;   /* 13px */
    --font-size-note: 0.6875rem;       /* 11px */

    /* Font Weights */
    --font-weight-hero: 700;
    --font-weight-secondary: 600;
    --font-weight-tertiary: 500;
    --font-weight-note: 400;
}

/* Base Typographic Hierarchy classes (checked by verify_hierarchy.py) */
.hero-metric-val {
    font-size: var(--font-size-hero);
    font-weight: var(--font-weight-hero);
    color: var(--color-warning);
}

.secondary-metric-val {
    font-size: var(--font-size-secondary);
    font-weight: var(--font-weight-secondary);
    color: var(--text-primary);
}

.tertiary-metric-val {
    font-size: var(--font-size-tertiary);
    font-weight: var(--font-weight-tertiary);
    color: var(--text-secondary);
}

.card-note {
    font-size: var(--font-size-note);
    font-weight: var(--font-weight-note);
    color: var(--text-muted);
}
```

### Card Layout Rules
- **Student comparison container**: `.student-comparison-grid` uses a two-column grid (`1fr 1fr`) on desktop, gap `20px`.
- **Arthur and Bank detail container**: `.secondary-details-grid` uses a two-column grid (`1fr 1fr`), gap `20px`.
- Inside `.secondary-details-grid`, the Arthur and Bank cards sit side-by-side inside detail columns (subgrid `1fr 1fr`).
- **Glassmorphism classes**: Cards use `backdrop-filter: blur(12px); border: 1px solid var(--border-color); background: var(--bg-panel);`.
- **Card hover scale**:
  ```css
  .comparison-card {
      transition: transform 0.3s cubic-bezier(0.25, 0.8, 0.25, 1), border-color 0.3s, box-shadow 0.3s;
  }
  .comparison-card.sf-theme:hover {
      transform: translateY(-4px);
      border-color: var(--color-sf);
      box-shadow: 0 12px 30px rgba(56, 189, 248, 0.15);
  }
  .comparison-card.bank-theme:hover {
      transform: translateY(-4px);
      border-color: var(--color-bk);
      box-shadow: 0 12px 30px rgba(244, 63, 94, 0.15);
  }
  ```

---

## 2. HTML Structure Restructuring
Inside `#tabContent_sim`, remove the old stacked `.scenario-section` containers and replace them with:

```html
<!-- Primary Student Comparison Dashboard -->
<div class="student-comparison-grid">
    <!-- Student: S1 (Seller Financing) -->
    <div class="player player-student comparison-card sf-theme">
        <div class="card-badge sf-badge">Scenario 1: Seller Financing</div>
        <h2>Student <span class="subtitle">(Buyer)</span></h2>
        
        <!-- Hero Metrics Row -->
        <div class="hero-metrics">
            <div class="metric-block">
                <div class="label">Net Wealth</div>
                <div class="hero-metric-val positive" id="sf_bNet">$50,000.00</div>
            </div>
            <div class="metric-block">
                <div class="label">Monthly Cash Flow</div>
                <div class="hero-metric-val positive" id="sf_bCashFlow">+$1,067.10</div>
            </div>
            <div class="metric-block">
                <div class="label">Capital Required</div>
                <div class="hero-metric-val" id="sf_bCapReq">$40,000.00</div>
            </div>
        </div>
        
        <!-- Secondary Metrics Grid -->
        <div class="stat-grid">
            <div class="stat-item">
                <div class="label">Cash (Wallet)</div>
                <div class="secondary-metric-val" id="sf_bCash">$10,000.00</div>
            </div>
            <div class="stat-item">
                <div class="label">Prop Equity</div>
                <div class="secondary-metric-val positive" id="sf_bEq">$40,000.00</div>
            </div>
            <div class="stat-item">
                <div class="label" id="sf_bDebtLabel">Debt (5.0%)</div>
                <div class="secondary-metric-val negative" id="sf_bDebt">-$360,000.00</div>
            </div>
        </div>
        
        <div class="footer-row">
            <span class="card-note" id="sf_bNote">No Bank Fees.</span>
            <div class="wealth-breakdown tertiary-metric-val" id="sf_bNet_brk"></div>
        </div>
    </div>

    <!-- Student: S2 (Bank Mortgage) -->
    <div class="player player-student comparison-card bank-theme">
        <div class="card-badge bank-badge">Scenario 2: Traditional Bank</div>
        <h2>Student <span class="subtitle">(Buyer)</span></h2>
        
        <!-- Hero Metrics Row -->
        <div class="hero-metrics">
            <div class="metric-block">
                <div class="label">Net Wealth</div>
                <div class="hero-metric-val positive" id="bk_bNet">$42,000.00</div>
            </div>
            <div class="metric-block">
                <div class="label">Monthly Cash Flow</div>
                <div class="hero-metric-val positive" id="bk_bCashFlow">+$257.00</div>
            </div>
            <div class="metric-block">
                <div class="label">Capital Required</div>
                <div class="hero-metric-val" id="bk_bCapReq">$48,000.00</div>
            </div>
        </div>
        
        <!-- Secondary Metrics Grid -->
        <div class="stat-grid">
            <div class="stat-item">
                <div class="label">Cash (Wallet)</div>
                <div class="secondary-metric-val" id="bk_bCash">$2,000.00</div>
            </div>
            <div class="stat-item">
                <div class="label">Prop Equity</div>
                <div class="secondary-metric-val positive" id="bk_bEq">$40,000.00</div>
            </div>
            <div class="stat-item">
                <div class="label">Debt Owed (7.5%)</div>
                <div class="secondary-metric-val negative" id="bk_bDebt">-$360,000.00</div>
            </div>
        </div>
        
        <div class="footer-row">
            <span class="card-note" id="bk_bNote">Paid $8k Closing.</span>
            <div class="wealth-breakdown tertiary-metric-val" id="bk_bNet_brk"></div>
        </div>
    </div>
</div>

<!-- Secondary Details Grid (Arthur & Bank) -->
<div class="secondary-details-grid">
    <!-- S1 Details -->
    <div class="details-cards-subgrid">
        <!-- Arthur S1 -->
        <div class="player player-arthur mini-card">
            ...
        </div>
        <!-- Bank S1 -->
        <div class="player player-bank mini-card" id="sf_bankCard">
            ...
        </div>
    </div>
    
    <!-- S2 Details -->
    <div class="details-cards-subgrid">
        <!-- Arthur S2 -->
        <div class="player player-arthur mini-card">
            ...
        </div>
        <!-- Bank S2 -->
        <div class="player player-bank mini-card">
            ...
        </div>
    </div>
</div>
```

---

## 3. Dynamic JS Integration & Bug Remediation
1. Declare global variables:
   ```javascript
   let sf_studentCash, bk_studentCash;
   ```
2. Initialize them in `initState()`:
   ```javascript
   sf_studentCash = CONFIG.buyerCash - CONFIG.downPayment;
   bk_studentCash = CONFIG.buyerCash - CONFIG.downPayment - CONFIG.closingCosts;
   ```
3. Update `updateUI()` to calculate and format **Monthly Cash Flow** and **Capital Required** dynamically:
   - S1 Cash Flow: `CONFIG.rent - sf_monthlyPayment`
   - S2 Cash Flow: `CONFIG.rent - bk_monthlyPayment - bk_pmi` (if PMI is active)
   - S1 Cap Req: `CONFIG.downPayment`
   - S2 Cap Req: `CONFIG.downPayment + CONFIG.closingCosts`
4. Wire up `flashElement(el)` on each metric update.
