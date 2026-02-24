# Ecommerce-PEP

A full-featured e-commerce web application built with Django, allowing users to browse products, manage carts, and place orders securely.

## Features

- User Authentication (Signup/Login/Profile)
- Category & Subcategory Filtering
- Product Search & Sorting
- Shopping Cart & Wishlist
- Order Placement & Order History
- Admin Panel for Product Management

## Project Architecture

- Django MVT Pattern
- Modular Apps (accounts, products, cart, orders)
- SQLite Database

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `venv\Scripts\activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Apply migrations: `python manage.py migrate`
6. Run the server: `python manage.py runserver`
