# Authentication Setup for E-commerce Product API

This guide explains the authentication system used in the E-commerce Product API and provides steps to test it.

## Overview
The API uses Django's built-in authentication system along with Django REST Framework (DRF) to secure endpoints. For additional security, token-based authentication is implemented using DRF's `TokenAuthentication`.

### Key Features:
1. **Token-Based Authentication**:
   - Each user is issued a unique authentication token after successful login.
   - The token must be included in the `Authorization` header of all API requests requiring authentication.

2. **Permission Classes**:
   - By default, only authenticated users can perform CRUD operations on products and categories.
   - Public endpoints like product listing can be accessed without authentication.

3. **Token Management**:
   - Tokens are generated using `rest_framework.authtoken`.
   - Users can log in to retrieve their token or create new accounts.

---

## Authentication Setup

### Step 1: Enable Token Authentication
Ensure the following is added to `settings.py`:

```python
INSTALLED_APPS += [
    'rest_framework',
    'rest_framework.authtoken',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
```

Run migrations to create the token table:

```bash
python manage.py migrate
```

### Step 2: Generate Tokens for Users
You can generate tokens for existing users using the following Django management command:

```bash
python manage.py drf_create_token <username>
```

Example:
```bash
python manage.py drf_create_token admin
```
This will output a token that the user can use for authentication.

### Step 3: Include Authentication Middleware
DRF automatically manages authentication headers. Ensure you have `api-auth/` configured for session-based authentication:

#### **File: `ecommerce_project/urls.py`**
```python
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),  # Optional for session-based login
]
```

---

## How to Test Authentication

### Prerequisites:
- Ensure you have at least one user created.
- Obtain a token for the user using the management command or by logging in.

### Step 1: Login to Retrieve Token

Use the `/api/token-auth/` endpoint to retrieve a token for the user.

#### Example Request:
```bash
POST /api/token-auth/
Content-Type: application/json

{
  "username": "testuser",
  "password": "testpassword"
}
```

#### Example Response:
```json
{
  "token": "9a8b7c6d5e4f3a2b1c0d123456789abc"
}
```

### Step 2: Authenticate Requests
Include the token in the `Authorization` header of your API requests:

#### Example Request:
```bash
GET /api/products/
Authorization: Token 9a8b7c6d5e4f3a2b1c0d123456789abc
```

### Step 3: Test Protected Endpoints
Try accessing a protected endpoint without the token:

#### Example Request:
```bash
GET /api/products/
```

#### Example Response:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

Now include the token and retry the request.

#### Example Request:
```bash
GET /api/products/
Authorization: Token 9a8b7c6d5e4f3a2b1c0d123456789abc
```

#### Example Response:
```json
[
  {
    "id": 1,
    "name": "Smartphone",
    "description": "A cool smartphone.",
    "price": "699.99",
    "category": "Electronics",
    "stock_quantity": 50,
    "image_url": "http://example.com/image.jpg",
    "created_date": "2025-01-01T12:00:00Z"
  }
]
```

---

## Troubleshooting

1. **Error: Token Not Found**:
   - Ensure the token exists for the user.
   - Use the management command to create a token: `python manage.py drf_create_token <username>`.

2. **Permission Denied**:
   - Ensure the user is authenticated and authorized.
   - Check the `permission_classes` in your views.

3. **Invalid Token**:
   - Verify that the token is correctly included in the `Authorization` header.

---

## Additional Notes
- For improved security, consider implementing JWT (JSON Web Tokens) using libraries like `djangorestframework-simplejwt`.
- Tokens should be securely stored on the client side and not exposed publicly.

This completes the authentication setup and testing guide for the E-commerce Product API.
