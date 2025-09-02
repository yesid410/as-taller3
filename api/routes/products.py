from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product

router = APIRouter()

@router.get("/")
async def get_products(db: Session = Depends(get_db)):
    # TODO: Implementar obtener lista de productos
    products = db.query(Product).all()
    return products

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener producto por ID
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product


@router.post("/")
async def create_product(
    name: str, description: str, price: float, stock: int, image_url: str = None,
    db: Session = Depends(get_db)
):
    # TODO: Implementar crear producto (admin)
    new_product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Producto creado correctamente", "product": new_product}

@router.put("/{product_id}")
async def update_product(
    product_id: int,
    name: str = None,
    description: str = None,
    price: float = None,
    stock: int = None,
    image_url: str = None,
    db: Session = Depends(get_db)
):
    # TODO: Implementar actualizar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    if name:
        product.name = name
    if description:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    if image_url:
        product.image_url = image_url

    db.commit()
    db.refresh(product)
    return {"message": "Producto actualizado correctamente", "product": product}


@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar eliminar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")

    db.delete(product)
    db.commit()
    return {"message": "Producto eliminado correctamente"}