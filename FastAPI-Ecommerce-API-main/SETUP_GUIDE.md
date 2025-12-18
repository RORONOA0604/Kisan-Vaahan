# Kisan Vaahan - Supabase Setup Guide

## 🚀 Quick Start

This guide will help you set up the Kisan Vaahan e-commerce platform with Supabase database.

## Prerequisites

- Python 3.8 or higher
- Supabase account (free tier works fine)
- Git (optional)

## Step 1: Supabase Database Setup

### 1.1 Execute SQL Schema

1. Go to your Supabase project dashboard: https://supabase.com/dashboard
2. Navigate to **SQL Editor** (left sidebar)
3. Open the file `supabase_schema.sql` from this project
4. Copy the entire SQL content
5. Paste it into the Supabase SQL Editor
6. Click **RUN** to execute the schema

This will create:
- All necessary tables (users, products, categories, carts, orders, etc.)
- Indexes for performance
- Default categories (Vegetables, Fruits, Grains, etc.)
- Default admin user (username: `admin`, password: `admin123`)
- Sample products

### 1.2 Get Your Database Password

1. In Supabase Dashboard, go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Click on **URI** tab
4. Copy the password from the connection string (it's between `postgres:` and `@db.`)
5. Save this password - you'll need it for the `.env` file

## Step 2: Environment Configuration

### 2.1 Create .env File

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` and update these values:
   ```env
   # Already filled in for you:
   SUPABASE_URL=https://anubppnlmkrelguhmukz.supabase.co
   SUPABASE_KEY=sb_publishable_TwqRbRJxUdTKZKRh3rKiew_46XLSGSc
   
   # UPDATE THIS with your Supabase database password:
   DB_PASSWORD=your_actual_password_here
   
   # RECOMMENDED: Generate a new secret key:
   SECRET_KEY=your_secret_key_here
   ```

3. To generate a secure SECRET_KEY (optional but recommended):
   ```bash
   # On Windows PowerShell:
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | ForEach-Object {[char]$_})
   
   # Or use any random 32+ character string
   ```

## Step 3: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 4: Run the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload

# Or use the run script:
python run.py
```

The application will be available at:
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## Step 5: Test the Setup

### 5.1 Test Admin Login

1. Navigate to: http://localhost:8000/Admin/Login
2. Login with:
   - **Username**: `admin`
   - **Password**: `admin123`
3. **IMPORTANT**: Change the admin password after first login!

### 5.2 Test Farmer Registration

1. Navigate to: http://localhost:8000/farmer/register
2. Create a farmer account
3. Login and try uploading a product
4. The product should be in "pending" status

### 5.3 Test Product Approval

1. Login as admin
2. Go to: http://localhost:8000/Admin/farmer-uploads
3. You should see pending products from farmers
4. Approve or reject products

### 5.4 Test Marketplace

1. Navigate to: http://localhost:8000/buyer/market
2. You should see only approved products
3. Both buyers and farmers can access this page

## 📋 Default Credentials

| User Type | Username | Password | Notes |
|-----------|----------|----------|-------|
| Admin | admin | admin123 | **Change this immediately!** |

## 🔑 Key Features Implemented

### ✅ Product Approval Workflow
- Farmers upload products → Status: **Pending**
- Admin reviews → Approve or Reject
- Only **Approved** products appear in marketplace

### ✅ Unified Marketplace
- Same marketplace (`/buyer/market`) for both buyers and farmers
- Both can browse and purchase products

### ✅ Admin CRUD Operations
- **Products**: Create, Read, Update, Delete, Approve, Reject
- **Orders**: View all, Update status, Delete

### ✅ API Endpoints

#### Product Endpoints
- `GET /products/` - Get all approved products (public)
- `GET /products/pending` - Get pending products (admin only)
- `POST /products/` - Create product (farmers create pending, admins create approved)
- `PUT /products/{id}/approve` - Approve product (admin only)
- `PUT /products/{id}/reject` - Reject product (admin only)
- `PUT /products/{id}` - Update product (admin only)
- `DELETE /products/{id}` - Delete product (admin only)

#### Order Endpoints
- `GET /orders/` - Get all orders (admin only)
- `GET /orders/me` - Get my orders (authenticated users)
- `POST /orders/` - Create order from cart
- `PUT /orders/{id}` - Update order status (admin only)
- `DELETE /orders/{id}` - Delete order (admin only)

## 🐛 Troubleshooting

### Database Connection Error
- Verify your `DB_PASSWORD` in `.env` is correct
- Check that you executed the SQL schema in Supabase
- Ensure your IP is not blocked by Supabase (check Settings → Database → Connection pooling)

### Products Not Showing
- Check that products have `approval_status='approved'`
- Login as admin and check `/products/pending` endpoint

### Admin Can't Login
- Verify the SQL schema was executed successfully
- Check the `users` table in Supabase has the admin user
- Password is `admin123` (hashed in database)

## 📚 Next Steps

1. **Change Admin Password**: Update the admin password in Supabase or via API
2. **Customize Products**: Add your own products via admin panel
3. **Configure Email**: Set up email notifications (optional)
4. **Deploy**: Deploy to production (Vercel, Railway, etc.)

## 🔒 Security Notes

- The default admin password (`admin123`) is **NOT SECURE**
- Change it immediately after first login
- Generate a strong `SECRET_KEY` for JWT tokens
- Never commit `.env` file to version control
- Use environment variables in production

## 📞 Support

If you encounter any issues:
1. Check the console/terminal for error messages
2. Verify all environment variables are set correctly
3. Ensure Supabase database is accessible
4. Check API documentation at `/docs`

---

**Happy Coding! 🎉**
