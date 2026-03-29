from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id          = Column(Integer, primary_key=True)
    name        = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price       = Column(Float, nullable=False)
    image_url   = Column(String, nullable=False)
    category    = Column(String, nullable=False)
    stock       = Column(Integer, nullable=False, default=0)
    cart_items  = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

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


class CartItem(Base):
    __tablename__ = "cart_items"

    id         = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity   = Column(Integer, nullable=False, default=1)
    product    = relationship("Product", back_populates="cart_items")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "name": self.product.name,
            "price": self.product.price,
            "image_url": self.product.image_url,
            "stock": self.product.stock,
        }
