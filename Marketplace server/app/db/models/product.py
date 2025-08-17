from sqlalchemy import Boolean, String, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str] = mapped_column(String(500))
    stock: Mapped[Boolean] = mapped_column(Boolean, default=True)
    is_available: Mapped[Boolean] = mapped_column(Boolean, default=True)








