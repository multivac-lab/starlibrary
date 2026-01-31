from __future__ import annotations

import html
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Node:
    kind: str
    text: str


def _escape(s: str) -> str:
    return html.escape(s, quote=False)


_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_CODE_INLINE_RE = re.compile(r"`([^`]+)`")


def _inline_format(s: str) -> str:
    s = _escape(s)
    s = _CODE_INLINE_RE.sub(lambda m: f"<code>{_escape(m.group(1))}</code>", s)
    s = _LINK_RE.sub(lambda m: f"<a href=\"{_escape(m.group(2))}\">{_escape(m.group(1))}</a>", s)
    return s


def parse_markdown(lines: Iterable[str]) -> list[Node]:
    """A deliberately tiny markdown parser.

    Supported:
    - # / ## / ### headings
    - unordered lists (- / * )
    - fenced code blocks ```
    - paragraphs
    - inline `code` and [links](url)

    Everything else is treated as plain text.
    """

    nodes: list[Node] = []
    in_code = False
    code_buf: list[str] = []
    para_buf: list[str] = []
    list_buf: list[str] = []

    def flush_para() -> None:
        nonlocal para_buf
        if para_buf:
            text = " ".join(x.strip() for x in para_buf).strip()
            if text:
                nodes.append(Node("p", text))
        para_buf = []

    def flush_list() -> None:
        nonlocal list_buf
        if list_buf:
            nodes.append(Node("ul", "\n".join(list_buf)))
        list_buf = []

    for raw in lines:
        line = raw.rstrip("\n")

        if line.strip().startswith("```"):
            if in_code:
                nodes.append(Node("code", "\n".join(code_buf)))
                code_buf = []
                in_code = False
            else:
                flush_para()
                flush_list()
                in_code = True
            continue

        if in_code:
            code_buf.append(line)
            continue

        if not line.strip():
            flush_para()
            flush_list()
            continue

        m = re.match(r"^(#{1,3})\s+(.*)$", line)
        if m:
            flush_para()
            flush_list()
            level = len(m.group(1))
            nodes.append(Node(f"h{level}", m.group(2).strip()))
            continue

        m = re.match(r"^\s*[-*]\s+(.*)$", line)
        if m:
            flush_para()
            list_buf.append(m.group(1).strip())
            continue

        para_buf.append(line)

    flush_para()
    flush_list()

    if in_code:
        nodes.append(Node("code", "\n".join(code_buf)))

    return nodes


def render_html(nodes: list[Node]) -> str:
    out: list[str] = []
    for n in nodes:
        if n.kind.startswith("h"):
            out.append(f"<{n.kind}>{_inline_format(n.text)}</{n.kind}>")
        elif n.kind == "p":
            out.append(f"<p>{_inline_format(n.text)}</p>")
        elif n.kind == "ul":
            items = "\n".join(f"<li>{_inline_format(x)}</li>" for x in n.text.splitlines())
            out.append(f"<ul>\n{items}\n</ul>")
        elif n.kind == "code":
            out.append(f"<pre><code>{html.escape(n.text)}</code></pre>")
        else:
            out.append(f"<p>{_escape(n.text)}</p>")
    return "\n".join(out) + "\n"
