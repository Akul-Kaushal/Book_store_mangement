import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_CONFIG = {
    "host": "localhost",
    "user": os.getenv("USERS"),
    "password": os.getenv("PASSWD"),
    "database": os.getenv("DATABASE"),
}

def Get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)