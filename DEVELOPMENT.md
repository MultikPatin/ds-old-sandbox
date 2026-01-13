# Инструменты для разработки

Описание предполагает использование uv в качестве менеджера пакетов.  
Документация https://docs.astral.sh/uv/

Ожидаемый результат (версии пакетов указаны на момент написания документации):

```toml
[dependency-groups]
dev = [
    "ruff==0.14.*",
    "mypy==1.19.*",
]
git = [
    "pre-commit==4.5.*",
    "commitizen==4.10.*",
]
build = [
    "hatchling==1.28.*",
    "hatch-vcs==0.5.*",
]
```

Если Вы не разрабатываете пакет, то группа **build** и библиотека **commitizen** не нужны!

## ruff

Документация: https://docs.astral.sh/ruff/  
Документация на правила: https://docs.astral.sh/ruff/rules/  
Документация на конфигурацию: https://docs.astral.sh/ruff/configuration/

#### Установка пакета:

```bash
uv add ruff --group dev
```

Запуска линтера (--fix для автоматического исправления)

```bash
ruff check ./src --fix
```

Запуск форматтера

```bash
ruff format ./src
```

## mypy

Документация: https://mypy.readthedocs.io/en/stable/  
Документация на конфигурацию: https://mypy.readthedocs.io/en/stable/config_file.html

#### Установка пакета:

```bash
uv add mypy --group dev
```

Запуск проверки типов

```bash
mypy ./src
```

## pre-commit

Документация: https://pre-commit.com/  
Документация на конфигурацию: https://pre-commit.com/#3-hooks

#### Установка пакета:

```bash
uv add pre-commit --group git
```

Установка хуков без использования **commitizen**:

```bash
pre-commit install
```

Установка хуков c **commitizen**:

```bash
pre-commit install --hook-type commit-msg
```

Что бы вручную прогнать хуки, выполните:

```bash
pre-commit run --all-files
```

## commitizen

Документация: https://commitizen-tools.github.io/commitizen/  

#### Установка пакета:

```bash
uv add commitizen --group git
```

## hatching

Документация: https://hatch.pypa.io/latest/  
Документация на конфигурацию: https://hatch.pypa.io/latest/config/metadata/

Используется для сборки пакетов.   
**Не предполагается использование разработчикам напрямую.**

#### Установка пакетов:

```bash
 uv add hatchling hatch-vcs --group build
```
