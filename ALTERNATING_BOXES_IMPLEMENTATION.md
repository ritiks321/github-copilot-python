# Sudoku Grid Alternating Box Colors Implementation

## Overview
The Sudoku grid now displays alternating background colors for the 3×3 sub-squares, matching the standard Sudoku board design. The implementation ensures no visible layout shifts and proper color handling in both light and dark modes.

## Changes Made

### 1. CSS Color Variables (styles.css)

#### Light Mode
- `--cell-light: #ffffff` (pure white for odd-numbered boxes 1, 3, 5, 7)
- `--cell-alternating: #e8e8e8` (light gray for even-numbered boxes 0, 2, 4, 6, 8)

#### Dark Mode
- `--cell-light: #3a3a3a` (light gray for odd-numbered boxes)
- `--cell-alternating: #1f1f1f` (darker gray for even-numbered boxes)

These colors provide clear visual contrast between alternating 3×3 boxes while maintaining readability.

### 2. CSS Rules Reorganization (styles.css)

The CSS rules have been reorganized to establish proper cascading hierarchy:

```css
.sudoku-cell {
    /* Base styling without background */
    /* The background is now provided by box classes */
}

/* Box alternation - lowest priority */
.sudoku-cell.box-0, .sudoku-cell.box-2, .sudoku-cell.box-4, 
.sudoku-cell.box-6, .sudoku-cell.box-8 {
    background: var(--cell-alternating);
}

.sudoku-cell.box-1, .sudoku-cell.box-3, .sudoku-cell.box-5, 
.sudoku-cell.box-7 {
    background: var(--cell-light);
}

/* Special states - override box colors */
.sudoku-cell.prefilled { background: var(--bg-tertiary); }
.sudoku-cell.incorrect { background: var(--incorrect-bg); }
.sudoku-cell.hint { background: var(--hint-bg); }

/* Focus state - highest priority */
.sudoku-cell:focus { background: var(--bg-hover); }
```

### 3. JavaScript Class Management (main.js)

Fixed two critical functions to preserve box classes when updating cell states:

#### checkSolution() Function
**Before:**
```javascript
inp.className = 'sudoku-cell';
if (incorrect.has(idx)) {
  inp.className = 'sudoku-cell incorrect';
}
```

**After:**
```javascript
inp.classList.remove('incorrect', 'hint');
if (incorrect.has(idx)) {
  inp.classList.add('incorrect');
}
```

#### provideHint() Function
**Before:**
```javascript
inp.className = 'sudoku-cell hint';
```

**After:**
```javascript
inp.classList.remove('incorrect');
inp.classList.add('hint');
```

### 4. Existing Implementation Verified

The following was already correctly implemented:
- Box number calculation in `createBoardElement()` function
- Data attributes for box identification (`data-box`)
- Thick borders between 3×3 boxes (3px right/bottom borders at columns/rows 2 and 5)
- Proper prefilled class handling with `className +=` (preserves box class)

## How It Works

### Box Number Calculation
Each cell's box number (0-8) is calculated based on its row and column:
```javascript
const boxRow = Math.floor(i / 3);  // 0, 1, or 2
const boxCol = Math.floor(j / 3);  // 0, 1, or 2
const boxNum = boxRow * 3 + boxCol; // 0-8
```

### Box Pattern
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

Even-numbered boxes (0, 2, 4, 6, 8) use `--cell-alternating` color
Odd-numbered boxes (1, 3, 5, 7) use `--cell-light` color

## No Layout Shifts

The implementation ensures no visible layout shifts because:
1. **Box size remains constant** - All cells maintain their aspect ratio (1:1)
2. **Padding unchanged** - Cells have 0 padding and use `box-sizing: border-box`
3. **Borders unchanged** - Only background colors change
4. **Font sizes unchanged** - Text rendering is unaffected
5. **Smooth transitions** - CSS includes `transition: background 0.2s` for smooth color changes

## CSS Priority (Specificity Order)

1. **.sudoku-cell.box-X** - Base alternating colors (most basic state)
2. **.sudoku-cell.prefilled** - Prefilled number styling
3. **.sudoku-cell.incorrect** - Wrong answer highlighting
4. **.sudoku-cell.hint** - Hint styling
5. **.sudoku-cell:focus** - Focus state (highest priority, always visible)
6. **.sudoku-cell.prefilled:focus**, **.sudoku-cell.incorrect:focus**, **.sudoku-cell.hint:focus** - Special focus states

## Testing Checklist

- [ ] Load the game and verify alternating 3×3 box colors are visible
- [ ] Switch between light and dark mode to verify colors adjust properly
- [ ] Fill in some cells and verify colors remain unchanged
- [ ] Use the "Check Solution" button and verify incorrect cells show red while box colors appear in background
- [ ] Use the "Hint" button and verify hint cells show green while box colors appear in background
- [ ] Tab through cells to verify focus state is clearly visible
- [ ] Verify prefilled cells have distinct styling while maintaining alternating box pattern
- [ ] Resize the browser window to verify layout remains stable

## Browser Compatibility

This implementation uses standard CSS features compatible with all modern browsers:
- CSS Custom Properties (CSS Variables)
- CSS Grid
- CSS Transitions
- ClassList API (JavaScript)

## Notes

- The 3×3 box borders are created using thick borders on columns 2, 5 and rows 2, 5
- Box background colors provide visual grouping without affecting the border structure
- Dark mode automatically adjusts both the text and box colors for optimal contrast
- The hint and incorrect states take priority over box background colors for visibility
