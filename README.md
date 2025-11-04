# E-Commerce Backend API

A Django REST API backend for an e-commerce platform with user management, product catalog, wallet system, and order processing.

## What This Does

This is a backend API for an e-commerce platform where:
- Admins can manage products (create, update, delete)
- Customers can register accounts and manage their profiles
- Each customer has a wallet to store funds
- Customers can purchase products using their wallet balance
- All transactions are tracked and viewable


## Features

**User System:**
- JWT-based authentication
- Role-based access (Admin vs Customer)
- Profile management

**Products:**
- CRUD operations for admins
- Product listing and search for everyone
- Stock tracking
- Bulk import from Excel files

**Wallet:**
- Each customer gets a wallet automatically
- Add funds endpoint
- Transaction history
- Atomic operations to prevent race conditions

**Orders:**
- Purchase products with wallet balance
- Validates stock availability and balance
- Reduces stock and wallet balance atomically
- Complete transaction history

## Tech Stack

- **Backend:** Django 4.2 + Django REST Framework 3.14
- **Auth:** JWT (SimpleJWT)
- **Database:** SQLite (dev)
- **Docs:** Swagger UI (drf-yasg)
- **Excel:** openpyxl
- **Config:** python-decouple

## Quick Start

### 1. Install Dependencies

```bash
# Clone or extract the project
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Set Up Database

```bash
# Run migrations
python manage.py migrate

# Create a superuser (optional, for admin panel)
python manage.py createsuperuser
```

### 3. Load Sample Products

```bash
python manage.py import_products products.xlsx
```

### 4. Start Server

```bash
python manage.py runserver
```

The API will be at http://127.0.0.1:8000/

## Project Structure

```
backend/
├── config/              # Django settings
├── users/               # User auth and management
├── products/            # Product catalog
├── wallet/              # Wallet and transactions
├── orders/              # Purchase orders
├── core/                # Shared utilities
├── products.xlsx        # Sample data
└── requirements.txt
```

## API Endpoints

### Authentication
- `POST /api/users/register/` - Sign up
- `POST /api/users/login/` - Login
- `GET /api/users/profile/` - View profile
- `PUT /api/users/profile/` - Update profile

### Products
- `GET /api/products/` - List products
- `POST /api/products/` - Create product (admin)
- `GET /api/products/{id}/` - Product details
- `PUT /api/products/{id}/` - Update product (admin)
- `DELETE /api/products/{id}/` - Delete product (admin)

### Wallet
- `GET /api/wallet/balance/` - Check balance
- `POST /api/wallet/add-funds/` - Add money
- `GET /api/wallet/transactions/` - Transaction history

### Orders
- `POST /api/orders/purchase/` - Buy a product

## Testing

### Using Postman (Recommended)

**Quick Start:**
1. Import `Ecommerce_API_Collection.postman_collection.json` into Postman
2. Import `Ecommerce_API.postman_environment.json`
3. Run "Register Customer" - token auto-saved
4. Test other APIs in order

**Test Flow:**
- Register Customer
- Add Funds to Wallet
- List Products
- Purchase Product
- View Transaction History

See `API_TESTING_GUIDE.md` for detailed step-by-step instructions.

### Alternative: Swagger UI

- Go to http://127.0.0.1:8000/
- Click "Authorize" and enter Bearer token
- Test endpoints directly in browser

## Management Commands

### Import Products

```bash
python manage.py import_products products.xlsx
```

The Excel file should have columns:
- `name` (required)
- `price` (required)
- `stock_quantity` (required)
- `description` (optional)

The command will:
- Validate all data
- Create new products or update existing ones
- Show you a summary of what was imported

## Configuration

The project uses sensible defaults. If you want to customize:

Create a `.env` file:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Database

By default uses SQLite (in `db.sqlite3`). For production, switch to PostgreSQL by updating the `DATABASES` setting in `config/settings.py`.

## Architecture Notes

**Service Layer Pattern:**
Business logic lives in service classes (`services.py` files), not in views. This makes the code more testable and reusable.

Example:
- `WalletService.credit_wallet(user, amount)` - handles adding funds
- `PurchaseService.create_purchase(customer, product_id, quantity)` - handles the entire purchase flow

**Atomic Transactions:**
Critical operations (purchases, wallet updates) use `@transaction.atomic` and database row locking to prevent race conditions.

**Custom Exceptions:**
Instead of generic errors, the API returns specific exception types with detailed messages (see `core/exceptions.py`).

## Code Quality

- Follows PEP-8 conventions
- Uses type hints
- Service layer for business logic
- Custom validators for data integrity
- Comprehensive error handling

## Files Included

- `README.md` - This file (includes setup and overview)
- `API_TESTING_GUIDE.md` - Complete Postman testing guide
- `requirements.txt` - Python dependencies
- `products.xlsx` - Sample product data
- `Ecommerce_API_Collection.postman_collection.json` - Postman collection
- `Ecommerce_API.postman_environment.json` - Postman environment

## Common Issues

**Port already in use?**
```bash
python manage.py runserver 8001
```

**Database errors?**
```bash
rm db.sqlite3
python manage.py migrate
```

**Module not found?**
Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.

## Admin Panel

Access the Django admin at http://127.0.0.1:8000/admin/ using your superuser credentials.

You can manage users, products, orders, wallets, and transactions from there.



For detailed API testing instructions, check `API_TESTING_GUIDE.md`.
