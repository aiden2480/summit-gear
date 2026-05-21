import uuid
from typing import List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (CheckConstraint("role IN ('user', 'admin')"))

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")
    cart: List["CartItem"] = Relationship(back_populates="user", cascade_delete=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "role": self.role,
        }

class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(default=None, primary_key=True)
    name: str
    description: str
    price: float
    image_url: str
    category: str
    stock: int = 0
    cart_items: List["CartItem"] = Relationship(back_populates="product", cascade_delete=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "image_url": self.image_url,
            "category": self.category,
            "stock": self.stock,
        }


class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"

    id: int = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id")
    user_id: uuid.UUID = Field(foreign_key="users.id")
    quantity: int = 1
    product: Product = Relationship(back_populates="cart_items")
    user: User = Relationship(back_populates="cart")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "name": self.product.name,
            "price": self.product.price,
            "image_url": self.product.image_url,
            "stock": self.product.stock,
            "user_id": str(self.user_id),
        }
