from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut



router = APIRouter(prefix='/products', tags=['Products'])


# Получение списка продуктов
@router.get("/", response_model=list[ProductOut])
async def read_products(
        db: AsyncSession = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    result = await db.execute(select(Product).offset(skip).limit(limit))
    return result.scalars().all()


# Получение одного продукта
@router.get("/{product_id}", response_model=ProductOut)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


# Создание продукта
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
        product_data: ProductCreate,
        db: AsyncSession = Depends(get_db)
):
    db_product = Product(**product_data.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


# Обновление продукта
@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
        product_id: int,
        product_data: ProductUpdate,
        db: AsyncSession = Depends(get_db)
):
    db_product = await db.get(Product, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for field, value in product_data.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product


# Частичное обновление продукта
@router.patch("/{product_id}", response_model=ProductOut)
async def patch_product(
        product_id: int,
        product_data: ProductUpdate,
        db: AsyncSession = Depends(get_db)
):
    return await update_product(product_id, product_data, db)


# Удаление продукта
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db)
):
    product = await db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()
    return None



