# Book Store API
Welcome to the Book Store API! This project is a backend implementation for managing a book store, including features like inventory management, cart operations, checkout, and transaction handling. Built using FastAPI and MySQL, this API supports efficient and scalable operations.

## Features
  1. Shelf Management:

  - Display books available in the store.

  - Filter by genre and status (e.g., available, booked, out_of_stock).

  2. Cart Operations:

  - Add items to the cart.

  - Remove items or adjust quantities.

  - Validate stock availability before checkout.

  3. Checkout:

  - Process purchases from the cart.

  - Update inventory (record table).

  - Record transactions in the transaction table.

  4. Transaction Management:

  - Record each purchase with unique transaction IDs.

  - Fetch transaction history for auditing purposes.

  5. Inventory Updates:

  - Automatically update product status (available, out_of_stock) based on stock levels.

  6. Tech Stack
  - Backend Framework: FastAPI

  - Database: MySQL

  - Language: Python

  - UUID Generation: Python's uuid module

## Installation
1. Clone the Repository
```bash
  git clone https://github.com/Akul-Kaushal/Book_store_mangement.git
  cd Book_store_mangement
```
2. Set Up Virtual Environment
```bash
  python -m venv .venv
  source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```
3. Install Dependencies
```bash
  pip install fastapi uvicorn mysql-connector-python python-dotenv
```
4. Configure .env File
Create a .env file in the root directory with your database credentials:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=book_store_db
```


## Run the Server Locally:
```bash
uvicorn main:app --reload
```
API Endpoints
Shelf Management:
```text
GET /shelf/: Fetch all books with optional filters (genre, status, pagination).

POST /shelf/: Add new books to the store.

Cart Operations:
POST /cart/update: Add or remove items from the cart.
```
Request Body:
```raw
json
{
    "product_id": 101,
    "action": "add"
}
Checkout:
POST /checkout: Process checkout and record transactions.

Request Body:

json
{
    "user_id": "user_123"
}
Transactions:
GET /transactions: Fetch all transactions or filter by user ID.

Error Handling
Common Errors:
Duplicate Transaction ID:

json
{
    "detail": "Transaction failed: Duplicate entry for key 'transaction.PRIMARY'"
}
Fix: Ensure unique transaction IDs using UUIDs.

Insufficient Stock:

json
{
    "detail": "Insufficient stock for product ID."
}
Empty Cart:

json
{
    "detail": "Cart is empty."
}
```
Future Enhancements
  - 🎯Integrate payment gateways like PayPal or Stripe.

  - 🔐Add user authentication and authorization (JWT).

  - 📜Implement advanced search and sorting for books.


Contributing
Feel free to contribute by submitting issues or pull requests!
