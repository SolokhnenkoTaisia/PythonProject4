import pytest

from src.products import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счётчики перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def products():
    """Создаёт список тестовых товаров."""
    return [
        Product("Samsung", "Смартфон Samsung", 100000.0, 5),
        Product("iPhone", "Смартфон Apple", 120000.0, 3),
        Product("Xiaomi", "Смартфон Xiaomi", 30000.0, 10),
    ]


def test_product_initialization():
    """Проверяет правильность создания товара."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    assert product.name == "Samsung"
    assert product.description == "Смартфон"
    assert product.price == 100000.0
    assert product.quantity == 5


def test_category_initialization(products):
    """Проверяет правильность создания категории."""
    category = Category("Смартфоны", "Мобильные телефоны", products)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert "Samsung, 100000.0 руб. Остаток: 5 шт.\n" in category.products
    assert "iPhone, 120000.0 руб. Остаток: 3 шт.\n" in category.products
    assert "Xiaomi, 30000.0 руб. Остаток: 10 шт.\n" in category.products


def test_category_count_increases(products):
    """Проверяет подсчёт созданных категорий."""
    Category("Смартфоны", "Мобильные телефоны", products)
    Category("Телевизоры", "Телевизоры для дома", [])

    assert Category.category_count == 2


def test_product_count_increases(products):
    """Проверяет подсчёт товаров в категориях."""
    Category("Смартфоны", "Мобильные телефоны", products)
    Category("Телевизоры", "Телевизоры для дома", [])

    assert Category.product_count == 3


def test_empty_category():
    """Проверяет создание пустой категории."""
    category = Category("Пустая категория", "Пока нет товаров", [])

    assert category.products == ""


def test_category_counters_are_shared():
    """Проверяет общие счётчики категорий."""
    Category("Первая", "Первая категория", [])
    Category("Вторая", "Вторая категория", [])

    assert Category.category_count == 2


def test_add_product(products):
    """Проверяет добавление товара в категорию."""
    category = Category("Смартфоны", "Мобильные телефоны", [])
    product = products[0]

    result = category.add_product(product)

    assert result is None
    assert "Samsung, 100000.0 руб. Остаток: 5 шт.\n" in category.products
    assert Category.product_count == 1


def test_products_is_private(products):
    """Проверяет отсутствие публичного атрибута products в экземпляре."""
    category = Category("Смартфоны", "Мобильные телефоны", products)

    assert "products" not in category.__dict__
    assert "_Category__products" in category.__dict__


def test_product_price_setter():
    """Проверяет изменение цены товара."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    product.price = 110000.0

    assert product.price == 110000.0


@pytest.mark.parametrize("invalid_price", [0, -1, -100.0])
def test_invalid_price_is_not_set(invalid_price, capsys):
    """Проверяет отказ от нулевой и отрицательной цены."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    product.price = invalid_price

    assert product.price == 100000.0
    assert "Цена не должна быть нулевая или отрицательная" in capsys.readouterr().out


def test_price_is_private():
    """Проверяет хранение цены в приватном атрибуте."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    assert "_Product__price" in product.__dict__
    assert "price" not in product.__dict__


def test_new_product():
    """Проверяет создание товара из словаря."""
    product_data = {
        "name": "Samsung",
        "description": "Смартфон",
        "price": 100000.0,
        "quantity": 5,
    }

    product = Product.new_product(product_data)

    assert isinstance(product, Product)
    assert product.name == "Samsung"
    assert product.description == "Смартфон"
    assert product.price == 100000.0
    assert product.quantity == 5


def test_new_product_merges_duplicates():
    """Проверяет объединение одинаковых товаров."""
    existing = Product("Samsung", "Смартфон", 100000.0, 5)
    products_list = [existing]

    product_data = {
        "name": "samsung",
        "description": "Другая модель описания",
        "price": 110000.0,
        "quantity": 3,
    }

    result = Product.new_product(product_data, products_list)

    assert result is existing
    assert existing.quantity == 8
    assert existing.price == 110000.0
    assert len(products_list) == 1


def test_new_product_keeps_higher_existing_price():
    """Проверяет сохранение более высокой существующей цены."""
    existing = Product("Samsung", "Смартфон", 120000.0, 5)
    products_list = [existing]

    product_data = {
        "name": "Samsung",
        "description": "Смартфон",
        "price": 100000.0,
        "quantity": 2,
    }

    result = Product.new_product(product_data, products_list)

    assert result is existing
    assert existing.quantity == 7
    assert existing.price == 120000.0
