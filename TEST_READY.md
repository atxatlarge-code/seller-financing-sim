# Test Suite Readiness: `verify_hierarchy.py`

This project uses a programmatic E2E verification script to validate visual hierarchy, CSS layout patterns, classes, and animation states.

## Testing Verification Script
The verification script is `verify_hierarchy.py` in the project root.

### How to Run Verification
Execute the script using standard Python 3:

```bash
python3 verify_hierarchy.py
```

### Verification Criteria
1. **HTML Class Existence**:
   - `.hero-metric-val` (required)
   - `.secondary-metric-val` (required)
   - `.card-note` and/or `.tertiary-metric-val` (at least one required)
2. **Visual Hierarchy Rules**:
   - `font-size(.hero-metric-val)` > `font-size(.secondary-metric-val)` > `font-size(tertiary)`
   - `font-weight(.hero-metric-val)` >= `font-weight(.secondary-metric-val)`
3. **Premium Interactions (Animations/Transitions)**:
   - CSS must contain at least one `@keyframes` block or `transition` declaration.
