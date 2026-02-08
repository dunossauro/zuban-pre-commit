# Zuban pre-commit hooks

Example for `.pre-commit-config.yaml`:

```yaml
repos:
- repo: https://github.com/dunossauro/zuban-pre-commit
  rev: v0.5.0
  hooks:
    # for zuban check
    - id: zuban
      args: [ --strict ]  # optional
    # for zuban mypy check
    - id: zmypy
      args: [ --warn-unreachable ]  # optional
```

Command-line arguments are optional; most configuration should live in `pyproject.toml` (`[tool.zuban]`) or `mypy.ini`.


> Note:
> `zuban check` may run in default or mypy-compatible mode depending on your configuration.
> Use the `zmypy` hook to force mypy behavior.


Example for `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/dunossauro/zuban-pre-commit"
rev = "v0.5.0"
hooks = [
  { id = "zuban", args = ["--strict"] },            # default / auto-detected mode
  { id = "zmypy", args = ["--warn-unreachable"] },  # force mypy-compatible mode
]
```
