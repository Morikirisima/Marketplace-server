from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Example: Футболка")
    price: float = Field(..., gt=0, description="Example: 849.99")
    description: Optional[str] = Field(None, max_length=500)
    stock: int = Field(default=0, ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(None, min_length=2, max_length=100)
    price: float = Field(None, gt=0)
    description: Optional[str] = None
    stock: int = Field(None, ge=0)


class ProductOut(BaseModel):
    id: int
    is_available: bool

    model_config = ConfigDict(from_attributes=True)