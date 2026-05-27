import base64
import uuid
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint, LargeBinary, Column


class User(SQLModel, table=True):
    """User account: credentials, role for RBAC, and optional inline avatar."""
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="ck_users_role"),
        CheckConstraint("avatar_mime IN ('image/png', 'image/jpeg')", name="ck_users_avatar_mime"),
        CheckConstraint("(avatar_data IS NULL) = (avatar_mime IS NULL)", name="ck_users_avatar_both_or_neither"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")
    avatar_data: Optional[bytes] = Field(default=None, sa_column=Column(LargeBinary, nullable=True))
    avatar_mime: Optional[str] = Field(default=None, nullable=True)
    cart: List["CartItem"] = Relationship(back_populates="user", cascade_delete=True)

    @property
    def avatar(self) -> Optional[str]:
        if not self.avatar_data or not self.avatar_mime:
            return None

        return f"data:{self.avatar_mime};base64,{base64.b64encode(self.avatar_data).decode('ascii')}"

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "role": self.role,
            "avatar": self.avatar,
        }

class Product(SQLModel, table=True):
    """Catalogue product. Seeded once at startup."""
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
    """A line in a user's cart. One row per (user, product) pair."""
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
