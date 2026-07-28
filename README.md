# product-x

End-to-end Sphinx-Needs based repository for ASPICE / ISO 26262 / ISO/SAE
21434 compliant development. See `docs/design_decisions/` for rationale and
`needs_overview.rst` for live traceability.

## Build docs locally
```
pip install sphinx sphinx-needs sphinx-rtd-theme sphinxcontrib-plantuml
sphinx-build -b html . _build/html
```

## Build & test code (Bazel, multi-language)
```
bazel build //...
bazel test //...
```

## Structure
- `requirements/`, `architecture/`, `design/`, `features/` — product enabler
- `tests/` — test enabler
- `safety/` — safety enabler (ISO 26262)
- `security/` — security enabler (ISO/SAE 21434)
- `docs/` — documentation enabler
- `metadata/` — feature/module/component catalogs
- `pipeline/gates/` — CI gate configuration

## Known gaps (not yet resolved — see prior review)
- Security enabler substructure needs sign-off from security lead
- SSR/CR merge point at architecture level is a placeholder convention
- Central vs. per-product CI gate ownership undecided
