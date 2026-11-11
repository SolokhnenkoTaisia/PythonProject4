import pytest

from src.products import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def product():
    return Product("Телефон", "Описание телефона", 10000.0, 5)


@pytest.fixture
def smartphone():
    return Smartphone(
        "Samsung",
        "Смартфон Samsung",
        80000.0,
        3,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )


@pytest.fixture
def category(product):
    return Category("Техника", "Электронные устройства", [product])


def test_product_init(product):
    assert product.name == "Телефон"
    assert product.description == "Описание телефона"
    assert product.price == 10000.0
    assert product.quantity == 5


def test_product_str(product):
    assert str(product) == "Телефон, 10000.0 руб. Остаток: 5 шт."


def test_product_add():
    product1 = Product("Телефон", "Описание", 100.0, 10)
    product2 = Product("Планшет", "Описание", 200.0, 2)

    assert product1 + product2 == 1400.0


def test_product_add_different_types(product, smartphone):
    with pytest.raises(TypeError):
        product + smartphone


def test_price_setter(product):
    product.price = 15000.0
    assert product.price == 15000.0


def test_price_setter_invalid(product, capsys):
    product.price = -100.0

    assert product.price == 10000.0
    assert "Цена не должна быть нулевая или отрицательная" in (capsys.readouterr().out)


def test_new_product_create():
    data = {
        "name": "Ноутбук",
        "description": "Игровой ноутбук",
        "price": 100000.0,
        "quantity": 3,
    }

    product = Product.new_product(data)

    assert product.name == "Ноутбук"
    assert product.price == 100000.0
    assert product.quantity == 3


def test_new_product_merge_higher_price(product):
    data = {
        "name": "телефон",
        "description": "Новое описание",
        "price": 15000.0,
        "quantity": 2,
    }

    result = Product.new_product(data, [product])

    assert result is product
    assert product.quantity == 7
    assert product.price == 15000.0


def test_new_product_merge_lower_price(product):
    data = {
        "name": "телефон",
        "description": "Новое описание",
        "price": 5000.0,
        "quantity": 2,
    }

    result = Product.new_product(data, [product])

    assert result is product
    assert product.quantity == 7
    assert product.price == 10000.0


def test_category_init(category, product):
    assert category.name == "Техника"
    assert category.description == "Электронные устройства"
    assert str(product) in category.products


def test_category_str(category):
    assert str(category) == "Техника, количество продуктов: 5 шт."


def test_category_products(category):
    assert category.products == ("Телефон, 10000.0 руб. Остаток: 5 шт.\n")


def test_category_add_product(category):
    new_product = Product("Планшет", "Описание", 20000.0, 2)
    category.add_product(new_product)

    assert "Планшет" in category.products


def test_category_add_invalid_product(category):
    with pytest.raises(TypeError):
        category.add_product("Не товар")


def test_smartphone_init(smartphone):
    assert isinstance(smartphone, Product)
    assert smartphone.name == "Samsung"
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_init(lawn_grass):
    assert isinstance(lawn_grass, Product)
    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_smartphone_add():
    smartphone1 = Smartphone("Samsung", "Описание", 80000.0, 2, 95.5, "S23", 256, "Серый")
    smartphone2 = Smartphone("Iphone", "Описание", 100000.0, 3, 98.0, "15", 512, "Черный")

    assert smartphone1 + smartphone2 == 460000.0


def test_lawn_grass_add():
    grass1 = LawnGrass("Трава 1", "Описание", 500.0, 10, "Россия", "7 дней", "Зеленый")
    grass2 = LawnGrass("Трава 2", "Описание", 400.0, 5, "США", "5 дней", "Темно-зеленый")

    assert grass1 + grass2 == 7000.0


def test_different_subclasses_add(smartphone, lawn_grass):
    with pytest.raises(TypeError):
        smartphone + lawn_grass


def test_category_accepts_subclasses(category, smartphone, lawn_grass):
    category.add_product(smartphone)
    category.add_product(lawn_grass)

    assert "Samsung" in category.products
    assert "Газонная трава" in category.products


def test_category_rejects_unrelated_object(category):
    with pytest.raises(TypeError):
        category.add_product(123)
