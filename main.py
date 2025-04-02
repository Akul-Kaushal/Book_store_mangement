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
    page_size: int = 10,
    page: int = 0,
@app.post("/shelf/")
async def get_details(object: filter):
    '''
    Display Feature, to display the books in the store  
    param : none
    '''
    conn = Get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        query = f"select * from shelf where 1=1"
        offset = (object.page-1)*object.page_size
        params = []
        if object.genre is None:
            query += ""
        else:
            query += " and genre = %s"
            params.append(object.genre)
        if object.status is None:
            query += ""
        else:
            query += " and status = %s"
            params.append(object.status)
        query += " limit %s offset %s"
        params.extend([object.page_size,offset])

        cursor.execute(query,tuple(params))
        # conn.commit()
        response = cursor.fetchall()
        return {"response":response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
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
        cursor.execute("insert into cart (book_id, product, price, quantity) values (1, 'Harry Potter', 19.99, 1) on duplicate key update quantity = quantity + 1;")
        return {"message":"Added item to cart"}
    except Exception as e:
        raise HTTPException(status_code=221,detail=str(e))
    finally:
        cursor.close()
        conn.close()

