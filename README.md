# ShopEase - E-Commerce Web Application

## Project Overview

ShopEase is a Django-based e-commerce application that allows users to browse products, search by name, filter by category, add products to a shopping cart, and place orders.

It also provides a REST API for managing products and categories.

## Features

- Product listing and product details
- Product search and category filtering
- Shopping cart management
- User registration and login
- Checkout and order creation
- Stock management
- Django administration dashboard
- REST API for products and categories
- Staff-only API access for creating, updating, and deleting products and categories

## Technologies Used

- Python
- Django
- Django REST Framework
- HTML and CSS
- SQLite
- Pillow
- Postman

## Local Installation

1. Clone the repository.
2. Open the project folder in your terminal.
3. Create and activate a virtual environment.
4. Install dependencies.
5. Apply migrations.
6. Start the development server.

Example commands:

```bash
python -m venv venv
pip install django djangorestframework pillow
python manage.py migrate
python manage.py runserver 8001
```

## Local URLs

- Homepage: http://127.0.0.1:8001/
- Admin dashboard: http://127.0.0.1:8001/admin/
- Product API: http://127.0.0.1:8001/api/products/
- Category API: http://127.0.0.1:8001/api/categories/

## API Documentation

See [api_docs.md](api_docs.md) for API endpoints, permissions, and expected response codes.

## API Testing

The API endpoints have been tested using Postman.

The Postman collection is available at:

`postman/ShopEase_API_Tests_Sanitized.postman_collection.json`

It covers listing, retrieving, creating, updating, and deleting products and categories.

## Security

- Secret keys should be stored in environment variables.
- `.env` files and database files should not be committed to Git.
- Production deployment must use `DEBUG=False` and an appropriate `ALLOWED_HOSTS` setting.

## Important Notes

Checkout creates orders and updates product stock. It does not currently process real payments.

## Deployment

Live HTTPS URL: To be added after deployment.

## Repository

GitHub: https://github.com/sammypee0214-cpu/Final-project-ShopEase
