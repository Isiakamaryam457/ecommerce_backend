# ecommerce_backend
E-Commerce API

A RESTful API for managing an e-commerce platform built with Django and Django REST Framework (DRF).
It supports products, categories, reviews, discounts, orders, wishlists, and product images, providing full CRUD operations and business logic such as discounted prices and stock management.

Table of Contents

Features

Tech Stack

Installation

API Endpoints

Authentication

Models

Example Requests

Pagination

Contributing

License

Features

Manage Products, Categories, and Product Images

CRUD for Reviews

Support for Discounts (percentage & fixed) with validity check

Orders with stock validation and total price calculation

Wishlist management

Automatically calculates discounted prices for products

Nested serialization to include related objects in responses

Soft delete support for categories

Pagination support for lists

Tech Stack

Python 3.14

Django 5.x

Django REST Framework

SQLite (default) or any other DB supported by Django

Optional: JWT / Token authentication

Installation

Clone the repository:

git clone https://github.com/yourusername/ecommerce-backend.git
cd ecommerce-backend

Create a virtual environment and activate it:

python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

Install dependencies:

pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Create a superuser (for admin access):

python manage.py createsuperuser

Run the development server:

python manage.py runserver

API will be available at: http://127.0.0.1:8000/api/

API Endpoints
Categories
Method	Endpoint	Description
GET	/api/categories/	List all categories
GET	/api/categories/<id>/	Retrieve a category
POST	/api/categories/	Create a category
PUT	/api/categories/<id>/	Update a category
DELETE	/api/categories/<id>/	Delete (soft) a category
Products
Method	Endpoint	Description
GET	/api/products/	List all products
GET	/api/products/<id>/	Retrieve a product (includes reviews & category)
POST	/api/products/	Create a product
PUT	/api/products/<id>/	Update a product
DELETE	/api/products/<id>/	Delete a product
Reviews
Method	Endpoint	Description
GET	/api/products/<product_id>/reviews/	List all reviews for a product
GET	/api/products/<product_id>/reviews/<id>/	Retrieve a review
POST	/api/products/<product_id>/reviews/	Create a review
Discounts
Method	Endpoint	Description
GET	/api/products/<product_id>/discounts/	List discounts for a product
POST	/api/products/<product_id>/discounts/	Create a discount
Fields include discount_type, value, start_date, end_date, and is_valid		
Orders
Method	Endpoint	Description
GET	/api/products/orders/	List all orders for the authenticated user
POST	/api/products/orders/	Create an order with items and quantity
Calculates total price automatically and validates stock		
Wishlist
Method	Endpoint	Description
GET	/api/products/wishlist/	Retrieve user wishlist
POST	/api/products/wishlist/add/<product_id>/	Add product to wishlist
POST	/api/products/wishlist/remove/<product_id>/	Remove product from wishlist
Authentication

Uses Django default User model

Protected endpoints require authentication (JWT or Session Auth can be configured)

Read-only endpoints (GET) can be accessed without authentication if desired

Models Overview

Category – name, description, created_by, is_active
Product – name, description, price, category, stock_quantity
ProductImage – image, alt_text, is_primary
Review – user, rating, comment
Discount – product, discount_type, value, start_date, end_date, is_valid
Order & OrderItem – tracks purchases with stock validation
Wishlist – user-specific product list

Example POST Request: Create Order
POST /api/products/orders/
{
  "items": [
    {"product_id": 1, "quantity": 2},
    {"product_id": 3, "quantity": 1}
  ]
}

Response:

{
  "id": 5,
  "user": "john_doe",
  "status": "pending",
  "items": [
    {"product": "Laptop", "quantity": 2, "price": 1500, "total_price": 3000},
    {"product": "Mouse", "quantity": 1, "price": 50, "total_price": 50}
  ],
  "total_price": 3050
}
Pagination

List endpoints are paginated using DRF’s pagination system

Example query:
/api/products/?page=2&page_size=10

Contributing

Fork the repository

Create a feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -am 'Add new feature')

Push to branch (git push origin feature/your-feature)

Open a pull request


