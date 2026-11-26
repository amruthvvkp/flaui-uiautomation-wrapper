"""Generate ``docs/llms.txt`` and ``docs/llms-full.txt`` for AI agents and LLM tools.

Both files follow the `llms.txt <https://llmstxt.org/>`_ convention and are copied by Zensical to
the root of the built site, next to ``index.html``:

- ``llms.txt`` is a short index: an H1, a blockquote summary, a few key facts, then one section per
  top-level navigation group, with a link and a one-line description for every page.
- ``llms-full.txt`` is the whole documentation flattened into one Markdown file. ``--8<--`` snippet
  includes are expanded from ``examples/``, and ``::: module.Object`` mkdocstrings directives are
  rendered from the docstrings with griffe, so the file carries the API reference too.

The page list and order come from ``nav`` in ``zensical.toml``. Run this script after
``extract_versions.py`` and ``build_changelog.py`` (so the generated includes and changelog exist)
and before ``zensical build``. Both outputs are gitignored.

Links are absolute. They point at the ``latest`` docs by default. Pass ``--base-url`` (or set
``FLAUI_DOCS_BASE_URL``) to point them at another published version, for example ``stable``.
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys
import textwrap
import tomllib
from typing import Any, Dict, Iterator, List, NamedTuple, Optional

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CONFIG = ROOT / "zensical.toml"
OUTPUT_INDEX = DOCS / "llms.txt"
OUTPUT_FULL = DOCS / "llms-full.txt"
REPO_URL = "https://github.com/amruthvvkp/flaui-uiautomation-wrapper"

# Navigation groups listed under the spec's "Optional" section: useful, but skippable when an agent
# is short on context.
OPTIONAL_GROUPS = ("Project", "Contributing")

SNIPPET_RE = re.compile(r'^(?P<indent>\s*)--8<-- "(?P<target>[^"]+)"\s*$')
SECTION_MARK_RE = re.compile(r"--8<-- \[(?P<kind>start|end):(?P<name>[\w-]+)\]")
DIRECTIVE_RE = re.compile(r"^:::\s+(?P<path>[\w.]+)\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


class Page(NamedTuple):
    """One documentation page, in navigation order."""

    group: str
    title: str
    path: str


def iter_nav(nav: List[Any], group: Optional[str] = None) -> Iterator[Page]:
    """Flatten the ``nav`` tree from ``zensical.toml`` into pages.

    :param nav: A list of single-key ``{title: path_or_children}`` tables.
    :param group: The top-level group the entries belong to; ``None`` at the top level.
    :return: The pages in navigation order.
    """
    for entry in nav:
        for title, value in entry.items():
            if isinstance(value, list):
                yield from iter_nav(value, group or title)
            else:
                yield Page(group or title, title, value)


def page_url(base_url: str, path: str) -> str:
    """Return the published URL of a page, using directory-style URLs.

    :param base_url: Site root URL, ending with ``/``.
    :param path: Page path relative to ``docs/`` (for example ``api/index.md``).
    :return: The absolute page URL.
    """
    stem = path[: -len(".md")] if path.endswith(".md") else path
    if stem == "index" or stem.endswith("/index"):
        stem = stem[: -len("index")]
    else:
        stem += "/"
    return base_url + stem.lstrip("/")


def _plain(text: str) -> str:
    """Strip common Markdown markup so a paragraph reads as plain text.

    :param text: A Markdown fragment.
    :return: The fragment without links, emphasis or inline-code markers.
    """
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)  # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)  # links
    text = re.sub(r"[*_]{1,2}([^*_]+)[*_]{1,2}", r"\1", text)  # emphasis
    text = text.replace("`", "")
    return " ".join(text.split())


def first_paragraph(markdown: str) -> str:
    """Return the first prose paragraph of a page, as plain text.

    Headings, admonitions, tabs, tables, lists, HTML, includes and code blocks are skipped.

    :param markdown: The page source.
    :return: The paragraph, or an empty string when the page has none.
    """
    lines: List[str] = []
    in_fence = False
    for line in markdown.splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped:
            if lines:
                break
            continue
        skip = (
            line[:1].isspace()
            or stripped.startswith(("#", "!!!", "???", "===", "|", "-", "*", "<", ">", ":::", "--8<--", "[![", "!["))
            or re.match(r"\d+\.", stripped)
        )
        if skip:
            if lines:
                break
            continue
        lines.append(stripped)
    return _plain(" ".join(lines))


def one_line(text: str, limit: int = 160) -> str:
    """Shorten text to its first sentence, capped at ``limit`` characters.

    :param text: Plain text.
    :param limit: Maximum length of the result.
    :return: A single line suitable for an index entry.
    """
    match = re.match(r"(.+?[.!?])(\s|$)", text)
    sentence = match.group(1) if match else text
    if len(sentence) > limit:
        sentence = sentence[: limit - 3].rsplit(" ", 1)[0] + "..."
    return sentence


# ---------------------------------------------------------------------------------------------
# Snippet includes
# ---------------------------------------------------------------------------------------------


def read_snippet(target: str) -> str:
    """Return the text a ``--8<-- "file[:section]"`` include stands for.

    :param target: The include target, relative to the repository root.
    :return: The file, or the named section of it, dedented, with section markers removed.
    :raises FileNotFoundError: If the file does not exist.
    :raises ValueError: If the named section is missing.
    """
    file_part, _, section = target.partition(":")
    lines = (ROOT / file_part).read_text(encoding="utf-8").splitlines()
    if section:
        start = end = None
        for index, line in enumerate(lines):
            mark = SECTION_MARK_RE.search(line)
            if mark and mark.group("name") == section:
                if mark.group("kind") == "start":
                    start = index + 1
                else:
                    end = index
        if start is None or end is None:
            raise ValueError(f"section {section!r} not found in {file_part}")
        lines = lines[start:end]
    kept = [line for line in lines if not SECTION_MARK_RE.search(line)]
    return textwrap.dedent("\n".join(kept)).strip("\n")


def expand_snippets(markdown: str) -> str:
    """Replace every ``--8<--`` include line with the content it includes.

    :param markdown: The page source.
    :return: The page with includes expanded, keeping each include's indentation.
    """
    out: List[str] = []
    for line in markdown.splitlines():
        match = SNIPPET_RE.match(line)
        if match:
            indent = match.group("indent")
            body = read_snippet(match.group("target"))
            out.extend((indent + part) if part else "" for part in body.splitlines())
        else:
            out.append(line)
    return "\n".join(out)


# ---------------------------------------------------------------------------------------------
# API reference (mkdocstrings ``:::`` directives)
# ---------------------------------------------------------------------------------------------


class ApiRenderer:
    """Render mkdocstrings ``:::`` directives as Markdown from docstrings, using griffe."""

    def __init__(self) -> None:
        """Load the ``flaui`` package statically (nothing is imported, so no .NET is needed)."""
        import griffe  # pylint: disable=import-outside-toplevel  # only the docs environment has it

        self._package: Any = griffe.load("flaui", search_paths=[str(ROOT)], allow_inspection=False)

    def lookup(self, path: str) -> Any:
        """Return the griffe object for a dotted path such as ``flaui.core.tools.Retry``.

        :param path: Dotted path starting with ``flaui``.
        :return: The griffe object.
        :raises KeyError: If the path does not exist.
        """
        parts = path.split(".")
        if parts[0] != "flaui":
            raise KeyError(path)
        return self._package[".".join(parts[1:])] if len(parts) > 1 else self._package

    def summary(self, path: str) -> str:
        """Return the first line of the docstring of the object at ``path``.

        :param path: Dotted path starting with ``flaui``.
        :return: The summary line, or an empty string.
        """
        try:
            docstring = self.lookup(path).docstring
        except KeyError:
            return ""
        return docstring.value.strip().splitlines()[0].strip() if docstring else ""

    @staticmethod
    def _signature(function: Any) -> str:
        """Format a function signature as Python source.

        :param function: A griffe ``Function``.
        :return: For example ``click(self, move_mouse: bool = False) -> None``.
        """
        params = []
        for param in function.parameters:
            prefix = {"var_positional": "*", "var_keyword": "**"}.get(str(param.kind.name), "")
            text = prefix + param.name
            if param.annotation is not None:
                text += f": {param.annotation}"
            if param.default is not None:
                text += f" = {param.default}" if param.annotation is not None else f"={param.default}"
            params.append(text)
        returns = f" -> {function.returns}" if function.returns is not None else ""
        return f"{function.name}({', '.join(params)}){returns}"

    @staticmethod
    def _docstring(obj: Any) -> str:
        """Return an object's docstring, dedented.

        :param obj: A griffe object.
        :return: The docstring, or an empty string.
        """
        return textwrap.dedent(obj.docstring.value).strip() if obj.docstring else ""

    def _members(self, obj: Any) -> Iterator[Any]:
        """Yield the public members declared on ``obj`` itself, in source order.

        :param obj: A griffe module or class.
        :return: Members that are not aliases (re-exports) and not private.
        """
        members = [m for m in obj.members.values() if not m.is_alias and not m.name.startswith("_")]
        yield from sorted(members, key=lambda m: m.lineno or 0)

    def render(self, path: str, level: int = 2) -> str:
        """Render the object at ``path`` (and its public members) as Markdown.

        :param path: Dotted path starting with ``flaui``.
        :param level: Heading level for the object itself.
        :return: The Markdown; a short note when the object cannot be found.
        """
        try:
            obj = self.lookup(path)
        except KeyError:
            return f"*(API reference for `{path}` is not available.)*"
        return self._render(obj, level)

    def _render(self, obj: Any, level: int) -> str:
        """Render one griffe object recursively.

        :param obj: A griffe module, class, function or attribute.
        :param level: Heading level for this object (capped at 6).
        :return: The Markdown.
        """
        hashes = "#" * min(level, 6)
        kind = obj.kind.value
        parts: List[str] = []
        if kind == "function":
            label = "property" if "property" in obj.labels else "method"
            parts.append(f"{hashes} `{obj.name}` ({label})")
            parts.append(f"```python\n{self._signature(obj)}\n```")
        elif kind == "attribute":
            annotation = f": {obj.annotation}" if obj.annotation is not None else ""
            parts.append(f"{hashes} `{obj.name}{annotation}` (attribute)")
        else:
            bases = f"({', '.join(str(b) for b in obj.bases)})" if kind == "class" and obj.bases else ""
            parts.append(f"{hashes} `{obj.path}{bases}` ({kind})")
        doc = self._docstring(obj)
        if doc:
            parts.append(doc)
        if kind in ("module", "class"):
            for member in self._members(obj):
                if kind == "module" and member.kind.value == "attribute" and not member.docstring:
                    continue  # skip undocumented module constants and loggers
                parts.append(self._render(member, level + 1))
        return "\n\n".join(parts)


def render_page(markdown: str, api: Optional[ApiRenderer]) -> str:
    """Flatten one page: expand includes and replace ``:::`` directives with rendered API docs.

    :param markdown: The page source.
    :param api: Renderer for ``:::`` directives; when ``None`` they are left as plain references.
    :return: Self-contained Markdown.
    """
    out: List[str] = []
    in_fence = False
    for line in expand_snippets(markdown).splitlines():
        if FENCE_RE.match(line):
            in_fence = not in_fence
        match = None if in_fence else DIRECTIVE_RE.match(line)
        if match and api is not None:
            out.append(api.render(match.group("path")))
        elif match:
            out.append(f"API reference: `{match.group('path')}`")
        else:
            out.append(line)
    return "\n".join(out).strip() + "\n"


# ---------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------


def describe(markdown: str, api: Optional[ApiRenderer]) -> str:
    """Return the one-line description of a page for ``llms.txt``.

    :param markdown: The page source.
    :param api: Used for API pages that have no prose of their own.
    :return: A description; may be empty.
    """
    text = first_paragraph(markdown)
    if not text and api is not None:
        directive = next((m for m in map(DIRECTIVE_RE.match, markdown.splitlines()) if m), None)
        if directive:
            text = _plain(api.summary(directive.group("path")))
    return one_line(text) if text else ""


def load_api() -> Optional[ApiRenderer]:
    """Create the API renderer, or return ``None`` (with a warning) when griffe is unavailable.

    :return: The renderer, or ``None``; the build never fails because of it.
    """
    try:
        return ApiRenderer()
    except Exception as error:  # pylint: disable=broad-exception-caught  # build-safe: degrade, don't fail
        print(f"WARNING: API reference skipped ({type(error).__name__}: {error})", file=sys.stderr)
        return None


def intro_lines(project: Dict[str, Any], base_url: str) -> List[str]:
    """Return the shared header of both files: the H1, the summary blockquote and key facts.

    :param project: The ``[project]`` table of ``zensical.toml``.
    :param base_url: Site root URL the links point at, ending with ``/``.
    :return: The header lines; the first three are the H1 and the blockquote.
    """
    return [
        f"# {project['site_name']}",
        "",
        f"> {project['site_description']}. A PythonNet port of the C# FlaUI library for Windows UI Automation "
        "(UIA2 and UIA3), typed with pydantic, for test automation and AI computer-use agents.",
        "",
        "Key facts:",
        "",
        "- Install with `pip install flaui-uiautomation-wrapper`. Windows only, 64-bit CPython "
        "3.11-3.15, .NET Framework 4.8.",
        "- Call `flaui.lib.pythonnet_bridge.setup_pythonnet_bridge()` before importing any other "
        "`flaui` module or C# type.",
        "- The API mirrors FlaUI C# in snake_case: `FindFirstDescendant` is `find_first_descendant`.",
        "- FlaUI timeouts are in milliseconds; `post_wait` floats are seconds.",
        f"- Agent skills and a Claude Code / Codex plugin live in the repository: {REPO_URL} "
        f"(see {page_url(base_url, 'ai-agents.md')}).",
        f"- The full documentation in one file: {base_url}llms-full.txt",
        "",
    ]


def build(base_url: str) -> Dict[Path, str]:
    """Build the contents of both output files.

    :param base_url: Site root URL the links point at, ending with ``/``.
    :return: Output path mapped to file content.
    """
    project = tomllib.loads(CONFIG.read_text(encoding="utf-8"))["project"]
    api = load_api()
    pages = [p for p in iter_nav(project["nav"]) if (DOCS / p.path).exists()]
    sources = {p.path: (DOCS / p.path).read_text(encoding="utf-8") for p in pages}
    intro = intro_lines(project, base_url)

    groups: Dict[str, List[str]] = {}
    for page in pages:
        key = "Optional" if page.group in OPTIONAL_GROUPS else page.group
        title = f"{page.group}: {page.title}" if key == "Optional" else page.title
        description = describe(sources[page.path], api)
        entry = f"- [{title}]({page_url(base_url, page.path)})"
        groups.setdefault(key, []).append(f"{entry}: {description}" if description else entry)

    index = list(intro)
    for key in sorted(groups, key=lambda k: k == "Optional"):  # stable: Optional goes last
        index += [f"## {key}", "", *groups[key], ""]

    full = list(intro[:3])
    for page in pages:
        full += [
            "",
            "---",
            "",
            f"<!-- Page: {page.group} / {page.title} | Source: {page_url(base_url, page.path)} -->",
            "",
            render_page(sources[page.path], api),
        ]

    return {
        OUTPUT_INDEX: "\n".join(index).rstrip() + "\n",
        OUTPUT_FULL: "\n".join(full).rstrip() + "\n",
    }


def main(argv: Optional[List[str]] = None) -> int:
    """Write ``docs/llms.txt`` and ``docs/llms-full.txt``.

    :param argv: Command-line arguments; defaults to ``sys.argv[1:]``.
    :return: Process exit code.
    """
    project = tomllib.loads(CONFIG.read_text(encoding="utf-8"))["project"]
    default_base = os.environ.get("FLAUI_DOCS_BASE_URL") or project["site_url"].rstrip("/") + "/latest/"
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base-url", default=default_base, help=f"site root the links point at ({default_base})")
    args = parser.parse_args(argv)
    base_url = args.base_url if args.base_url.endswith("/") else args.base_url + "/"

    for path, content in build(base_url).items():
        path.write_text(content, encoding="utf-8", newline="\n")
        print(f"Written: {path.relative_to(ROOT)} ({len(content.encode('utf-8')) // 1024} KiB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
