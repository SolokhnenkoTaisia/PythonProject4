# Product and Category

Учебный проект на Python для работы с товарами и категориями с использованием объектно-ориентированного программирования (ООП).

## Функциональность

- Класс `Product` хранит название, описание, цену и количество товара.
- Класс `Category` хранит название, описание и список товаров.
- Подсчёт общего количества созданных категорий.
- Подсчёт общего количества товаров во всех категориях.

## Структура проекта

```text
PythonProject4/
├── src/
│   ├── __init__.py
│   └── products.py
├── tests/
│   └── test_products.py
├── main.py
├── README.md
├── .gitignore
├── .flake8
├── pyproject.toml
└── poetry.lock
```

## Используемые технологии

- Python 3.12
- Poetry
- Pytest
- pytest-cov
- Black
- isort
- Flake8

## Установка зависимостей

```bash
poetry install
```

## Запуск программы

```bash
poetry run python main.py
```

## Запуск тестов

```bash
poetry run pytest -v
```

## Проверка покрытия тестами

```bash
poetry run pytest --cov=src --cov-report=term-missing --cov-report=html
```

Последняя команда выводит процент покрытия кода и создаёт HTML-отчёт в папке `htmlcov`.
