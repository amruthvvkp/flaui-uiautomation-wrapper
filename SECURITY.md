# Security Policy

Thank you for helping keep **FlaUI for Python** (`flaui-uiautomation-wrapper` on PyPI) and its users
safe. This document explains which versions receive security fixes, how to report a vulnerability
privately, and what to expect after you do.

## Supported versions

Security fixes are released for the **1.x** line only.

| Version | Supported | Notes |
|---------|-----------|-------|
| 1.x (including `1.0.0` pre-releases) | ✅ | Fixes ship in the next patch or pre-release. |
| 0.x | ❌ | Legacy experimental wrapper; please [upgrade](https://amruthvvkp.github.io/flaui-uiautomation-wrapper/upgrade-guide/). |

Python **3.11–3.15** on Windows is supported, matching `requires-python` in `pyproject.toml`.

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues, discussions, or pull
requests.**

Report it privately through GitHub's private vulnerability reporting:

1. Go to the repository's **[Security → Advisories](https://github.com/amruthvvkp/flaui-uiautomation-wrapper/security/advisories/new)** page.
2. Click **Report a vulnerability** and fill in the form.

Only the maintainers can see the report. It becomes a private advisory where we can discuss the
issue with you, work on a fix in a private fork, and request a CVE.

To help us triage quickly, please include as much of the following as you can:

- The affected version(s) of `flaui-uiautomation-wrapper`, plus your Python version and Windows build.
- The type of issue (for example, arbitrary code execution, DLL loading from an untrusted path, or
  credential exposure in logs or captures).
- The affected source file(s), with a link to the tag, branch, or commit.
- Step-by-step reproduction instructions, and a minimal proof of concept if you have one.
- The impact: what an attacker could do, and under what preconditions.

## What to expect

FlaUI for Python is maintained by a small volunteer team, so these timelines are targets, not
guarantees:

| Step | Target |
|------|--------|
| Acknowledge your report | within **5 business days** |
| Initial assessment (confirmed / not a vulnerability / need more info) | within **10 business days** |
| Fix or mitigation for confirmed high-severity issues | within **30 days** of confirmation |

We will keep you updated in the advisory thread while we work on it. Once a fix is released, we
publish the advisory and credit you by name or handle, unless you'd rather stay anonymous.

We follow **coordinated disclosure**. Please give us a reasonable chance to release a fix before
you disclose the issue publicly. If we cannot fix it within 90 days, we will agree a disclosure date
with you.

## Scope

**In scope:**

- The Python package in this repository (`flaui/`): the PythonNet bridge, DLL loading, exception
  translation, logging, capture and video helpers, and the element and pattern wrappers.
- The build, packaging, and release pipeline in this repository (GitHub Actions, Azure Pipelines,
  AppVeyor configuration), including anything that could let someone tamper with a published wheel.
- The runnable examples under `examples/`, and the documentation site, where they could lead users
  to unsafe practices.

**Report upstream as well:**

- **FlaUI** (the C# library whose DLLs are bundled in `flaui/bin/`): report to
  [FlaUI/FlaUI](https://github.com/FlaUI/FlaUI/security). Please also tell us, so we can ship
  updated DLLs.
- **Python.NET**: report to [pythonnet/pythonnet](https://github.com/pythonnet/pythonnet/security).
- Other third-party dependencies: report to their maintainers. Dependabot alerts us to published
  advisories for our dependencies.

**Out of scope:**

- The intended behaviour of UI automation. This library drives other applications' UIs by design,
  through Microsoft UI Automation, with the permissions of the user running it. Being able to click,
  type into, read, or screenshot windows that the current user can already access is not a
  vulnerability.
- The bundled test applications under `test_applications/`. They exist only to exercise the test
  suite.
- Findings that need an already-compromised machine or administrator access, for example replacing
  files inside the installed package.
- Reports from automated scanners without a demonstrated, exploitable impact.

## Security practices in this repository

- **CodeQL** code scanning runs for Python and GitHub Actions.
- **Dependabot** security updates are enabled for our dependencies.
- **Secret scanning** with push protection is enabled.
- The bundled FlaUI DLLs in `flaui/bin/` are official FlaUI build outputs. They are never modified,
  and their versions are recorded in `flaui/bin/Version.md`.

## Safe usage notes

- UI automation runs with the privileges of the current user. Do not run untrusted automation
  scripts, and be careful when automating elevated (administrator) applications.
- Screenshots, video recordings (`flaui.core.capturing`), and the C# log bridge (`FLAUI_LOG_CSHARP`)
  can capture whatever is on screen or in the UI tree, including passwords and personal data. Treat
  these artifacts as sensitive. This matters most in CI, where they are often uploaded.
- Install the package from PyPI or from a source you trust. The wheel loads .NET assemblies from its
  own `flaui/bin/` directory, unless the `FLAUI_BIN_HOME` environment variable points somewhere else.
  Only set it to test a FlaUI build you trust, and treat anyone who can change your environment
  variables as able to change which DLLs are loaded. When it is set, the bridge logs a warning on the
  `flaui.lib.pythonnet_bridge` logger.
