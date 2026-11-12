from abc import ABC, abstractmethod


class ProductCreationMixin:
    """Миксин для вывода информации о создании объекта."""

    def __init__(self, *args: object, **kwargs: object) -> None:
        print(f"Создан объект {self.__class__.__name__} " f"с параметрами: {args}, {kwargs}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    """Абстрактный базовый класс для товаров."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        **extra_attributes: object,
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price

        if quantity < 0:
            raise ValueError("Количество товара не может быть отрицательным")

        self.quantity = quantity

        for attribute, value in extra_attributes.items():
            setattr(self, attribute, value)

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

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        pass


class Product(ProductCreationMixin, BaseProduct):
    """Класс для представления товара."""

    def __str__(self) -> str:
        """Возвращает строковое представление товара."""
        return f"{self.name}, {self.price} руб. " f"Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Складывает стоимость товаров одного типа."""
        if type(self) is not type(other):
            raise TypeError("Можно складывать только товары одного типа")

        return self.price * self.quantity + other.price * other.quantity

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


class Smartphone(Product):
    """Класс для представления смартфона."""

    efficiency: float
    model: str
    memory: int
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(
            name,
            description,
            price,
            quantity,
            efficiency=efficiency,
            model=model,
            memory=memory,
            color=color,
        )


class LawnGrass(Product):
    """Класс для представления газонной травы."""

    country: str
    germination_period: str
    color: str

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(
            name,
            description,
            price,
            quantity,
            country=country,
            germination_period=germination_period,
            color=color,
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
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только товары")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает строковое представление товаров категории."""
        return "".join(str(product) + "\n" for product in self.__products)

    def __str__(self) -> str:
        """Возвращает строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
