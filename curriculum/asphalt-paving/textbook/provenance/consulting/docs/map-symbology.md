# Map symbology

Open **Contents → Symbology** for a vector layer or project area. Choose **Single colour** or **Graduated colours**, then adjust the appearance. **Source style** and **Reset style** restore the original presentation.

The editor supports polygon and point fills, line colours, outline colours and widths, separate fill/outline opacity, six preset ramps, two to eight custom ramp colours, reversal, numeric fields, and linear or logarithmic scales. The current indicator option follows the layer's existing year and indicator controls. An explicitly chosen historical field remains available when reopening the editor.

Styles also apply to weather and source-inventory overlays. Project areas have independent styles; changing their appearance does not change their bounds or filters. Raster services retain their Contents opacity control because their rendered imagery cannot be recoloured as vector attributes.

Presentation settings are stored in this browser. Source geometry and attributes are not stored in the preferences or rewritten by styling. Removing layers and Clear map remove the displayed layers; Reset style removes the selected style preference. Transient map-view area preferences are removed when those areas are removed.

## Data behaviour

- Cached features are restyled when they return after filtering. Refreshes retain style settings and use the newly loaded source collection.
- Static economic layers retain domains calculated from their complete loaded source collection, independently of project-area filters. Live layers use the complete collection returned by their bounded query; a subsequent refresh can change that collection and its domain.
- Missing, unavailable and suppressed values retain a separate grey symbol. Unsigned zero retains its separate white symbol. Signed domains use linear scaling and the editor displays the effective scale.
- Numeric field discovery excludes object/array/Boolean coercion. Original fields, scalar types, nulls and native geometry remain intact.
- Line and nested mixed-geometry collections receive their corresponding stroke/fill styles without rebuilding source geometry.
- The storage format validates settings, rejects corrupt snapshots, and handles unavailable browser storage without breaking map interaction.

## Validation

Twenty-eight targeted model, preference-storage and recursive-geometry tests passed. An isolated headless Edge candidate check passed 22 interactions using published data: 13 household-account polygons, 259 native New Brunswick polygons followed by 238 exact source polygons after refresh, 69 inventory polygons and 40 weather observations. It checked filtering, full-source domains, presets/custom/reversed ramps, linear/log and signed behaviour, reload, hide/show, remove/re-add, reset/focus, independent project areas, clear actions and a 390-pixel layout. There were no source-data substitutions, saved source records, screenshots or browser exceptions. Candidate code substitutions are explicitly recorded in [the candidate receipt](evidence/symbology-candidate-2026-10-26.json).

Published in `d253d6515b4c8383a0ca92972091a945c23ccb95` after [full validation](https://github.com/GOSTROGIS/CONSULTING/actions/runs/40266107931), [interface checks](https://github.com/GOSTROGIS/CONSULTING/actions/runs/40266107933), and [Pages deployment](https://github.com/GOSTROGIS/CONSULTING/actions/runs/40266523501) (deployment 7323767707). All 22 checks passed again on the actual public application with zero code/data substitutions and zero browser errors. [Exact public receipt](evidence/symbology-public-2026-10-26.json).
