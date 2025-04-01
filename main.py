from config import Get_db_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re 
from  typing import Optional


app = FastAPI()

@app.post("/")
def home():
    return {"message":{"Welcome to Book Store"}}


# 1: Display/record
class filter(BaseModel):
    genre: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 10,
    offset: int = 0,


@app.post("/shelf/")
async def get_details():
    '''
    Display Feature, to display the books in the store  
    param : none
    '''
    conn = Get_db_connection()
    cursor = conn.cursor()

    try:
        query = f"select * from shelf"
        cursor.execute(query)
        # conn.commit()
        response = cursor.fetchall()
        return {"response":response}
    except Exception as e:
        raise HTTPException(status_code=200,detail=str(e))
    finally:
        cursor.close()
        conn.close()



class cart_item(BaseModel):
    item: str

@app.post("/cart/")
def add_to_cart(object: cart_item):
    conn = Get_db_connection()
    cursor = conn.cursor()

    try:
        return {"message":"Added item to cart"}
    except Exception as e:
        raise HTTPException(status_code=221,detail=str(e))
    finally:
        cursor.close()
        conn.close()

