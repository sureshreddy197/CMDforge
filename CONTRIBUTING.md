# Contributing to CMDforge

Thanks for your interest in contributing.
CMDforge aims to stay focused, readable, and production-friendly, so the bar for changes is less about volume and more about clarity and maintainability.

## Principles

- Prefer small, composable modules over large feature piles.
- Keep command behavior explicit and deterministic.
- Preserve cross-platform behavior where practical.
- Maintain user-facing polish: command wording, help text, and terminal rendering matter.
- Avoid speculative abstractions until the project genuinely needs them.

## Local setup

### Using `uv`

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

### Using `pip`

```bash
python -m pip install -e ".[dev]"
pre-commit install
```

## Development workflow

1. Create a branch for your work.
2. Make focused changes with tests.
3. Run the full validation suite.
4. Open a pull request with a clear description of the behavior change.

Useful commands:

```bash
make format
make lint
make typecheck
make test
make check
```

## Coding standards

- Use type hints where they improve correctness and readability.
- Write docstrings for public functions and modules that benefit from context.
- Keep error messages direct, actionable, and professional.
- Prefer stable interfaces over clever shortcuts.
- Do not add dependencies lightly.

## Tests

Every user-facing command or behavior change should include or update tests.
In particular, validate:

- CLI exit codes
- user-visible output for happy paths and errors
- filesystem effects for config and scaffold behavior
- cross-platform safe path handling where relevant

## Pull requests

A good pull request usually includes:

- a short explanation of the problem being solved
- implementation notes for anything non-obvious
- tests for the new or changed behavior
- docs updates when command semantics or development workflow changed

## Release-minded changes

If your change affects packaging, versioning, docs, or the generated scaffold, review those parts carefully.
CMDforge is intended to be pushed directly to GitHub and used as a reference implementation, so repo-level coherence matters.
