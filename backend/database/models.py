from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")  # "user" or "admin"
    cart: List["CartItem"] = Relationship(back_populates="user", cascade_delete=True)
    
    def to_dict(self): 
        return {
            "id" : self.id,
            "username" : self.username,
            "role" : self.role
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
    username: str = Field(foreign_key="users.username")
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
            "user_id": self.username
        }
