import pytest

from src.products import Category, Product


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счётчики категорий перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def product():
    """Создаёт тестовый товар."""
    return Product(
        name="Samsung Galaxy S23 Ultra",
        description="Смартфон с камерой 200 Мп",
        price=180000.0,
        quantity=5,
    )


@pytest.fixture
def products():
    """Создаёт список тестовых товаров."""
    return [
        Product("Samsung", "Смартфон", 100000.0, 5),
        Product("iPhone", "Смартфон", 120000.0, 3),
        Product("Xiaomi", "Смартфон", 30000.0, 10),
    ]


def test_product_initialization(product):
    """Проверяет правильность инициализации товара."""
    assert product.name == "Samsung Galaxy S23 Ultra"
    assert product.description == "Смартфон с камерой 200 Мп"
    assert product.price == 180000.0
    assert product.quantity == 5


def test_category_initialization(products):
    """Проверяет правильность инициализации категории."""
    category = Category("Смартфоны", "Мобильные телефоны", products)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные телефоны"
    assert category.products == (
        "Samsung, 100000.0 руб. Остаток: 5 шт.\n"
        "iPhone, 120000.0 руб. Остаток: 3 шт.\n"
        "Xiaomi, 30000.0 руб. Остаток: 10 шт.\n"
    )


def test_category_count_increases(products):
    """Проверяет подсчёт созданных категорий."""
    Category("Смартфоны", "Мобильные телефоны", products)
    Category("Телевизоры", "Телевизоры для дома", [])

    assert Category.category_count == 2


def test_product_count_increases(products):
    """Проверяет подсчёт товаров во всех категориях."""
    Category("Смартфоны", "Мобильные телефоны", products)
    Category("Телевизоры", "Телевизоры для дома", [Product("TV", "Телевизор", 50000.0, 2)])

    assert Category.product_count == 4


def test_empty_category():
    """Проверяет создание категории без товаров."""
    category = Category("Пустая категория", "Пока нет товаров", [])

    assert category.products == ""


def test_category_counters_are_shared(products):
    """Проверяет общие счётчики класса Category."""
    category1 = Category("Смартфоны", "Мобильные телефоны", products)
    category2 = Category("Телевизоры", "Телевизоры для дома", [])

    assert category1.category_count == category2.category_count == 2
    assert category1.product_count == category2.product_count == 3


def test_product_str():
    """Проверяет строковое представление товара."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    assert str(product) == "Samsung, 100000.0 руб. Остаток: 5 шт."


def test_category_str(products):
    """Проверяет строковое представление категории."""
    category = Category("Смартфоны", "Мобильные телефоны", products)

    assert str(category) == "Смартфоны, количество продуктов: 18 шт."


def test_product_add():
    """Проверяет сложение общей стоимости товаров."""
    product1 = Product("Samsung", "Смартфон", 100.0, 10)
    product2 = Product("iPhone", "Смартфон", 200.0, 2)

    assert product1 + product2 == 1400.0


def test_empty_category_str():
    """Проверяет строковое представление пустой категории."""
    category = Category("Пустая категория", "Пока нет товаров", [])

    assert str(category) == "Пустая категория, количество продуктов: 0 шт."


def test_product_price_setter_valid():
    """Проверяет изменение цены товара."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    product.price = 120000.0

    assert product.price == 120000.0


def test_product_price_setter_invalid(capsys):
    """Проверяет, что отрицательная цена не устанавливается."""
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    product.price = -100.0

    assert product.price == 100000.0
    assert capsys.readouterr().out.strip() == ("Цена не должна быть нулевая или отрицательная")


def test_new_product_creation():
    """Проверяет создание нового товара."""
    product_data = {
        "name": "Samsung",
        "description": "Смартфон",
        "price": 100000.0,
        "quantity": 5,
    }

    product = Product.new_product(product_data)

    assert product.name == "Samsung"
    assert product.price == 100000.0
    assert product.quantity == 5


def test_new_product_merge():
    """Проверяет объединение одинаковых товаров."""
    existing_product = Product("Samsung", "Смартфон", 100000.0, 5)
    product_data = {
        "name": "samsung",
        "description": "Новый смартфон",
        "price": 120000.0,
        "quantity": 3,
    }

    result = Product.new_product(product_data, [existing_product])

    assert result is existing_product
    assert result.quantity == 8
    assert result.price == 120000.0


def test_new_product_merge_lower_price():
    """Проверяет, что при объединении цена не уменьшается."""
    existing_product = Product("Samsung", "Смартфон", 120000.0, 5)
    product_data = {
        "name": "Samsung",
        "description": "Смартфон",
        "price": 100000.0,
        "quantity": 2,
    }

    result = Product.new_product(product_data, [existing_product])

    assert result.price == 120000.0
    assert result.quantity == 7


def test_category_add_product():
    """Проверяет добавление товара в категорию."""
    category = Category("Смартфоны", "Мобильные телефоны", [])
    product = Product("Samsung", "Смартфон", 100000.0, 5)

    category.add_product(product)

    assert "Samsung, 100000.0 руб. Остаток: 5 шт." in category.products
