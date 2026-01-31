from __future__ import annotations

import argparse
from pathlib import Path

from .build import build_site


def main() -> None:
    p = argparse.ArgumentParser(prog="starlibrary", description="Build a tiny HTML site from notes/")
    sub = p.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="Build site/ from notes/")
    b.add_argument("--notes", type=Path, default=Path("notes"))
    b.add_argument("--out", type=Path, default=Path("site"))
    b.add_argument("--title", type=str, default="Starlibrary")

    args = p.parse_args()

    if args.cmd == "build":
        build_site(notes_dir=args.notes, out_dir=args.out, title=args.title)


if __name__ == "__main__":
    main()
