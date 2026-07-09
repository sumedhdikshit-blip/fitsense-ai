# FitSense AI Design System (Whoop Athletic Telemetry)

## Aesthetic: Whoop App (v4.0)
- Personality: High-density athletic dashboard (dark mode focused, flat telemetry).
- Key Rule: Thick, crisp borders (2px solid) replacing drop shadows/elevations.

## Color Tokens (Existing CSS Variables)
- Accent: Green (`#00c853` / light: `#00873c`)
- Border: Grey (`#2c2c2c` / light: `#e2e2e2`)
- Panel Background: Dark grey (`#1a1a1a` / light: `#ffffff`)
- Main Background: Deep black (`#0f0f0f` / light: `#f5f5f7`)
- Text: Main white/black, muted grey (`#aaaaaa` / light: `#555555`)
- Status Alerts:
  - Green (Success): `#00c853` / light: `#00873c`
  - Yellow (Warning): `#ffd600` / light: `#b58900`
  - Red (Danger): `#ff1744` / light: `#d32f2f`
  - Blue (Info): `#29b6f6` / light: `#0288d1`

## Spacing Scale
Modular athletic grid:
- 4px: Extra small gaps, borders
- 8px: Small elements, item-level padding
- 12px: Inner content layout gaps
- 16px: Card inner padding, section gaps
- 24px: Large panel grids, outer margins

## Component Design Guidelines
- Cards/Panels: `border: 2px solid var(--border-color); border-radius: 12px; box-shadow: none; background: var(--panel-bg);`
- Buttons: High-contrast fills, `border: 2px solid transparent` or `border: 2px solid var(--border-color)`. Flat scaling hover transitions.
- Shadows: None (flat athletic HUD style).
