import base64
import uuid
from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint, LargeBinary, Column


_PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
_JPEG_MAGIC = b"\xff\xd8\xff"


def _sniff_avatar_mime(data: bytes) -> Optional[str]:
    if data.startswith(_PNG_MAGIC):
        return "image/png"
    if data.startswith(_JPEG_MAGIC):
        return "image/jpeg"
    return None


class User(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint("role IN ('user', 'admin')", name="ck_users_role"),
    )

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    role: str = Field(default="user")
    avatar_blob: Optional[bytes] = Field(default=None, sa_column=Column(LargeBinary, nullable=True))
    cart: List["CartItem"] = Relationship(back_populates="user", cascade_delete=True)

    @property
    def avatar(self) -> Optional[str]:
        if not self.avatar_blob:
            return None
        mime = _sniff_avatar_mime(self.avatar_blob) or "application/octet-stream"
        return f"data:{mime};base64,{base64.b64encode(self.avatar_blob).decode('ascii')}"

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "role": self.role,
            "avatar": self.avatar,
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
