"""Keep the agent skills, plugin manifests and llms.txt generator honest.

The skills under ``plugins/flaui/skills`` are read by AI agents, so they must not drift from the code:

- every fenced Python block must be copied verbatim from a runnable file under ``examples/``;
- every dotted ``flaui.*`` path they mention must import;
- the Claude Code and Codex manifests must agree with each other and with ``pyproject.toml``.
"""

import importlib
import importlib.util
import json
from pathlib import Path
import re
import tomllib
from types import ModuleType
from typing import Dict, List

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "flaui"
SKILLS = sorted(PLUGIN_ROOT.glob("skills/*/SKILL.md"))
EXAMPLES = sorted((REPO_ROOT / "examples").rglob("*.py"))

PYTHON_BLOCK_RE = re.compile(r"^```python\n(.*?)^```", re.MULTILINE | re.DOTALL)
DOTTED_PATH_RE = re.compile(r"`(flaui(?:\.\w+)+)`")


def _frontmatter(text: str) -> Dict[str, str]:
    """Parse the simple ``key: value`` YAML frontmatter of a SKILL.md file.

    :param text: The file content.
    :return: Frontmatter keys mapped to values.
    """
    assert text.startswith("---\n"), "SKILL.md must start with a frontmatter block"
    block = text.split("---\n", 2)[1]
    return dict(line.split(": ", 1) for line in block.strip().splitlines())


def _stripped_lines(text: str) -> List[str]:
    """Return the non-blank lines of ``text`` without indentation.

    :param text: Source text.
    :return: The lines, stripped.
    """
    return [line.strip() for line in text.splitlines() if line.strip()]


def _load_json(path: Path) -> dict:
    """Read a JSON file.

    :param path: File path.
    :return: The parsed object.
    """
    return json.loads(path.read_text(encoding="utf-8"))


def test_skills_exist() -> None:
    """The plugin ships the four documented skills."""
    assert [p.parent.name for p in SKILLS] == [
        "flaui-debug-flaky",
        "flaui-find-and-act",
        "flaui-setup",
        "flaui-write-tests",
    ]


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.parent.name)
def test_skill_frontmatter(skill: Path) -> None:
    """Frontmatter follows the Agent Skills format that Claude Code and Codex both read."""
    meta = _frontmatter(skill.read_text(encoding="utf-8"))
    assert meta["name"] == skill.parent.name
    assert re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["name"]) and len(meta["name"]) <= 64
    assert 0 < len(meta["description"]) <= 1024


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.parent.name)
def test_skill_python_snippets_come_from_examples(skill: Path) -> None:
    """Every Python block in a skill is a contiguous excerpt of a runnable example file."""
    example_lines = {path: _stripped_lines(path.read_text(encoding="utf-8")) for path in EXAMPLES}
    blocks = PYTHON_BLOCK_RE.findall(skill.read_text(encoding="utf-8"))
    assert blocks, "each skill should show at least one runnable snippet"
    for block in blocks:
        wanted = _stripped_lines(block)
        found = any(lines[i : i + len(wanted)] == wanted for lines in example_lines.values() for i in range(len(lines)))
        assert found, f"snippet not found verbatim in examples/:\n{block}"


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.parent.name)
def test_skill_dotted_paths_resolve(skill: Path) -> None:
    """Every ``flaui.*`` dotted path a skill names is a real module or attribute."""
    for dotted in sorted(set(DOTTED_PATH_RE.findall(skill.read_text(encoding="utf-8")))):
        parts = dotted.split(".")
        for split in range(len(parts), 0, -1):
            try:
                obj: object = importlib.import_module(".".join(parts[:split]))
            except ModuleNotFoundError:
                continue
            for attribute in parts[split:]:
                obj = getattr(obj, attribute)
            break
        else:
            pytest.fail(f"{dotted} does not resolve")


def test_manifests_agree() -> None:
    """Claude Code and Codex manifests name the same plugin, path and version as pyproject."""
    version = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    claude_market = _load_json(REPO_ROOT / ".claude-plugin" / "marketplace.json")
    codex_market = _load_json(REPO_ROOT / ".agents" / "plugins" / "marketplace.json")
    claude_plugin = _load_json(PLUGIN_ROOT / ".claude-plugin" / "plugin.json")
    codex_plugin = _load_json(PLUGIN_ROOT / ".codex-plugin" / "plugin.json")

    assert claude_market["name"] == codex_market["name"]
    [claude_entry] = claude_market["plugins"]
    [codex_entry] = codex_market["plugins"]
    assert claude_entry["name"] == codex_entry["name"] == claude_plugin["name"] == codex_plugin["name"]
    assert (REPO_ROOT / claude_entry["source"]).resolve() == PLUGIN_ROOT
    assert (REPO_ROOT / codex_entry["source"]["path"]).resolve() == PLUGIN_ROOT
    assert claude_plugin["version"] == codex_plugin["version"] == version
    assert (PLUGIN_ROOT / codex_plugin["skills"]).is_dir()


def _llms_script() -> ModuleType:
    """Import ``scripts/build_llms_txt.py`` as a module.

    :return: The loaded module.
    """
    spec = importlib.util.spec_from_file_location("build_llms_txt", REPO_ROOT / "scripts" / "build_llms_txt.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "path, expected",
    [
        ("index.md", ""),
        ("basics.md", "basics/"),
        ("api/index.md", "api/"),
        ("api/elements/tab.md", "api/elements/tab/"),
    ],
)
def test_llms_page_url(path: str, expected: str) -> None:
    """Page URLs follow Zensical's directory-style URLs."""
    assert _llms_script().page_url("https://example.test/latest/", path) == "https://example.test/latest/" + expected


def test_llms_expands_snippets() -> None:
    """``--8<--`` includes are replaced by the example section, re-indented, without markers."""
    expanded = _llms_script().expand_snippets('    --8<-- "examples/scripts/quickstart.py:setup"')
    assert expanded.startswith("    from flaui.lib.pythonnet_bridge import setup_pythonnet_bridge")
    assert "--8<--" not in expanded


def test_llms_first_paragraph_skips_markup() -> None:
    """The index description is the first prose paragraph, as plain text."""
    markdown = "# Title\n\n![logo](logo.png)\n\n!!! note\n    hidden\n\nSee [the guide](g.md) for **more**.\n"
    assert _llms_script().first_paragraph(markdown) == "See the guide for more."
