# Running UI Tests on CI/CD

Desktop UI automation is different from web or unit testing: it drives **real windows on a real
Windows desktop**. The single most common reason FlaUI (and pywinauto, WinAppDriver, Playwright‑for‑
Windows, etc.) tests "work on my machine but fail on CI" is that the CI runner has **no interactive
desktop session** for the application to render into. This page explains why, and how to get a green
UI pipeline.

!!! tip "TL;DR"
    UI automation needs an **interactive, unlocked, logged‑in desktop session** at a real screen
    resolution. Headless containers and the default Microsoft‑hosted cloud runners usually don't
    provide one. Use **AppVeyor** (hosted, interactive desktop out of the box) or a **self‑hosted
    runner configured with autologon + an interactive session**. This project uses a hybrid
    **Azure Pipelines (fast gates) + AppVeyor (UI gate)** setup — see [below](#how-this-project-does-it).

---

## Why the default cloud runners struggle

Windows UI Automation (the API underneath FlaUI) reads the on‑screen automation tree and computes
clickable points from actual window geometry. That requires a window station / desktop that is
actually composing UI. Hosted CI runners frequently fall short in one of these ways:

- **No interactive session (Session 0 / service context).** Build agents installed as a Windows
  *service* run in the non‑interactive "Session 0". Apps launched there have no visible desktop, so
  controls may never render, `GetClickablePoint` fails, and focus/foreground operations are no‑ops.
- **Locked or disconnected session.** When a desktop is locked (or an RDP session is disconnected),
  Windows stops composing the UI. Clicks and coordinate lookups then fail intermittently.
- **No/!unknown screen resolution or DPI.** A headless session may report a tiny or zero‑size
  virtual screen, pushing controls "off‑screen" so they can't be clicked.
- **Containers.** Windows server containers have no desktop/GUI stack at all; desktop UIA does not
  work inside them.

| Runner | Interactive desktop by default? | Good for desktop UI tests? |
|--------|--------------------------------|----------------------------|
| **AppVeyor** (Windows images) | ✅ Yes — builds run in a logged‑in interactive session | ✅ Recommended hosted option |
| **GitHub Actions** `windows-latest` (Microsoft‑hosted) | ⚠️ Not reliably — no guaranteed interactive desktop | ⚠️ Flaky; prefer a self‑hosted interactive runner |
| **Azure Pipelines** Microsoft‑hosted `windows-2022` | ⚠️ Not reliably | ⚠️ Use for unit/lint gates; run UI on AppVeyor or self‑hosted |
| **Self‑hosted runner as a *service*** | ❌ No (Session 0) | ❌ Will fail |
| **Self‑hosted runner as a *process* in a logged‑in session** | ✅ Yes (when configured) | ✅ Works |
| **Windows server container** | ❌ No desktop stack | ❌ Not supported |

!!! note "Why AppVeyor 'just works'"
    AppVeyor's Windows build images execute the build inside an **interactive, auto‑logged‑in
    desktop session**, so real windows render and UIA can see and click them — no extra setup. That
    is exactly why this repository runs its full desktop UI suite there.

---

## What actually works

### Option 1 — AppVeyor (recommended hosted)

No special configuration is needed for the desktop itself; a minimal `appveyor.yml` that installs
your deps and runs pytest is enough:

```yaml
image: Visual Studio 2022
build: off
install:
  - cmd: curl -LsSf https://astral.sh/uv/install.ps1 | powershell -c -
  - cmd: uv sync --all-extras
test_script:
  - cmd: uv run pytest tests/ -v
```

Because the session is already interactive, FlaUI can launch your app, read the tree, and click.

### Option 2 — Self‑hosted runner with an interactive session

If you must use GitHub Actions or Azure DevOps, register a **self‑hosted** runner on a Windows VM
you control and make sure the agent runs **in a logged‑in desktop session**, not as a service.

Checklist for the VM:

1. **Enable autologon** so the box boots straight into a desktop session (configure a dedicated CI
   user via Sysinternals `Autologon`, or the `DefaultUserName`/`DefaultPassword`/`AutoAdminLogon`
   registry values under `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon`).
2. **Run the runner/agent as a foreground process in that session** (e.g. `run.cmd` in a Startup
   shortcut), *not* as a Windows service. Service installs land in Session 0 and break UI tests.
3. **Disable the lock screen and screensaver**, and set the power plan to never sleep/turn off the
   display. A locked desktop stops composing UI.
4. **Set a real screen resolution / DPI** (e.g. 1920×1080 at 100%). Headless GPUs can default to a
   resolution that pushes controls off‑screen.
5. **Avoid plain RDP for maintenance** — disconnecting an RDP session locks the console and UI work
   stops. If you must use RDP, keep the session connected, or use a tool that keeps the physical
   console active (e.g. `tscon` to move the session back to the console on disconnect).
6. **Don't run UI tests in a Windows container.** Use a full VM (or a nested VM with a GUI).

---

## Common failure symptoms → fixes

| Symptom on CI (passes locally) | Likely cause | Fix |
|--------------------------------|--------------|-----|
| `NoClickablePointException` / `GetClickablePoint` fails | Session locked or off‑screen window | Unlock session, set real resolution, bring window to foreground |
| `ElementNotFound` for controls that exist | App rendered in a non‑interactive session, or tree not ready | Use an interactive session; add a short retry/wait around first lookups |
| Tests hang then time out | App never showed a window (Session 0) | Run the agent as a process in a logged‑in session |
| Works on first run, flaky in bulk | Session idle/backgrounded, transient UIA hiccups | Keep the session active; retry first finds; serialize UI tests |
| Everything fails in a container | No desktop stack | Switch to a full Windows VM |

!!! tip "Make finds resilient"
    Even on a healthy interactive runner, the automation tree can momentarily be incomplete right
    after an app launches or a tab switches. Wrap the first lookups in a small retry (this library
    ships [`flaui.core.tools`](api/tools.md) retry helpers and [`Wait`](api/wait.md)), and prefer
    stable conditions (`ControlType` + `Name`) over volatile AutomationIDs.

---

## How this project does it

This repository uses a **hybrid CI** that splits the work by what each runner is good at:

- **Azure Pipelines** (Microsoft‑hosted `windows-2022`) owns the fast gates — Ruff + Interrogate
  linting, the strict docs build, a small unit/identifier smoke suite, and package/deploy stages.
- **AppVeyor** (`Visual Studio 2022`) is the **interactive desktop gate** that runs the full
  UIA2/UIA3 × WinForms/WPF UI suite, where a real logged‑in session is available.

This is a good template to copy: run lint/unit/build anywhere, and pin the **desktop UI suite** to a
runner that guarantees an interactive session. See the contributor
[Development Workflow](contributing/development.md) for the full pipeline details, and
[Troubleshooting](troubleshooting.md) for non‑CI setup issues.
