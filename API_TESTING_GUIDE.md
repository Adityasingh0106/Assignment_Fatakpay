# API Testing Guide - Using Postman

Okay, so you've got the server running. Now let's test the APIs using Postman. This guide will walk you through the complete user flow - from creating an account to making your first purchase.

## What You Need

**Postman** - If you don't have it, download from https://www.postman.com/downloads/

## Quick Setup

1. **Import the Collection:**
   - Open Postman
   - Click "Import" button
   - Select `Ecommerce_API_Collection.postman_collection.json`
   - Collection will appear in your sidebar

2. **Import the Environment:**
   - Click the gear icon (⚙️) in top right
   - Click "Import"
   - Select `Ecommerce_API.postman_environment.json`
   - Select "E-Commerce API" environment from dropdown

3. **You're Ready!**
   - The collection has 13 APIs ready to test
   - Tokens are saved automatically after login/register
   - Just hit Send and start testing

## Testing Flow (Using Imported Collection)

**Easiest Way - Just follow the order:**

1. **Register Customer** → Sends request, saves token automatically
2. **Add Funds** → Add money to wallet (try 5000)
3. **List Products** → See what's available
4. **Purchase Product** → Buy something (change product_id and quantity as needed)
5. **Transaction History** → View all transactions
6. **Check Balance** → See remaining wallet balance

**That's it!** The collection handles all the authentication for you. Tokens are saved automatically after register/login.

---

## Manual Testing (Step by Step)

Want to understand each API in detail? Follow this guide to manually create and test each request.

## The User Journey

Let me walk you through a realistic scenario: A customer signs up, adds money to their wallet, browses products, and makes a purchase.

---

## Step 1: Register a New Customer

This is where it all starts. We'll create a customer account.

**Endpoint:** `POST /api/users/register/`

**What you need to send:**
```json
{
  "username": "rahul_sharma",
  "email": "rahul.sharma@email.com",
  "password": "SecurePass@123",
  "password_confirm": "SecurePass@123",
  "first_name": "Rahul",
  "last_name": "Sharma",
  "phone_number": "+919876543210",
  "role": "CUSTOMER"
}
```

### In Postman:
1. Create a new request (or use the imported collection)
2. Set method to **POST**
3. URL: `http://127.0.0.1:8000/api/users/register/`
4. Go to **Body** tab → **raw** → **JSON**
5. Paste the JSON above
6. Click **Send**

**Pro Tip:** If you imported the collection, just find "Register Customer" request and hit Send!

**What you'll get back:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "username": "rahul_sharma",
      "email": "rahul.sharma@email.com",
      "full_name": "Rahul Sharma",
      "role": "CUSTOMER"
    },
    "tokens": {
      "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
      "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
  }
}
```

**Important:** Copy that `access` token! You'll need it for almost everything else. Store it somewhere - a text file, Postman environment variable, whatever works for you.

> **Pro tip:** In Postman, you can save the token as an environment variable. Makes life much easier.

### Common Issues:
- **"This username is already taken"** - Pick a different username
- **"Passwords do not match"** - Make sure password and password_confirm are identical
- **"Password too weak"** - Needs at least 8 characters

---

## Step 2: Login 

If you already have an account or want to get fresh tokens, you can login instead.

**Endpoint:** `POST /api/users/login/`

**What you need:**
```json
{
  "username": "rahul_sharma",
  "password": "SecurePass@123"
}
```

### In Postman:
Same as before - POST request with JSON body.

**Steps:**
1. Method: **POST**
2. URL: `http://127.0.0.1:8000/api/users/login/`
3. Body → raw → JSON
4. Paste the JSON above
5. Send

You'll get back the response - user info and tokens.

---

## Step 3: Check Your Profile

Let's make sure authentication is working properly. This is also your first authenticated request.

**Endpoint:** `GET /api/users/profile/`

**Important:** Now you need to include your access token in the headers!

### In Postman:
1. Create new request, method: **GET**
2. URL: `http://127.0.0.1:8000/api/users/profile/`
3. Go to **Authorization** tab
4. Type: Select **Bearer Token**
5. Token: Paste your access token here (or use `{{access_token}}` if using environment)
6. Send

**Alternative (Manual Headers):**
- Go to **Headers** tab
- Add: Key = `Authorization`, Value = `Bearer YOUR_ACCESS_TOKEN`
- Don't forget the word "Bearer" before your token (with a space)

**Pro Tip:** If you're using the imported collection, the token is automatically set from the environment variable!

**Response:**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "id": 1,
    "username": "rahul_sharma",
    "email": "rahul.sharma@email.com",
    "first_name": "Rahul",
    "last_name": "Sharma",
    "full_name": "Rahul Sharma",
    "phone_number": "+919876543210",
    "role": "CUSTOMER"
  }
}
```

If this works, your auth is set up correctly!

---

## Step 4: Add Funds to Your Wallet

Before you can buy anything, you need money in your wallet. This simulates adding funds (in a real app, this would integrate with Stripe, PayPal, etc.).

**Endpoint:** `POST /api/wallet/add-funds/`

**Auth Required:** Yes (use your access token)

**Request:**
```json
{
  "amount": 5000.00,
  "description": "Adding initial funds"
}
```

### In Postman:
1. Method: **POST**
2. URL: `http://127.0.0.1:8000/api/wallet/add-funds/`
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. **Body** tab: raw → JSON → Paste the JSON above
5. Send

**Response:**
```json
{
  "success": true,
  "message": "Funds added successfully",
  "data": {
    "transaction": {
      "id": 1,
      "transaction_type": "CREDIT",
      "amount": "5000.00",
      "balance_after_transaction": "5000.00",
      "description": "Adding initial funds",
      "timestamp": "2025-11-03 14:30:00"
    },
    "wallet": {
      "id": 1,
      "balance": "5000.00"
    }
  }
}
```

Nice! You now have ₹5000 to spend.

---

## Step 5: Browse Available Products

Let's see what we can buy.

**Endpoint:** `GET /api/products/`

**Auth Required:** Yes

### In Postman:
1. Method: **GET**
2. URL: `http://127.0.0.1:8000/api/products/`
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. Send

**Response:**
```json
{
  "count": 15,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Laptop",
      "price": "999.99",
      "stock_quantity": 50,
      "is_in_stock": true,
      "created_at": "2025-11-03 10:00:00"
    },
    {
      "id": 2,
      "name": "Wireless Mouse",
      "price": "29.99",
      "stock_quantity": 200,
      "is_in_stock": true,
      "created_at": "2025-11-03 10:00:00"
    }
    // ... more products
  ]
}
```

The response is paginated (10 items per page by default). You can navigate using the `next` and `previous` URLs.

**Query Parameters you can use:**
- `?search=laptop` - Search products
- `?page=2` - Get second page

Example: `http://127.0.0.1:8000/api/products/?search=laptop`

---

## Step 6: Get Product Details

Want more info about a specific product? Use its ID.

**Endpoint:** `GET /api/products/{id}/`

Example for product ID 1:

### In Postman:
1. Method: **GET**
2. URL: `http://127.0.0.1:8000/api/products/1/`  (replace `1` with any product ID)
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. Send

**Response:**
```json
{
  "success": true,
  "message": "Product retrieved successfully",
  "data": {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop with 16GB RAM",
    "price": "999.99",
    "stock_quantity": 50,
    "is_in_stock": true,
    "is_low_stock": false,
    "created_at": "2025-11-03 10:00:00",
    "updated_at": "2025-11-03 10:00:00"
  }
}
```

---

## Step 7: Make a Purchase! 🎉

This is the main feature - buying a product. The system will:
1. Check if you have enough money
2. Check if there's enough stock
3. Deduct money from your wallet
4. Reduce product stock
5. Create an order record
6. Create a transaction record

All of this happens atomically (either everything succeeds or nothing happens).

**Endpoint:** `POST /api/orders/purchase/`

**Auth Required:** Yes

**Request:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

This tries to buy 2 laptops.

### In Postman:
1. Method: **POST**
2. URL: `http://127.0.0.1:8000/api/orders/purchase/`
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. **Body** tab: raw → JSON → Paste the JSON above
5. Send

**Success Response:**
```json
{
  "success": true,
  "message": "Purchase completed successfully",
  "data": {
    "order": {
      "id": 1,
      "customer": "rahul_sharma",
      "product": {
        "id": 1,
        "name": "Laptop",
        "price": "999.99"
      },
      "quantity": 2,
      "unit_price": "999.99",
      "total_price": "1999.98",
      "status": "COMPLETED",
      "created_at": "2025-11-03 14:45:00"
    },
    "transaction": {
      "transaction_type": "DEBIT",
      "amount": "1999.98",
      "balance_after_transaction": "3000.02",
      "description": "Purchase: Laptop x2"
    },
    "total_amount": "1999.98",
    "remaining_balance": "3000.02"
  }
}
```

Congrats! You just bought 2 laptops. Your wallet now has ₹3000.02 left.

### Possible Errors:

**Insufficient Balance:**
```json
{
  "success": false,
  "message": "Insufficient wallet balance",
  "errors": {
    "error": "Insufficient wallet balance",
    "required_balance": 1999.98,
    "available_balance": 100.00,
    "shortfall": 1899.98
  }
}
```
Solution: Add more funds to your wallet.

**Out of Stock:**
```json
{
  "success": false,
  "message": "Insufficient stock",
  "errors": {
    "error": "Insufficient stock",
    "product": "Laptop",
    "requested_quantity": 100,
    "available_quantity": 50
  }
}
```
Solution: Reduce the quantity or choose a different product.

---

## Step 8: Check Your Wallet Balance

Let's confirm how much money you have left.

**Endpoint:** `GET /api/wallet/balance/`

### In Postman:
1. Method: **GET**
2. URL: `http://127.0.0.1:8000/api/wallet/balance/`
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. Send

**Response:**
```json
{
  "success": true,
  "message": "Balance retrieved successfully",
  "data": {
    "balance": "3000.02"
  }
}
```

---

## Step 9: View Your Transaction History

Want to see all your wallet activity? Credits, debits, purchases - it's all here.

**Endpoint:** `GET /api/wallet/transactions/`

### In Postman:
1. Method: **GET**
2. URL: `http://127.0.0.1:8000/api/wallet/transactions/`
3. **Authorization** tab: Bearer Token → `{{access_token}}`
4. Send

**Response:**
```json
{
  "success": true,
  "message": "Transaction history retrieved successfully",
  "data": {
    "count": 2,
    "results": [
      {
        "id": 2,
        "transaction_type": "DEBIT",
        "amount": "1999.98",
        "balance_after_transaction": "3000.02",
        "description": "Purchase: Laptop x2",
        "timestamp": "2025-11-03 14:45:00"
      },
      {
        "id": 1,
        "transaction_type": "CREDIT",
        "amount": "5000.00",
        "balance_after_transaction": "5000.00",
        "description": "Adding initial funds",
        "timestamp": "2025-11-03 14:30:00"
      }
    ]
  }
}
```

Transactions are sorted by timestamp, newest first.

---

## Step 10: Import Products from Excel

This one's different - it's a management command, not an API endpoint. But it's super useful for bulk operations.

**What it does:** Reads an Excel file and creates/updates products in bulk.

### Excel File Format

Your Excel file should have these columns:
- `name` (required)
- `price` (required)
- `stock_quantity` (required)
- `description` (optional)

Example:

| name | description | price | stock_quantity |
|------|-------------|-------|----------------|
| Laptop | High-performance laptop | 999.99 | 50 |
| Mouse | Wireless mouse | 29.99 | 200 |
| Keyboard | Mechanical keyboard | 89.99 | 100 |

### Running the Import

Open a **new terminal** (keep the server running in the original one), activate your venv if needed, and run:

```bash
python manage.py import_products products.xlsx
```

Or with a custom file:
```bash
python manage.py import_products path/to/your/file.xlsx
```

**What you'll see:**
```
=== Product Import Started ===
File: products.xlsx

[OK] File validation passed
[OK] Loaded 15 products from Excel

Importing products...

==================================================

=== Import Summary ===

Total rows processed: 15
[+] Created: 12
[~] Updated: 3
[-] Failed: 0

==================================================

[SUCCESS] Import completed successfully!
```

**How duplicates are handled:** If a product with the same name exists, it updates the price, description, and stock. Otherwise, it creates a new product.

### If you get errors:

Check the error output - it tells you exactly which row failed and why. Common issues:
- Empty product name
- Negative or zero price
- Negative stock quantity
- Invalid number format

Fix the Excel file and run the command again.

---

## Alternative: Using Swagger UI

If you prefer browser-based testing, you can use the built-in Swagger UI:

1. Open http://127.0.0.1:8000/ in your browser
2. Click the **Authorize** button (🔒 top right)
3. Enter: `Bearer YOUR_ACCESS_TOKEN` 
4. Now you can test any endpoint directly from the browser

**However, Postman is recommended** because:
- Better request history
- Can save collections
- Environment variables work seamlessly
- Easier to organize and share tests

---

## Testing as Admin (Bonus)

Want to test admin features? You need to create an admin user.

### Create Admin:
When registering, set `"role": "ADMIN"` instead of `"CUSTOMER"`.

Or use the superuser you created during setup and login through the API.

### What admins can do:
- Create products: `POST /api/products/`
- Update products: `PUT /api/products/{id}/`
- Delete products: `DELETE /api/products/{id}/`

Customers can only view products and make purchases.

---

## Quick Reference

Here's a cheat sheet of all the endpoints:

**Auth (Public):**
- `POST /api/users/register/` - Sign up
- `POST /api/users/login/` - Login
- `POST /api/users/token/refresh/` - Refresh token

**User (Authenticated):**
- `GET /api/users/profile/` - Get profile
- `PUT /api/users/profile/` - Update profile

**Products (Authenticated):**
- `GET /api/products/` - List products
- `GET /api/products/{id}/` - Product details
- `POST /api/products/` - Create (admin only)
- `PUT /api/products/{id}/` - Update (admin only)
- `DELETE /api/products/{id}/` - Delete (admin only)

**Wallet (Customer):**
- `GET /api/wallet/balance/` - Check balance
- `POST /api/wallet/add-funds/` - Add money
- `GET /api/wallet/transactions/` - Transaction history

**Orders (Customer):**
- `POST /api/orders/purchase/` - Buy product

**Management Commands:**
- `python manage.py import_products FILE.xlsx` - Bulk import

---

## Tips & Tricks for Postman

1. **Use Environment Variables:** 
   - The imported environment has `{{base_url}}` and `{{access_token}}`
   - Tokens are saved automatically after register/login
   - You don't need to copy-paste tokens manually!

2. **Token Expired?** 
   - Just run the "Login" request again
   - Access tokens expire after 60 minutes by default
   - New token is auto-saved to environment

3. **Test in Order:**
   - Register → Add Funds → List Products → Purchase → View Transactions
   - Follow this flow for smooth testing

4. **Check Response Times:**
   - Postman shows response time in bottom right
   - Most APIs should respond in <100ms locally

5. **Save Your Work:**
   - Create a new collection for your custom tests
   - Use folders to organize by feature (Auth, Products, Wallet, etc.)

6. **Reset Database if Needed:**
   ```bash
   rm db.sqlite3
   python manage.py migrate
   python manage.py import_products products.xlsx
   ```
   Then re-register your test user in Postman

7. **Check Server Logs:**
   - If something fails, check your terminal where the server is running
   - Django logs all requests and errors there

---

That's it! You now know how to test the entire API using Postman. 

**Remember:**
- Use the imported collection for fastest testing
- Tokens are handled automatically
- Check the server logs if something doesn't work
- The error messages are detailed - read them carefully

**Best Way to Learn:**
- Follow the collection in order
- Try intentional errors (insufficient balance, out of stock, etc.)
- Experiment with different quantities and products




