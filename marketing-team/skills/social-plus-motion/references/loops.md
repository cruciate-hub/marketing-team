# Loops

A loop makes a finished static feel alive. Build it from the **final approved static**: copy the markup between its COMPOSITION markers into the cut, add ids to what moves, drop the static grain SVGs (motion grain is drawn on `kit.fx`). If the static changes later, rebuild the loop before exporting.

## Vocabulary (all periodic in the loop length L, default 6 s)

| Element | Motion | Amount |
|---|---|---|
| Background layer (wall, field, grid) | sway or drift, phase-shifted per row/tile | ±7–14px |
| Largest object | float (and ±0.5° tilt for tilted cards) | ±6px |
| The accent element | press (gaussian bump, scale −3% / +3.5%) then a blue-400 ring that grows and fades | every L/2 |
| Glow | breathe | opacity 0.82 ± 0.15 |
| Paths, connectors | dashes flow along the path via `stroke-dashoffset` (a whole number of dash periods per loop) | |
| Grain (editorial only) | boil | 12/s |

When the image tells a sequence (a path, cause → effect), play it in order each cycle: dots flow, the social signal pops (+8%), then the accent action is pressed and rings.

Nothing else moves: no camera, nothing enters or leaves, no text changes, nothing flashes more than 3×/s.

Examples: `assets/examples/thumbnail-loop.js` (wall + focal post), `assets/examples/thumbnail-loop-flow-path.js` (path: post → product → cart).
