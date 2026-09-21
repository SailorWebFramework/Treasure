# Tailwind CSS v3 Coverage Audit

**Date:** 2026-03-14
**Auditor:** Archie (Architect Agent)
**File:** `Treasure/json/tailwind.json`
**Total entries:** ~1,877 key-value pairs

---

## Executive Summary

The current `tailwind.json` covers roughly **40-45%** of Tailwind CSS v3 utility classes. Coverage is strong in spacing (margin/padding), colors (bg/text/border), flexbox, grid, and transforms. Major gaps exist in **filters, effects (blur/backdrop), accessibility modifiers, aspect-ratio utilities, columns, break-after/before/inside, and the full TW v3 color palette** (missing slate, zinc, neutral, stone, emerald, cyan, sky, violet, rose, fuchsia, amber, lime).

### Quality Issues Found

1. **Typo:** `.place-contant-*` should be `.place-content-*` (lines 711-717)
2. **Typo:** `.divide-doubble` should be `.divide-double` (line 483)
3. **Typo:** `.ring-indingo-100` should be `.ring-indigo-100` (line 1279)
4. **Bug:** `.flex-wrap` maps to `wrap-reverse` instead of `wrap` (line 501)
5. **Bug:** `.h-screen` uses `100vw` instead of `100vh` (line 749)
6. **Inconsistency:** Color palette uses Tailwind v1/v2 hex values (e.g., gray-100: #f7fafc) rather than v3 values (gray-100: #f3f4f6). The 50-shade entries use v3 values. These should be reconciled.
7. **Inconsistency:** Gradient `from-*/to-*/via-*` entries only have 100-shade for most colors + a few named colors. Missing full shade range.
8. **Combined entries:** Some entries combine two classes in one key (e.g., `.flex-grow / .flex-grow-0`, `.table-auto / .table-fixed`). These should be split for clean codegen.
9. **Stale API:** Uses deprecated `.row-gap-*` / `.col-gap-*` instead of v3 `.gap-x-*` / `.gap-y-*` (both present but the old ones should be removed).
10. **Missing `> * + *` selector** on `.space-*` and `.divide-*` entries — they're simplified to just `margin-left`/`margin-top`/`border-width` without the child combinator context.

---

## What's Currently Covered

### Layout
| Category | Status | Notes |
|----------|--------|-------|
| Container | Partial | Has `.container` with breakpoints |
| Box Sizing | Complete | `box-border`, `box-content` |
| Display | Good | `block`, `inline-block`, `inline`, `flex`, `inline-flex`, `grid`, `inline-grid`, `hidden`, `table-*`, `flow-root`, `contents` |
| Float | Complete | `float-left/right/none` |
| Clear | Complete | `clear-left/right/both/none` |
| Object Fit | Complete | `object-contain/cover/fill/none/scale-down` |
| Object Position | Complete | All 9 positions |
| Overflow | Complete | All `overflow-*` variants |
| Overscroll | Partial | Has `contain`, `x-auto`, `x-contain`, `x-none`, `y-auto`, `y-contain`, `y-none`. Missing `overscroll-auto`, `overscroll-none` |
| Position | Complete | `static`, `relative`, `absolute`, `fixed`, `sticky` |
| Top/Right/Bottom/Left | Partial | Has 0, auto, 1, full, and some negative values. Missing 2-64 scale, fractional values |
| Visibility | Complete | `visible`, `invisible` |
| Z-Index | Complete | 0, 10, 20, 30, 40, 50, auto |

### Flexbox & Grid
| Category | Status | Notes |
|----------|--------|-------|
| Flex Direction | Complete | row, row-reverse, col, col-reverse |
| Flex Wrap | Buggy | `.flex-wrap` incorrectly maps to `wrap-reverse` |
| Flex | Complete | `flex-1`, `flex-auto`, `flex-initial`, `flex-none` |
| Flex Grow/Shrink | Complete | Combined in single entries |
| Order | Complete | 1-12, first, last, none |
| Grid Template Columns | Complete | 1-12, none |
| Grid Column Span/Start/End | Complete | Full range |
| Grid Template Rows | Complete | 1-6, none |
| Grid Row Span/Start/End | Complete | Full range |
| Grid Auto Flow | Complete | row, col, dense variants |
| Grid Auto Columns/Rows | Complete | auto, min, max, fr |
| Gap | Good | 0-64 scale + px. Has both old (`row-gap-*`/`col-gap-*`) and new (`gap-x-*`/`gap-y-*`) |
| Justify Content | Complete | start, center, end, between, around |
| Justify Items | Complete | start, center, end, stretch |
| Justify Self | Complete | auto, start, center, end, stretch |
| Align Content | Complete | start, center, end, between, around, evenly |
| Align Items | Complete | stretch, start, center, end, baseline |
| Align Self | Complete | auto, start, center, end, stretch |
| Place Content | Has typo | `place-contant-*` instead of `place-content-*` |
| Place Items | Complete | center, end, start, stretch |
| Place Self | Complete | auto, end, start, stretch |

### Spacing
| Category | Status | Notes |
|----------|--------|-------|
| Padding | Complete | Full 0-64 scale + px, all directions (p, pt, pr, pb, pl, px, py) |
| Margin | Complete | Full 0-64 scale + px + auto, all directions, including negatives |
| Space Between | Complete | Full scale + negatives + reverse |

### Sizing
| Category | Status | Notes |
|----------|--------|-------|
| Width | Good | 0-64 scale + fractions (1/2 through 11/12) + auto, full, screen, px |
| Min-Width | Partial | Only 0, full, min, max |
| Max-Width | Good | 0, xs-7xl, full, screen-*, none, prose, min, max |
| Height | Good | 0-64 scale + auto, px, full, screen |
| Min-Height | Partial | Only 0, full, screen |
| Max-Height | Partial | Only 0, full, screen, px |

### Typography
| Category | Status | Notes |
|----------|--------|-------|
| Font Family | Complete | sans, serif, mono |
| Font Size | Complete | xs through 9xl |
| Font Smoothing | Complete | antialiased, subpixel-antialiased |
| Font Style | Complete | italic, not-italic |
| Font Weight | Complete | hairline through black (100-900) |
| Font Variant Numeric | Partial | lining-nums, normal-nums, oldstyle-nums, stacked-fractions, diagonal-fractions. Missing: proportional-nums, tabular-nums, slashed-zero, ordinal |
| Letter Spacing | Complete | tighter through widest |
| Line Height | Complete | none, tight, snug, normal, relaxed, loose + 3-10 |
| List Style Type | Complete | none, disc, decimal |
| List Style Position | Complete | inside, outside |
| Text Align | Complete | left, center, right, justify |
| Text Color | Good | Full old palette. Missing v3 palette colors |
| Text Decoration | Complete | underline, line-through, no-underline |
| Text Transform | Complete | uppercase, lowercase, capitalize, normal-case |
| Text Opacity | Complete | 0, 25, 50, 75, 100 |
| Vertical Align | Complete | baseline, top, middle, bottom, text-top, text-bottom |
| Whitespace | Complete | normal, no-wrap, pre, pre-line, pre-wrap |
| Word Break | Complete | break-normal, break-words, break-all, truncate |
| Placeholder Color | Partial | Only 600-shade + gray full range |
| Placeholder Opacity | Complete | 0, 25, 50, 75, 100 |

### Backgrounds
| Category | Status | Notes |
|----------|--------|-------|
| BG Attachment | Complete | fixed, local, scroll |
| BG Clip | Complete | border, content, padding, text |
| BG Color | Good | Full old palette + 50 shades. Missing v3 colors |
| BG Opacity | Partial | Only 0, 10, 25, 50, 75, 100. Missing 5, 20, 30, 40, 60, 70, 80, 90, 95 |
| BG Position | Complete | All 9 positions |
| BG Repeat | Complete | repeat, no-repeat, repeat-x, repeat-y, round, space |
| BG Size | Complete | auto, cover, contain |
| BG Image / Gradients | Partial | Has gradient directions. `from-*/to-*/via-*` only have 100-shade |
| BG Origin | Missing | `bg-origin-border`, `bg-origin-padding`, `bg-origin-content` |

### Borders
| Category | Status | Notes |
|----------|--------|-------|
| Border Radius | Complete | Full set including 2xl, 3xl, xl, all corner variants |
| Border Width | Complete | 0, default, 2, 4, 8 + directional |
| Border Color | Good | Full old palette + 50 shades |
| Border Style | Complete | solid, dashed, dotted, double, none |
| Border Opacity | Complete | 0, 25, 50, 75, 100 |
| Border Collapse | Complete | collapse, separate |
| Divide Width | Complete | x/y 0-8 + reverse |
| Divide Color | Partial | Only has some shades per color |
| Divide Style | Complete | solid, dashed, dotted, double, none |
| Divide Opacity | Complete | 0, 25, 50, 75, 100 |
| Ring Width | Partial | Only `ring`, `ring-0`. Missing `ring-1`, `ring-2`, `ring-4`, `ring-8` |
| Ring Color | Partial | Only 100-shade per color |
| Ring Offset Width | Partial | Only `ring-offset-0`. Missing 1, 2, 4, 8 |
| Ring Offset Color | Partial | Only 100-shade per color |
| Ring Opacity | Partial | Only `ring-opacity-0` |
| Outline | Partial | Only `outline-none`, `outline-black`, `outline-white` |

### Effects
| Category | Status | Notes |
|----------|--------|-------|
| Box Shadow | Good | xs, sm, default, md, lg, xl, 2xl, inner, outline, none |
| Opacity | Partial | 0, 10, 25, 50, 75, 100. Missing 5, 20, 30, 40, 60, 70, 80, 90, 95 |
| Mix Blend Mode | **Missing** | All `mix-blend-*` utilities |
| BG Blend Mode | **Missing** | All `bg-blend-*` utilities |

### Filters
| Category | Status | Notes |
|----------|--------|-------|
| Blur | **Missing** | `blur-none`, `blur-sm`, `blur`, `blur-md`, `blur-lg`, etc. |
| Brightness | **Missing** | `brightness-0` through `brightness-200` |
| Contrast | **Missing** | `contrast-0` through `contrast-200` |
| Drop Shadow | **Missing** | `drop-shadow-sm` through `drop-shadow-2xl` |
| Grayscale | **Missing** | `grayscale-0`, `grayscale` |
| Hue Rotate | **Missing** | `hue-rotate-0` through `hue-rotate-180` |
| Invert | **Missing** | `invert-0`, `invert` |
| Saturate | **Missing** | `saturate-0` through `saturate-200` |
| Sepia | **Missing** | `sepia-0`, `sepia` |
| Backdrop Blur | **Missing** | `backdrop-blur-*` |
| Backdrop Brightness | **Missing** | `backdrop-brightness-*` |
| Backdrop Contrast | **Missing** | `backdrop-contrast-*` |
| Backdrop Grayscale | **Missing** | `backdrop-grayscale-*` |
| Backdrop Hue Rotate | **Missing** | `backdrop-hue-rotate-*` |
| Backdrop Invert | **Missing** | `backdrop-invert-*` |
| Backdrop Opacity | **Missing** | `backdrop-opacity-*` |
| Backdrop Saturate | **Missing** | `backdrop-saturate-*` |
| Backdrop Sepia | **Missing** | `backdrop-sepia-*` |

### Transforms
| Category | Status | Notes |
|----------|--------|-------|
| Transform | Complete | `transform`, `transform-none` |
| Transform Origin | Complete | All 9 positions |
| Scale | Complete | 0, 50, 75, 90, 95, 100, 105, 110, 125, 150 + x/y variants |
| Rotate | Complete | 0, 1, 45, 90, 180 + negatives |
| Translate | Complete | Full 0-64 scale + px, 1/2, full + negatives |
| Skew | Complete | 0, 1, 2, 3, 6, 12 + negatives |

### Transitions & Animation
| Category | Status | Notes |
|----------|--------|-------|
| Transition Property | Complete | none, all, default, colors, opacity, shadow, transform |
| Transition Duration | Complete | 75-1000ms |
| Transition Timing | Complete | linear, in, out, in-out |
| Transition Delay | Complete | 75-1000ms |
| Animation | Complete | none, spin, ping, pulse, bounce |

### Interactivity
| Category | Status | Notes |
|----------|--------|-------|
| Appearance | Complete | `appearance-none` |
| Cursor | Partial | auto, default, move, pointer, text, wait, not-allowed. Missing: crosshair, grab, grabbing, help, none, context-menu, cell, etc. |
| Outline | Partial | Only none, black, white |
| Pointer Events | Complete | none, auto |
| Resize | Complete | both, none, y, x |
| User Select | Complete | none, text, all, auto |
| Scroll Behavior | **Missing** | `scroll-auto`, `scroll-smooth` |
| Scroll Margin | **Missing** | Full `scroll-m-*` set |
| Scroll Padding | **Missing** | Full `scroll-p-*` set |
| Scroll Snap Align | **Missing** | `snap-start`, `snap-end`, `snap-center`, `snap-align-none` |
| Scroll Snap Stop | **Missing** | `snap-normal`, `snap-always` |
| Scroll Snap Type | **Missing** | `snap-none`, `snap-x`, `snap-y`, `snap-both`, `snap-mandatory`, `snap-proximity` |
| Touch Action | **Missing** | `touch-auto`, `touch-none`, `touch-pan-x`, etc. |
| Will Change | **Missing** | `will-change-auto`, `will-change-scroll`, `will-change-contents`, `will-change-transform` |

### SVG
| Category | Status | Notes |
|----------|--------|-------|
| Fill | Partial | Only `fill-current` |
| Stroke | Partial | Only `stroke-current`, `stroke-0/1/2` |

### Accessibility
| Category | Status | Notes |
|----------|--------|-------|
| Screen Readers | Complete | `sr-only`, `not-sr-only` |

### Tables
| Category | Status | Notes |
|----------|--------|-------|
| Table Layout | Complete | `table-auto`, `table-fixed` (combined entry) |

---

## What's Completely Missing (by Tailwind v3 Category)

### 1. Filters (HIGH PRIORITY - 18 utility groups)
All filter and backdrop-filter utilities are absent. This is the single largest gap.

### 2. Tailwind v3 Extended Color Palette
Missing entire color families: **slate, zinc, neutral, stone, amber, lime, emerald, cyan, sky, violet, rose, fuchsia**. Each has 50-950 shades across bg, text, border, ring, divide, placeholder, gradient stops.

### 3. Scroll Snap (6 utility groups)
Entire scroll snap API is missing.

### 4. Touch Action
All `touch-*` utilities.

### 5. Will Change
All `will-change-*` utilities.

### 6. Aspect Ratio
`aspect-auto`, `aspect-square`, `aspect-video` (note: the properties.json has `aspect-ratio` as a CSS property, but Tailwind utility shortcuts are absent).

### 7. Columns
`columns-1` through `columns-12`, `columns-auto`, `columns-3xs` through `columns-7xl`.

### 8. Break After/Before/Inside
`break-after-auto`, `break-before-page`, `break-inside-avoid`, etc.

### 9. Box Decoration Break
`box-decoration-clone`, `box-decoration-slice`.

### 10. Isolation
`isolate`, `isolation-auto`.

### 11. Mix/BG Blend Modes
`mix-blend-normal`, `mix-blend-multiply`, etc. `bg-blend-*` variants.

### 12. Content
`content-none` (for pseudo-elements).

### 13. Caret Color
`caret-*` utilities.

### 14. Accent Color
`accent-*` utilities (note: properties.json has `accent-color` but TW shortcuts missing).

### 15. Text Decoration Style/Thickness/Offset
`decoration-solid`, `decoration-dashed`, `decoration-wavy`, `decoration-1`, `underline-offset-*`.

### 16. Text Indent
`indent-0` through `indent-96`.

### 17. Text Overflow
Only `truncate` is present. Missing `text-ellipsis`, `text-clip`.

### 18. Hyphens
`hyphens-none`, `hyphens-manual`, `hyphens-auto`.

---

## Recommendations for Structuring New Entries

### 1. Fix existing bugs first
Before adding new entries, fix the 5 bugs and 3 typos identified above.

### 2. Split combined entries
Entries like `.flex-grow / .flex-grow-0` should become two separate keys for clean Shipwright codegen.

### 3. Update to Tailwind v3 color palette
Reconcile hex values to v3 defaults. Add missing color families (slate, zinc, neutral, stone, amber, lime, emerald, cyan, sky, violet, rose, fuchsia) with full 50-950 shade ranges.

### 4. Add missing categories in priority order

**Phase 1 — High impact, straightforward:**
- Filters (blur, brightness, contrast, grayscale, etc.)
- Backdrop filters
- Mix/BG blend modes
- Aspect ratio utilities
- Columns

**Phase 2 — Interactivity & scroll:**
- Scroll snap utilities
- Scroll margin/padding
- Touch action
- Will change
- Caret color / Accent color

**Phase 3 — Typography refinements:**
- Text decoration style/thickness/offset
- Text indent
- Text overflow (`text-ellipsis`, `text-clip`)
- Hyphens
- Font variant numeric completions

**Phase 4 — Layout edge cases:**
- Break after/before/inside
- Box decoration break
- Isolation
- Content

### 5. Expand opacity scales
Current opacity utilities only cover 0/10/25/50/75/100. Tailwind v3 provides: 0, 5, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 95, 100.

### 6. Expand inset/top/right/bottom/left scales
Currently only 0, 1, auto, full. Should have the full spacing scale (0-96) plus fractional values (1/2, 1/3, 2/3, 1/4, 3/4, full).

### 7. Consider structural refactor
The current flat key-value format doesn't encode metadata (e.g., which CSS property a utility maps to, which responsive/state variants apply). Consider whether `tailwind.json` should adopt a structure closer to `properties.json` — with typed parameters — so Shipwright can generate richer Swift APIs rather than just string literals.

---

## Entry Count Estimates for Full Coverage

| Category | Current | Estimated Missing | Total Needed |
|----------|---------|-------------------|--------------|
| Colors (12 new families x ~10 shades x 6 contexts) | ~700 | ~720 | ~1,420 |
| Filters + Backdrop | 0 | ~120 | ~120 |
| Scroll Snap/Margin/Padding | 0 | ~200 | ~200 |
| Interactivity gaps | ~15 | ~60 | ~75 |
| Typography gaps | ~5 | ~50 | ~55 |
| Layout gaps | ~5 | ~40 | ~45 |
| Opacity scale expansions | ~30 | ~80 | ~110 |
| Inset scale expansions | ~20 | ~150 | ~170 |
| **Total** | **~1,877** | **~1,420** | **~3,300** |

Full Tailwind v3 parity would roughly double the current file size.
