from config import Get_db_connection
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re 
from  typing import Optional


app = FastAPI()

@app.post("/")
def home():
    return {"message":{"Welcome to Book Store"}}

@app.post("/shelf")
def get_details():
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
    