# starlibrary

A tiny static generator for a personal “library” of notes.

- Input: Markdown files in `notes/`
- Output: a clean HTML site in `site/`
- Goal: **zero dependencies** and boring reliability.

This is the first “real” repo in the `multivac-lab` account: a small tool that matches the identity theme —
*turning questions and notes into something browsable*.

## Quickstart

```bash
python -m starlibrary build
```

Then open:

- `site/index.html`

## Project layout

- `starlibrary/` — the generator (Python package)
- `notes/` — markdown sources
- `site/` — generated output (committed for now; can be ignored later)

## Philosophy

1. Keep the format simple.
2. Prefer explicitness over “smart parsing”.
3. Keep it hackable.

## License

MIT.
