# Kisan Vaahan - Refactored Frontend Files

This document contains all the refactored frontend files that need to be updated.

## market.html - Complete Refactored Version

Save this as `app/templates/market.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Kisan Vaahan | Marketplace</title>
  <script src="https://cdn.tailwindcss.com"></script>

  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            'kisan-green': '#22C55E',
            'kisan-dark':  '#047857',
            'kisan-light': '#D1FAE5',
          },
          boxShadow: { 'card-lift': '0 4px 10px rgba(0,0,0,0.08)' }
        }
      }
    }
  </script>

  <style>
    .fade-in { animation: fadeIn .15s ease both; }
    @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
  </style>
</head>

<body class="bg-gray-50 font-sans text-gray-800" style="zoom: 70%; overflow-x: hidden;">

<!-- HEADER -->
<header class="bg-white shadow-md sticky top-3 z-30">
  <div class="flex justify-between items-center px-6 md:px-10 py-3 max-w-8xl mx-auto">
    <div class="flex items-center space-x-4 cursor-pointer">
      <img src="/static/logo.png" alt="Kisan Vaahan Logo" class="h-20 w-20 object-contain transform hover:rotate-12 transition-transform duration-400" />
      <h1 class="text-3xl md:text-4xl font-extrabold text-kisan-dark tracking-tight leading-none transform hover:scale-105 transition-transform duration-300">
        KISAN VAAHAN
      </h1>
    </div>

    <nav class="hidden lg:flex items-center space-x-6">
      <a href="{{ url_for('landing_page') }}" class="text-kisan-dark hover:text-kisan-green text-lg font-semibold">Home</a>
      <a href="{{ url_for('about') }}" class="text-kisan-dark hover:text-kisan-green text-lg font-semibold">About</a>
      <a href="{{ url_for('contact') }}" class="text-kisan-dark hover:text-kisan-green text-lg font-semibold">Contact</a>

      <!-- View Cart with badge -->
      <a href="{{ url_for('buyer_cart') }}"
         class="ml-4 px-4 py-2 border border-kisan-green rounded-lg text-base font-semibold hover:bg-kisan-dark hover:text-white transition text-center flex items-center gap-2">
        🛒 View Cart
        <span id="cart-badge" class="inline-block px-2 py-1 text-sm bg-kisan-green text-white rounded-full">0</span>
      </a>
    </nav>
  </div>
</header>

<!-- PAGE LAYOUT -->
<div class="flex flex-1 min-h-[calc(100vh-8rem)] max-w-8xl mx-auto px-4 md:px-6 py-8 gap-8">

  <!-- SIDEBAR -->
  <aside class="w-64 bg-white shadow-lg border border-gray-200 p-6 hidden md:flex flex-col justify-between rounded-xl">
    <div>
      <div class="flex items-center space-x-3 mb-4">
        <div class="w-12 h-12 rounded-full bg-gray-200 flex items-center justify-center text-gray-600 text-2xl">👤</div>
        <div>
          <p class="font-semibold text-lg text-gray-800">Kisan Vaahan</p>
          <p class="text-sm text-gray-500">Buyer Portal</p>
        </div>
      </div>
      <nav>
        <ul class="space-y-2">
          <li>
            <a href="{{ url_for('buyer_market') }}"
               class="flex items-center p-3 rounded-lg text-kisan-dark bg-kisan-light font-medium hover:bg-kisan-green hover:text-white transition">
              <span class="mr-3 text-xl">🛒</span> Marketplace
            </a>
          </li>
          <li>
            <a href="{{ url_for('buyer_orders') }}"
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-kisan-dark transition">
              <span class="mr-3 text-xl">📦</span> My Orders
            </a>
          </li>
          <li>
            <a href="{{ url_for('buyer_profile') }}"
               class="flex items-center p-3 rounded-lg text-gray-700 hover:bg-gray-100 hover:text-kisan-dark transition">
              <span class="mr-3 text-xl">👤</span> Profile
            </a>
          </li>
        </ul>
      </nav>
    </div>

    <!-- LOGOUT BUTTON -->
    <div class="mt-6">
      <button onclick="confirmLogout()"
              class="w-full bg-red-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-red-600 transition">
        Log Out
      </button>
    </div>
  </aside>

  <!-- MAIN CONTENT -->
  <main class="flex-1">
    <section class="mb-6">
      <div class="flex flex-col md:flex-row md:items-end md:justify-between gap-6 mb-6">
        <div>
          <h2 class="text-4xl md:text-6xl font-extrabold text-kisan-dark">Marketplace</h2>
          <p class="text-lg md:text-2xl text-gray-600 mt-1">Browse products from farmers across India</p>
        </div>

        <!-- Filters -->
        <div class="w-full md:w-auto flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
          <input id="searchBar" type="text" placeholder="Search products..."
                 class="border border-gray-300 rounded-lg px-4 py-2 w-full sm:w-64 focus:ring-2 focus:ring-kisan-green outline-none">
          <select id="categoryFilter"
                  class="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-kisan-green outline-none">
            <option value="all">All Categories</option>
            <option value="Vegetables">Vegetables</option>
            <option value="Fruits">Fruits</option>
            <option value="Grains">Grains</option>
            <option value="Pulses">Pulses</option>
            <option value="Millets">Millets</option>
          </select>
          <select id="sortFilter"
                  class="border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-kisan-green outline-none">
            <option value="default">Sort by</option>
            <option value="low">Price: Low to High</option>
            <option value="high">Price: High to Low</option>
          </select>
          <a href="{{ url_for('buyer_cart') }}"
             class="px-4 py-2 border border-kisan-green rounded-lg text-base font-semibold hover:bg-kisan-dark hover:text-white transition text-center">
            Quick Cart
          </a>
        </div>
      </div>
    </section>

    <!-- PRODUCT GRID -->
    <section>
      <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8"></div>
    </section>
  </main>
</div>

<!-- FOOTER -->
<footer class="bg-kisan-dark text-white py-8 text-center mt-8">
  <p class="text-lg">© 2025 Kisan Vaahan. All Rights Reserved.</p>
</footer>

<!-- LOGOUT CONFIRMATION MODAL -->
<div id="logoutModal" class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
  <div class="bg-white w-full max-w-sm rounded-2xl p-6 shadow-lg fade-in text-center">
    <h3 class="text-xl font-bold text-kisan-dark mb-3">Confirm Logout</h3>
    <p class="text-gray-700 mb-6">Are you sure you want to log out?</p>
    <div class="flex justify-center gap-4">
      <button onclick="closeLogout()" class="px-4 py-2 rounded-lg border border-gray-300 hover:bg-gray-100">No</button>
      <button onclick="proceedLogout()" class="px-4 py-2 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700">Yes, Log Out</button>
    </div>
  </div>
</div>

<!-- JS LOGIC -->
<script>
  const grid = document.getElementById("productGrid");
  const searchBar = document.getElementById("searchBar");
  const categoryFilter = document.getElementById("categoryFilter");
  const sortFilter = document.getElementById("sortFilter");
  const logoutModal = document.getElementById("logoutModal");

  function confirmLogout() { logoutModal.classList.remove("hidden"); }
  function closeLogout() { logoutModal.classList.add("hidden"); }
  function proceedLogout() {
    logoutModal.classList.add("hidden");
    localStorage.removeItem("access_token");
    window.location.href = '{{ url_for("landing_page") }}';
  }

  // Fetch products from backend
  let allProducts = [];

  async function fetchProducts() {
    try {
      const res = await fetch("/products/?page=1&limit=100");
      if (!res.ok) throw new Error("Failed to fetch products");
      const json = await res.json();
      allProducts = json.data || [];
      return allProducts;
    } catch (err) {
      console.error("fetchProducts error", err);
      showToast("Failed to load products");
      return [];
    }
  }

  // Utility: show toast
  function showToast(msg, timeout = 1200) {
    const t = document.createElement('div');
    t.innerText = msg;
    t.style = "position:fixed;right:20px;top:20px;background:#16a34a;color:white;padding:10px 14px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,.12);z-index:9999;font-weight:600";
    document.body.appendChild(t);
    setTimeout(() => t.remove(), timeout);
  }

  // Render product cards
  async function loadProducts() {
    const products = await fetchProducts();
    grid.innerHTML = "";
    
    if (products.length === 0) {
      grid.innerHTML = `<p class="col-span-full text-center text-gray-600 text-xl py-10">No products available</p>`;
      return;
    }

    products.forEach(p => {
      const card = document.createElement("div");
      card.className = "product-card border bg-white rounded-xl p-4 md:p-5 shadow-card-lift transition relative";
      card.dataset.productId = p.id;
      card.dataset.name = p.title || "";
      card.dataset.category = p.category?.name || "Other";
      card.dataset.price = p.price;

      const imageUrl = (p.images && p.images.length > 0) ? p.images[0] : (p.thumbnail || "https://via.placeholder.com/300");

      card.innerHTML = `
        <span class="success-msg hidden absolute inset-0 bg-kisan-green/90 text-white flex flex-col items-center justify-center rounded-xl text-xl font-bold z-20 transition duration-500" style="opacity:0;">✅ Added to Cart</span>
        <div class="relative h-52 md:h-64 rounded-lg overflow-hidden group">
          <img src="${imageUrl}" class="w-full h-full object-cover">
          <div class="absolute inset-0 bg-black/50 text-white opacity-0 group-hover:opacity-100 transition flex items-center justify-center text-center px-2 text-sm md:text-lg">${p.description || ''}</div>
        </div>
        <h3 class="mt-4 font-bold text-lg">${p.title}</h3>
        <p class="text-gray-600 text-sm">Farmer • India</p>
        <div class="flex justify-between mt-3 items-center">
          <span class="font-bold text-kisan-dark text-lg">₹${p.price}/Kg</span>
          <span class="bg-kisan-light px-3 py-1 text-xs font-bold rounded-full">${p.stock > 0 ? 'In Stock' : 'Out of Stock'}</span>
        </div>
        <div class="flex justify-between items-center mt-4">
          <div class="flex items-center border border-kisan-green rounded-lg px-3">
            <button onclick="changeQty(this, -1)" class="px-2">-</button>
            <span class="px-3 font-semibold qty">1</span>
            <button onclick="changeQty(this, 1)" class="px-2">+</button>
          </div>
          <button onclick="addToCart(this)" data-name="${p.title}" data-price="${p.price}" class="bg-kisan-green text-white px-4 py-2 rounded-lg hover:bg-kisan-dark" ${p.stock <= 0 ? 'disabled' : ''}>Add to Cart</button>
        </div>`;
      grid.appendChild(card);
    });
    updateUI();
  }

  function getCards() { return Array.from(grid.querySelectorAll(".product-card")); }

  function applyFilters() {
    const q = (searchBar?.value || "").trim().toLowerCase();
    const cat = (categoryFilter?.value || "all");
    getCards().forEach(card => {
      const name = (card.dataset.name || "").toLowerCase();
      const cardCat = card.dataset.category || "all";
      const matchSearch = q === "" || name.includes(q);
      const matchCategory = (cat === "all") || (cardCat === cat);
      card.style.display = (matchSearch && matchCategory) ? "block" : "none";
    });
  }

  function applySort() {
    const mode = sortFilter?.value || "default";
    if (mode === "default") return;
    const cards = getCards();
    cards.sort((a, b) => {
      const pa = parseFloat(a.dataset.price || "0");
      const pb = parseFloat(b.dataset.price || "0");
      return mode === "low" ? pa - pb : pb - pa;
    });
    cards.forEach(c => grid.appendChild(c));
  }

  function updateUI() { applyFilters(); applySort(); }

  function changeQty(btn, delta) {
    const qtySpan = btn.parentElement.querySelector('.qty');
    let qty = parseInt(qtySpan.innerText) || 1;
    qty += delta;
    if (qty < 1) qty = 1;
    qtySpan.innerText = qty;
  }

  searchBar?.addEventListener("input", updateUI);
  categoryFilter?.addEventListener("change", updateUI);
  sortFilter?.addEventListener("change", updateUI);

  loadProducts();

  // ====== Cart Backend Integration ======

  async function addToCartAPI(productId, qty = 1) {
    const token = localStorage.getItem("access_token");
    if (!token) {
      showToast("Please login to add items");
      setTimeout(() => window.location.href = "/buyer/login", 700);
      return { ok: false, msg: "not_logged_in" };
    }

    try {
      const res = await fetch("/carts/add-item", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + token
        },
        body: JSON.stringify({ product_id: productId, quantity: qty })
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Failed" }));
        console.warn("addToCartAPI failed", err);
        return { ok: false, msg: err.detail || "Failed to add" };
      }

      const body = await res.json();
      return { ok: true, body };
    } catch (e) {
      console.error("addToCartAPI error", e);
      return { ok: false, msg: "network_error" };
    }
  }

  async function addToCart(btn) {
    const card = btn.closest('.product-card');
    const productId = parseInt(card.dataset.productId || btn.dataset.productId, 10);
    if (!productId || isNaN(productId)) {
      showToast("Product ID missing");
      return;
    }
    const qty = parseInt(card.querySelector('.qty').innerText) || 1;

    btn.disabled = true;
    btn.style.opacity = 0.6;

    const r = await addToCartAPI(productId, qty);
    if (!r.ok) {
      showToast(r.msg || "Add failed");
      btn.disabled = false;
      btn.style.opacity = 1;
      return;
    }

    card.querySelector('.qty').innerText = 1;
    const msg = card.querySelector('.success-msg');
    if (msg) {
      msg.classList.remove('hidden');
      msg.style.opacity = "1";
      setTimeout(() => {
        msg.style.opacity = "0";
        setTimeout(() => msg.classList.add('hidden'), 500);
      }, 1200);
    }
    showToast("Added to cart");

    await refreshCartBadge();

    btn.disabled = false;
    btn.style.opacity = 1;
  }

  async function refreshCartBadge() {
    const badge = document.getElementById("cart-badge");
    if (!badge) return;
    const token = localStorage.getItem("access_token");
    if (!token) {
      badge.innerText = "0";
      return;
    }

    try {
      const res = await fetch("/carts/me", {
        headers: { "Authorization": "Bearer " + token }
      });
      if (!res.ok) {
        badge.innerText = "0";
        return;
      }
      const json = await res.json();
      const items = (json.data && json.data.cart_items) ? json.data.cart_items : [];
      const totalQty = items.reduce((s, i) => s + (i.quantity || 0), 0);
      badge.innerText = totalQty;
    } catch (err) {
      console.error("refreshCartBadge error", err);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    refreshCartBadge();
  });
</script>

</body>
</html>
```

Copy the complete HTML files from this document to replace your existing templates.
