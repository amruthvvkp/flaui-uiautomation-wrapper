"""Audit FlaUI C# API parity against the Python wrapper.

Reflects over the bundled FlaUI DLLs (``FlaUI.Core``, ``FlaUI.UIA2``, ``FlaUI.UIA3``) to
enumerate every public type and member, then introspects the ``flaui`` Python package to
determine what is wrapped. Emits a Markdown parity map to ``docs/parity.md``.

The audit is version-exact to the DLLs we ship (currently FlaUI 5.0). Re-run whenever the
bundled binaries change::

    uv run python scripts/parity_audit.py

C#-to-Python member matching uses the project's naming convention (PascalCase ->
snake_case). A type counts as *covered* when a Python class of the same name exists,
*partial* when some of its public members are missing, and *missing* when no Python class
maps to it. The result is a planning aid, not a strict gate -- intentional omissions (e.g.
``CustomNavigation``, GH-121) are expected and annotated in the generated doc.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
import re
from dataclasses import dataclass, field
from pathlib import Path
import sys
from typing import Dict, List, Optional, Set

# isort: off  -- the bridge MUST load the C# DLLs before any C# type is touched.
from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge

setup_pythonnet_bridge()

import flaui  # noqa: E402  Python package we audit against
from System import AppDomain  # noqa: E402  pyright: ignore[reportMissingImports]
from System.Reflection import BindingFlags  # noqa: E402  pyright: ignore[reportMissingImports]

# isort: on

# Public, instance-level, declared-on-this-type members only. Inherited members (e.g. the
# AutomationElement base surface) are reported once on the base type, not on every subclass.
_DECLARED_PUBLIC = (
    BindingFlags.Public | BindingFlags.Instance | BindingFlags.DeclaredOnly
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_MD = ROOT / "docs" / "parity.md"

TARGET_ASSEMBLIES = ("FlaUI.Core", "FlaUI.UIA2", "FlaUI.UIA3")

# C# members that have no meaningful Python counterpart (object plumbing / operators).
IGNORED_MEMBERS = {
    "ToString",
    "Equals",
    "GetHashCode",
    "GetType",
    "Finalize",
    "MemberwiseClone",
}

_CAMEL_BOUNDARY_1 = re.compile(r"(.)([A-Z][a-z]+)")
_CAMEL_BOUNDARY_2 = re.compile(r"([a-z0-9])([A-Z])")


def to_snake_case(name: str) -> str:
    """Convert a C# PascalCase identifier to the wrapper's snake_case convention.

    :param name: C# member or type name.
    :return: snake_case form (e.g. ``BoundingRectangle`` -> ``bounding_rectangle``).
    """
    interim = _CAMEL_BOUNDARY_1.sub(r"\1_\2", name)
    return _CAMEL_BOUNDARY_2.sub(r"\1_\2", interim).lower()


@dataclass
class CsType:
    """A public C# type and the public members declared on it."""

    assembly: str
    namespace: str
    name: str
    kind: str  # "class" | "interface" | "enum" | "struct"
    members: Set[str] = field(default_factory=set)

    @property
    def folder(self) -> str:
        """Return the leaf namespace segment, mirroring the C# source folder layout."""
        return self.namespace.split(".")[-1] if self.namespace else "(root)"


@dataclass
class PyClass:
    """A Python class discovered in the ``flaui`` package."""

    name: str
    module: str
    members: Set[str] = field(default_factory=set)


def collect_csharp_types() -> List[CsType]:
    """Reflect over the loaded FlaUI assemblies and collect public types/members.

    :return: List of :class:`CsType`, one per public exported type.
    """
    types: List[CsType] = []
    assemblies = {
        asm.GetName().Name: asm
        for asm in AppDomain.CurrentDomain.GetAssemblies()
        if asm.GetName().Name in TARGET_ASSEMBLIES
    }
    for asm_name in TARGET_ASSEMBLIES:
        asm = assemblies.get(asm_name)
        if asm is None:
            print(f"WARNING: assembly {asm_name} not loaded", file=sys.stderr)
            continue
        for t in asm.GetExportedTypes():
            if t.IsNested or (t.Name and t.Name.startswith("<")):
                continue
            kind = (
                "enum"
                if t.IsEnum
                else "interface"
                if t.IsInterface
                else "struct"
                if t.IsValueType
                else "class"
            )
            members: Set[str] = set()
            if not t.IsEnum:
                for m in t.GetMethods(_DECLARED_PUBLIC):
                    if m.IsSpecialName:  # property/event accessors, operators
                        continue
                    if m.Name in IGNORED_MEMBERS:
                        continue
                    members.add(m.Name)
                for p in t.GetProperties(_DECLARED_PUBLIC):
                    members.add(p.Name)
            types.append(
                CsType(
                    assembly=asm_name,
                    namespace=t.Namespace or "",
                    name=t.Name,
                    kind=kind,
                    members=members,
                )
            )
    return types


def collect_python_classes() -> Dict[str, PyClass]:
    """Walk the ``flaui`` package and index every class by name.

    :return: Mapping of class name -> :class:`PyClass`. Later definitions win on name
        collision, which is acceptable for a coverage signal.
    """
    classes: Dict[str, PyClass] = {}
    for mod_info in pkgutil.walk_packages(flaui.__path__, prefix="flaui."):
        try:
            module = importlib.import_module(mod_info.name)
        except Exception as err:  # pragma: no cover - defensive against optional deps
            print(f"WARNING: could not import {mod_info.name}: {err}", file=sys.stderr)
            continue
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if not obj.__module__.startswith("flaui"):
                continue
            members = {
                name
                for name, _ in inspect.getmembers(obj)
                if not name.startswith("_")
            }
            classes[obj.__name__] = PyClass(name=obj.__name__, module=obj.__module__, members=members)
    return classes


def classify(cs: CsType, py_classes: Dict[str, PyClass]) -> tuple[str, Optional[PyClass], List[str]]:
    """Classify a C# type's coverage against the Python wrappers.

    :param cs: The C# type under audit.
    :param py_classes: Index of Python classes by name.
    :return: ``(status, matched_py_class, missing_members)`` where status is one of
        ``"covered"``, ``"partial"``, or ``"missing"``.
    """
    py = py_classes.get(cs.name)
    if py is None:
        return "missing", None, sorted(cs.members)
    if cs.kind == "enum" or not cs.members:
        return "covered", py, []
    missing = sorted(m for m in cs.members if to_snake_case(m) not in py.members and m not in py.members)
    status = "covered" if not missing else "partial"
    return status, py, missing


def build_markdown(cs_types: List[CsType], py_classes: Dict[str, PyClass]) -> str:
    """Render the parity map as Markdown grouped by assembly and namespace folder.

    :param cs_types: All public C# types collected via reflection.
    :param py_classes: Index of Python classes by name.
    :return: Markdown document text.
    """
    rows = [(cs, *classify(cs, py_classes)) for cs in cs_types]
    totals = {"covered": 0, "partial": 0, "missing": 0}
    for _, status, _, _ in rows:
        totals[status] += 1
    total = len(rows) or 1

    out: List[str] = [
        "<!-- Auto-generated by scripts/parity_audit.py. Do not edit manually. -->",
        "# FlaUI C# Parity Map",
        "",
        "Generated by reflecting over the bundled FlaUI DLLs and diffing against the `flaui`",
        "Python package. Re-run with `uv run python scripts/parity_audit.py`.",
        "",
        "**Status key:** ✅ covered · 🟡 partial (some public members unwrapped) · ❌ missing",
        "",
        "## Scope & how to read this",
        "",
        "This map covers **every public type** in the three assemblies, but the wrapper",
        "deliberately mirrors only the **user-facing FlaUI.Core surface** — automation elements,",
        "patterns, conditions, input, tools, capturing, overlay, identifiers, and event handlers.",
        "A large share of the ❌ *missing* count is **out of scope by design**, not a gap:",
        "",
        "- **`FlaUI.UIA2` / `FlaUI.UIA3`** types are framework *adapters*. Python selects a backend",
        "  via `UIAutomationTypes` and reaches C# through the PythonNet bridge; the adapter classes",
        "  (converters, COM-interop shims, native-method wrappers) are not re-wrapped 1:1.",
        "- **Core infrastructure** — internal converters, `*Extensions` helper classes, COM interop,",
        "  and abstract base plumbing — is consumed indirectly and intentionally unwrapped.",
        "- Known intentional omission: `CustomNavigation` (GH-121) exists only in raw COM interop.",
        "",
        "Treat 🟡 *partial* / ❌ *missing* rows in the **FlaUI.Core element, pattern, condition,",
        "input, tool, capturing, overlay, and identifier folders** as the actionable backlog; rows",
        "elsewhere are usually intentional. 🟡 can also be an API-shape difference (e.g. C# exposes a",
        "`FooPattern` property where Python exposes a `foo()` method), not a true gap.",
        "",
        "## Summary",
        "",
        "| Status | Types | % |",
        "| --- | ---: | ---: |",
        f"| ✅ Covered | {totals['covered']} | {totals['covered'] * 100 // total}% |",
        f"| 🟡 Partial | {totals['partial']} | {totals['partial'] * 100 // total}% |",
        f"| ❌ Missing | {totals['missing']} | {totals['missing'] * 100 // total}% |",
        f"| **Total** | **{total}** | 100% |",
        "",
    ]

    icon = {"covered": "✅", "partial": "🟡", "missing": "❌"}
    by_asm: Dict[str, Dict[str, list]] = {}
    for cs, status, py, missing in rows:
        by_asm.setdefault(cs.assembly, {}).setdefault(cs.folder, []).append((cs, status, py, missing))

    for asm in TARGET_ASSEMBLIES:
        folders = by_asm.get(asm)
        if not folders:
            continue
        out.append(f"## {asm}")
        out.append("")
        for folder in sorted(folders):
            out.append(f"### {folder}")
            out.append("")
            out.append("| Type | Kind | Status | Notes |")
            out.append("| --- | --- | --- | --- |")
            for cs, status, _py, missing in sorted(folders[folder], key=lambda r: r[0].name):
                if status == "missing":
                    note = "no Python class"
                elif status == "partial":
                    shown = ", ".join(f"`{m}`" for m in missing[:6])
                    extra = f" (+{len(missing) - 6} more)" if len(missing) > 6 else ""
                    note = f"unwrapped: {shown}{extra}"
                else:
                    note = ""
                out.append(f"| {cs.name} | {cs.kind} | {icon[status]} | {note} |")
            out.append("")
    return "\n".join(out)


def main() -> int:
    """Generate the parity map and write it to ``docs/parity.md``.

    :return: Process exit code (0 on success).
    """
    cs_types = collect_csharp_types()
    if not cs_types:
        print("No C# types collected -- is the PythonNet bridge working?", file=sys.stderr)
        return 1
    py_classes = collect_python_classes()

    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_MD.write_text(build_markdown(cs_types, py_classes), encoding="utf-8")

    covered = sum(1 for cs in cs_types if classify(cs, py_classes)[0] == "covered")
    print(f"Audited {len(cs_types)} public C# types across {', '.join(TARGET_ASSEMBLIES)}.")
    print(f"Python classes indexed: {len(py_classes)}")
    print(f"Covered: {covered}/{len(cs_types)}")
    print(f"Written: {OUTPUT_MD.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
