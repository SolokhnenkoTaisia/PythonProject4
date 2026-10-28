class Product:
    """Класс для представления товара."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Возвращает цену товара."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Изменяет цену, если она положительная."""
        if new_price > 0:
            self.__price = new_price
        else:
            print("Цена не должна быть нулевая или отрицательная")

    @classmethod
    def new_product(
        cls,
        product_data: dict,
        products: list["Product"] | None = None,
    ) -> "Product":
        """Создаёт товар или объединяет его с существующим."""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        if products is not None:
            for product in products:
                if product.name.lower() == name.lower():
                    product.quantity += quantity

                    if price > product.price:
                        product.price = price

                    return product

        return cls(
            name=name,
            description=description,
            price=price,
            quantity=quantity,
        )


class Category:
    """Класс для представления категории товаров."""

    category_count = 0
    product_count = 0

    def __init__(
        self,
        name: str,
        description: str,
        products: list[Product],
    ) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строковое представление товаров категории."""
        result = ""

        for product in self.__products:
            result += f"{product.name}, {product.price} руб. " f"Остаток: {product.quantity} шт.\n"

        return result
