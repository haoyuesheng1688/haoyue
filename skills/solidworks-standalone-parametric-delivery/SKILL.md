---
name: solidworks-standalone-parametric-delivery
description: Build an isolated SolidWorks part or assembly with a parameter panel and geometry-backed regression evidence. Use when the user wants a component separated from a source model and driven by named dimensions.
allowed-tools:
  - Read
  - Grep
  - PowerShell
---

# SolidWorks standalone parametric delivery

## When to use

Use for a user-requested standalone SolidWorks part/assembly with a double-clickable parameter panel, native and STEP deliverables, and proof that the requested parameters changed real geometry. Do not use it to alter the source assembly unless that is explicitly requested, or to represent manufacturing, thermal, material, or filter-performance approval.

## Inputs to establish

1. Bind the exact running SolidWorks document and identify which source files must remain unchanged.
2. Confirm the standalone output directory and the complete list of primary driving parameters.
3. Define the geometric acceptance checks for each parameter, including any interface, hole-pattern, clearance, or extraction-path requirements.

## Procedure

1. Create an independent output model/assembly and preserve the source files. Include the native file, STEP, parameter-update script, double-clickable panel launcher, usage notes, current-parameter record, and validation summary.
2. Make the requested dimensions named driving variables/equations; map every panel control to a real model dimension. If an initially simplified envelope is requested (for example, a rectangular filter core), make that envelope a clearly stated parametric placeholder.
3. Exercise an A→B→A change through the panel, rebuild, save, reopen, and read actual geometry. Validate each requested control rather than only equation strings or COM success. Do not substitute direct equation editing plus rebuild for a panel-driven test: it may not update every dependency.
4. For assemblies, additionally check mating/paired hole patterns, positive-volume interference, and any requested removal/extraction sweep. Re-import or read STEP and compare component/body count, volume, and overall bounds with the native artifact.
5. State scope boundaries: a volume containing placeholder or insulation bodies is not a metal mass; geometry checks are not material, thermal, filter-performance, sheet-metal-flat-pattern, manufacturing, or fastening approval.

## Efficiency plan

1. Start with `MEMORY.md` searches for `LADDER_HEIGHT`, `RUNG_COUNT`, `G25_Standalone_HEPA`, or `dangling relation` when working in `D:\codex\solidworks`.
2. Capture the intended active document identity before any mutation and use one parameter matrix for all regression cases.
3. Stop and repair before delivery when feature errors, dangling sketch relations, failed reopen, missing STEP read-back, or a control with no measured geometry change appears.

## Pitfalls and fixes

- Symptom: `草图5`/a feature has dangling relations after an array or auxiliary-sketch edit.
  - Fix: inspect `Sketch.RelationManager.GetRelations(1)` (dangling filter), call `DeleteRelation` for each offending relation, then `ForceRebuild3(False)` and repeat geometry checks.
- Symptom: a cage/ring appears centered but an automated check reports an offset.
  - Fix: compare the circle/arc center with the bounding-box center of non-construction geometry; do not use a derived point algorithm without validating it on changed width/diameter cases.
- Symptom: a green rebuild or unchanged native volume is treated as acceptance.
  - Fix: perform real A→B→A geometry read-back, save/reopen, and STEP read-back; for assemblies include interference and extraction evidence when requested.
- Symptom: an independent copy has empty or missing flanges/supports.
  - Fix: immediately compare critical entity count, bounding box, volume, and interface dimensions before parameterization; repair isolation first.
- Symptom: interference output lists contact candidates.
  - Fix: do not call them positive-volume interference or weld/structural validation unless the check establishes overlapping volume.
- Symptom: restoring a parameter default crashes SolidWorks with `0xc0000374` after feature-copy reuse or batch cuts.
  - Fix: avoid those operations in the acceptance path, reconstruct the affected geometry independently, retain the process-exit evidence, and state that the underlying crash is unresolved.

## Verification checklist

1. The source model/hash is unchanged when isolation was requested.
2. Every promised parameter has panel, equation, and measured-geometry coverage.
3. The final default set is restored, saved, reopened, and documented.
4. Native and STEP artifacts exist; STEP has been read back if it is part of delivery.
5. Feature errors and dangling relations are absent after rebuild.
6. Any assembly-specific hole alignment, interference, and removal-path checks requested by the user are evidenced.
