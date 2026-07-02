from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session,engine
import database_model
from sqlalchemy.orm import Session

app=FastAPI()

# List of origins (frontend URLs) allowed to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"] ,  # React dev server
     allow_methods=["*"]
    # "http://127.0.0.1:3000",   # alternative
    )


#to create table in connected database
database_model.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "wellcome to Zahid Center"

products=[
    Product(id=1,name="samsung",description="smart phone",price=999,quantity=5),
    Product(id=2,name="iphone",description="i phone 14",price=2000,quantity=3),
    Product(id=3,name="laptom",description="del 14 inspiration",price=856,quantity=3),
    Product(id=4,name="PS5",description="GTA 6",price=852,quantity=4)  ]

#add the proctus list to db
def init_db():
    db=session()

    #every time we realod it add to db where it already exit same same data, we shoudl add when no rwos exit
    count=db.query(database_model.Product).count()

    if count==0:
        for product in products:
            db.add(database_model.Product(**product.model_dump()))
        db.commit()
init_db()

#dependecy injection
def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close

#fetch all the products 
@app.get("/products")
def get_all_products(db:Session=Depends(get_db)):
    db_products=db.query(database_model.Product).all()   
    return db_products

#Read only one product
@app.get("/products/{id}")
def get_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
        return db_product
    else:
        return "product not found"

#add a product
@app.post("/products")
def add_product(product:Product,db:Session=Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

#update a product
@app.put("/products/{id}")
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
            db_product.name=product.name
            db_product.description=product.description
            db_product.price=product.price
            db_product.quantity=product.quantity
            db.commit()
            return f"product with id:{id} updates successfully "
       
    return "No proudct found"

#delete a proudct
@app.delete("/products/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_model.Product).filter(database_model.Product.id==id).first()
    if db_product:
            db.delete(db_product)
            db.commit()
            return f"product with id:{id} deleted successfully"
    return "proudct not found"