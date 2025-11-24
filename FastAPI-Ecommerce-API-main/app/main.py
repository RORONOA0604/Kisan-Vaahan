from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routers import products, categories, carts, users, auth, accounts

description = """
Welcome to the E-commerce API! 🚀

This API provides a comprehensive set of functionalities for managing your e-commerce platform.

Key features include:

- **Crud**
	- Create, Read, Update, and Delete endpoints.
- **Search**
	- Find specific information with parameters and pagination.
- **Auth**
	- Verify user/system identity.
	- Secure with Access and Refresh tokens.
- **Permission**
	- Assign roles with specific permissions.
	- Different access levels for User/Admin.
- **Validation**
	- Ensure accurate and secure input data.


For any inquiries, please contact:

* Github: https://github.com/aliseyedi01
"""
templates = Jinja2Templates(directory="app/templates")


app = FastAPI(
    description=description,
    title="E-commerce API",
    version="1.0.0",
    contact={
        "name": "Ali Seyedi",
        "url": "https://github.com/aliseyedi01",
    },
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)

# Mount static files (images etc.). Place your logo at: app/static/logo.png
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Jinja2 templates directory
templates = Jinja2Templates(directory="app/templates")

# Template routes (function names used by url_for in templates)
@app.get("/", response_class=HTMLResponse, name="landing_page")
async def landing_page(request: Request):
    return templates.TemplateResponse("landingpage.html", {"request": request})

@app.get("/marketplace", response_class=HTMLResponse, name="marketplace")
async def marketplace(request: Request):
    return templates.TemplateResponse("marketplace.html", {"request": request})

@app.get("/privacy", response_class=HTMLResponse, name="privcay_policy")
async def marketplace(request: Request):
    return templates.TemplateResponse("privacyandpolicy.html", {"request": request})

@app.get("/terms", response_class=HTMLResponse, name="terms_and_conditions")
async def marketplace(request: Request):
    return templates.TemplateResponse("termsandconditionspage.html", {"request": request})

@app.get("/about", response_class=HTMLResponse, name="about")
async def about(request: Request):
    return templates.TemplateResponse("aboutpage.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse, name="contact")
async def contact(request: Request):
    return templates.TemplateResponse("contactpage.html", {"request": request})

@app.get("/farmer/login", response_class=HTMLResponse, name="farmer_login")
async def farmer_login(request: Request):
    return templates.TemplateResponse("farmerlogin.html", {"request": request})

@app.get("/farmer/register", response_class=HTMLResponse, name="farmer_register")
async def farmer_register(request: Request):
    return templates.TemplateResponse("farmerregister.html", {"request": request})

@app.get("/farmer/register/success", response_class=HTMLResponse, name="farmer_register_success")
async def farmer_register_success(request: Request):
    return templates.TemplateResponse("faregistsuccesspage.html", {"request": request})

@app.get("/farmer/dashboard", response_class=HTMLResponse, name="farmer_dashboard")
async def farmer_dashboard(request: Request):
    return templates.TemplateResponse("farmerdashboard.html", {"request": request})

@app.get("/farmer/add-product", response_class=HTMLResponse, name="farmer_add_product")
async def farmer_add_product(request: Request):
    return templates.TemplateResponse("addnewpage.html", {"request": request})
@app.get("/farmer/edit-product", response_class=HTMLResponse, name="farmer_edit_product")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("editproduct.html", {"request": request})

@app.get("/cart", response_class=HTMLResponse, name="cart")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/cart/order-success", response_class=HTMLResponse, name="order_success")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("ordersuccess.html", {"request": request})


@app.get("/buyer/login", response_class=HTMLResponse, name="buyer_login")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("buyerlogin.html", {"request": request})

@app.get("/buyer/Register", response_class=HTMLResponse, name="buyer_register")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("Registerpage.html", {"request": request})

@app.get("/buyer/market", response_class=HTMLResponse, name="buyer_market")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("market.html", {"request": request})

@app.get("/buyer/market/cart", response_class=HTMLResponse, name="buyer_cart")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("cart.html", {"request": request})

@app.get("/buyer/profile", response_class=HTMLResponse, name="buyer_profile")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@app.get("/buyer/profile/edit", response_class=HTMLResponse, name="buyer_edit_profile")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("editprofile.html", {"request": request})

@app.get("/buyer/Myorder", response_class=HTMLResponse, name="buyer_orders")
async def farmer_edit_product(request: Request):
    return templates.TemplateResponse("Myorder.html", {"request": request})

# Include your routers (after mounting static & templates)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(carts.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)