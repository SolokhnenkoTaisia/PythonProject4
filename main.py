from src.products import Category, LawnGrass, Smartphone

if __name__ == "__main__":
    smartphone1 = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )

    smartphone2 = Smartphone(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8,
        98.2,
        "15",
        512,
        "Gray space",
    )

    smartphone3 = Smartphone(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        14,
        90.3,
        "Note 11",
        1024,
        "Синий",
    )

    for smartphone in [smartphone1, smartphone2, smartphone3]:
        print(smartphone.name)
        print(smartphone.description)
        print(smartphone.price)
        print(smartphone.quantity)
        print(smartphone.efficiency)
        print(smartphone.model)
        print(smartphone.memory)
        print(smartphone.color)
        print()

    grass1 = LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )

    grass2 = LawnGrass(
        "Газонная трава 2",
        "Выносливая трава",
        450.0,
        15,
        "США",
        "5 дней",
        "Темно-зеленый",
    )

    for grass in [grass1, grass2]:
        print(grass.name)
        print(grass.description)
        print(grass.price)
        print(grass.quantity)
        print(grass.country)
        print(grass.germination_period)
        print(grass.color)
        print()

    smartphone_sum = smartphone1 + smartphone2
    print(smartphone_sum)

    grass_sum = grass1 + grass2
    print(grass_sum)

    try:
        invalid_sum = smartphone1 + grass1
    except TypeError:
        print("Возникла ошибка TypeError при попытке сложения")
    else:
        print("Не возникла ошибка TypeError при попытке сложения")

    category_smartphones = Category(
        "Смартфоны",
        "Высокотехнологичные смартфоны",
        [smartphone1, smartphone2],
    )

    category_grass = Category(
        "Газонная трава",
        "Различные виды газонной травы",
        [grass1, grass2],
    )

    category_smartphones.add_product(smartphone3)

    print(category_smartphones.products)
    print(Category.product_count)

    try:
        category_smartphones.add_product("Not a product")
    except TypeError:
        print("Возникла ошибка TypeError при добавлении не продукта")
    else:
        print("Не возникла ошибка TypeError при добавлении не продукта")
