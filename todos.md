# TODOs

## P2 — Enable GitHub auto-delete head branches

**What:** Turn on "Automatically delete head branches" in repo Settings → General.

**Why:** Remote branches survive after PR merge (e.g. `expand-light-groups-help`
existed on remote after PR #18 merged). One-click setting eliminates the remote half
of branch clutter automatically.

**How:** github.com/florianhorner/adaptive-lighting/settings → "Pull Requests" section
→ enable "Automatically delete head branches".

**Note:** Doesn't help with local branches — those still need manual `git branch -D`
after verifying the PR merged (`gh pr view <number> --json state`).
