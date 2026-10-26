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
    assert category.products == products


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

    assert category.products == []
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_category_counters_are_shared(products):
    """Проверяет общие счётчики класса Category."""
    category1 = Category("Смартфоны", "Мобильные телефоны", products)
    category2 = Category("Телевизоры", "Телевизоры для дома", [])

    assert category1.category_count == category2.category_count == 2
    assert category1.product_count == category2.product_count == 3
