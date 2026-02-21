# Zuban pre-commit hooks

[Pre-commit](https://pre-commit.com/)/[Prek](https://prek.j178.dev/) hook for [Zuban](https://github.com/zubanls/zuban).

## Using with `pre-commit`

Example `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/dunossauro/zuban-pre-commit
    rev: v0.6.0
    hooks:
      # Run `zuban check`
      - id: zuban
        args: [--pretty]  # optional

      # Run `zuban check` in mypy-compatible mode
      - id: zmypy
        args: [--warn-unreachable]  # optional
```

Command-line arguments are optional. You can read more about the available options in the [Zuban CLI documentation](https://docs.zubanls.com/en/latest/usage.html#type-checking-command-line).

Most configuration should live in:

- `pyproject.toml` under `[tool.zuban]`, or
- `mypy.ini`

See the [configuration reference](https://docs.zubanls.com/en/latest/usage.html#configuration) for more details.

> **Note**
>
> `zuban check` may run in default or mypy-compatible mode depending on your configuration.
> Use the `zmypy` hook to explicitly force mypy-compatible behavior.

## Using with `prek`

Example `prek.toml`:

```toml
[[repos]]
repo = "https://github.com/dunossauro/zuban-pre-commit"
rev = "v0.6.0"

hooks = [
  { id = "zuban", args = ["--pretty"] },            # default / auto-detected mode
  { id = "zmypy", args = ["--warn-unreachable"] },  # force mypy-compatible mode
]
```
