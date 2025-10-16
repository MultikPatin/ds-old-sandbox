## Development tools

### Pre commit hooks

install the pre-commit hooks

```bash
uv add --group dev pre-commit
```

First install the pre-commit hooks, run the following command:

```bash
pre-commit install
```

To manual run all the pre-commit hooks, run the following command:

```bash
pre-commit run --all-files
```

### Ruff (lint and format)

Install the ruff lint and format, run the following command:

```bash
uv add --group dev ruff
```

To run the lint, run the following command:

```bash
ruff check ./src --fix
```

To run the format, run the following command:

```bash
ruff format ./src
```

### Mypy (static type checker)

Install the mypy type check, run the following command:

```bash
uv add --group dev mypy
```

To run the type check, run the following command:

```bash
mypy ./src
```
