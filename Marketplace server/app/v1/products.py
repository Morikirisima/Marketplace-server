from fastapi import APIRouter, Depends, HTTPException, status
from markdown.extensions.toc import stashedHTML2text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.db.session import get_db
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut



router = APIRouter(prefix='/products', tags=['Products'])


@router.get("/", response_model=list[ProductOut])
async def read_products(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")



