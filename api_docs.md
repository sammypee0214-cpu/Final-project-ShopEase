# ShopEase API Documentation

## Base URL

Local development: `http://127.0.0.1:8001/`

## Authentication and Permissions

- GET requests are publicly accessible.
- POST, PUT, PATCH, and DELETE requests require an authenticated staff user.
- Write requests use Django REST Framework's `IsAdminUser` permission.

## Product Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/products/` | List available products |
| GET | `/api/products/<product_id>/` | Retrieve one product |
| POST | `/api/products/create/` | Create a product |
| PUT/PATCH | `/api/products/<product_id>/update/` | Update a product |
| DELETE | `/api/products/<product_id>/delete/` | Delete a product |

## Category Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/categories/` | List categories |
| GET | `/api/categories/<category_id>/` | Retrieve one category |
| POST | `/api/categories/create/` | Create a category |
| PUT/PATCH | `/api/categories/<category_id>/update/` | Update a category |
| DELETE | `/api/categories/<category_id>/delete/` | Delete a category |

## Expected HTTP Status Codes

- `200 OK` — Successful GET, update, or delete.
- `201 Created` — Successful creation.
- `400 Bad Request` — Invalid request data.
- `403 Forbidden` — User lacks permission.
- `404 Not Found` — Requested resource does not exist.
- `405 Method Not Allowed` — Unsupported HTTP method.

## Testing

The endpoints have been tested using Postman. The collection includes product and category list, detail, create, update, and delete requests.

## Important Notes

- The product list returns products marked as available.
- Checkout creates orders and order items and updates stock.
- Checkout does not process real payments.
- Product deletion may be prevented when an existing order item references that product.
