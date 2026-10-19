---
name: "speckit-taskstoissues"
description: "Convert app2 Spec Kit tasks into GitHub issues."
compatibility: "Requires Spec Kit installed in app2/.specify/."
---

Read and execute the complete workflow in `app2/.github/skills/speckit-taskstoissues/SKILL.md`.
Treat `app2` as the Spec Kit project root for every relative path and command in that
workflow. Keep generated or modified Spec Kit artifacts inside `app2`; run project
scripts with `app2` as the working directory. The repository root remains the VS Code
workspace so its documentation stays available as context.
