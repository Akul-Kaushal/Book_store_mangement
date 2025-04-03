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



class CartItem(BaseModel):
    product_id: int 
    action: str

@app.post("/cart/update")
async def update_cart(item: CartItem):
    conn = Get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT product_id, product, price FROM shelf WHERE product_id = %s", (item.product_id,))
        product_details = cursor.fetchone()
        cursor.execute("select quantity from record where product_id=%s",(item.product_id,))
        record_quantity_check = cursor.fetchone()

        if not product_details:
            raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found in shelf.")

        check_cart_query = "SELECT quantity FROM cart WHERE product_id = %s"
        cursor.execute(check_cart_query, (item.product_id,))
        cart_item = cursor.fetchone()

        if item.action == "add":
            if cart_item:
                if (record_quantity_check.quantity <= cart_item.quantity):
                    update_query = "UPDATE cart SET quantity = quantity + 1 WHERE product_id = %s"
                    cursor.execute(update_query, (item.product_id,))
                elif  (record_quantity_check.quantity <= cart_item.quantity):
                    update_record_quantity = "update record set quantity = %s"
                    cursor.execute(update_record_quantity,("booked"))
            else:
                insert_query = """
                    INSERT INTO cart (product_id, product, price, quantity)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (product_details["id"], product_details["product"], product_details["price"], 1))


        elif item.action == "remove":
            if cart_item and cart_item["quantity"] > 1:
                update_query = "UPDATE cart SET quantity = quantity - 1 WHERE product_id = %s"
                cursor.execute(update_query, (item.product_id,))
            elif cart_item and cart_item["quantity"] == 1:
                delete_query = "DELETE FROM cart WHERE product_id = %s"
                cursor.execute(delete_query, (item.product_id,))
            else:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found in cart.")
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'add' or 'remove'.")

        conn.commit()
        cursor.execute("SELECT * FROM cart")
        updated_cart = cursor.fetchall()
        return {"message": f"Cart updated successfully.", "cart": updated_cart}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    finally:
        cursor.close()
        conn.close()
