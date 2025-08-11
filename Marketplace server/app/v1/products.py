from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from app.db.session import get_db
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductOut



router = APIRouter(prefix='/products', tags=['Products'])


@router.get('/',responses=list[ProductOut])
async def get_products():


