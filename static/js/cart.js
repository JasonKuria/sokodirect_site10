/* ============================================================
   Soko Direct — cart.js  (updated)
   Cookie-based shopping cart aligned with products/models.py

   Product model fields used:
     id, title, price, unit, quantity_available, imageURL,
     county, owner (Profile)

   Cart cookie structure:
   {
     "<product-uuid>": {
       quantity:  1,
       title:     "Roma Tomatoes",
       price:     "150",
       unit:       "kg",
       imageURL:  "/media/products/tomatoes.jpg",
       county:    "Nyeri"
     },
     ...
   }
   ============================================================ */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────
     COOKIE HELPERS
  ────────────────────────────────────────────── */
  function getCookie(name) {
    var arr = document.cookie.split(';');
    for (var i = 0; i < arr.length; i++) {
      var pair = arr[i].trim().split('=');
      if (pair[0] === name) {
        try { return JSON.parse(decodeURIComponent(pair[1])); }
        catch (e) { return null; }
      }
    }
    return null;
  }

  function setCookie(name, value) {
    document.cookie = name + '=' + encodeURIComponent(JSON.stringify(value)) + ';domain=;path=/';
  }

  /* ──────────────────────────────────────────────
     CART STATE
  ────────────────────────────────────────────── */
  function getCart() {
    var cart = getCookie('cart');
    if (!cart || typeof cart !== 'object') cart = {};
    return cart;
  }

  function saveCart(cart) {
    setCookie('cart', cart);
    updateCartDisplay();
  }

  /* ──────────────────────────────────────────────
     CART OPERATIONS
  ────────────────────────────────────────────── */

  /**
   * Add a product to the cart.
   * @param {string} productId   — Product.id (UUID)
   * @param {number} quantity    — how many units (default 1)
   * @param {object} meta        — { title, price, unit, imageURL, county }
   *                               pulled from data-* attributes on the button
   */
  function addToCart(productId, quantity, meta) {
    quantity = parseInt(quantity, 10) || 1;
    meta     = meta || {};
    var cart = getCart();

    if (cart[productId]) {
      // Respect quantity_available cap if present
      var cap = parseInt(meta.maxQty, 10);
      var newQty = cart[productId].quantity + quantity;
      if (cap && newQty > cap) {
        showCartToast('Only ' + cap + ' ' + (meta.unit || 'units') + ' available ⚠');
        return cart;
      }
      cart[productId].quantity = newQty;
    } else {
      cart[productId] = {
        quantity:  quantity,
        title:     meta.title    || 'Produce Item',
        price:     meta.price    || '0',
        unit:      meta.unit     || '',
        imageURL:  meta.imageURL || '',
        county:    meta.county   || '',
      };
    }

    saveCart(cart);
    showCartToast('\u2705 ' + (meta.title || 'Item') + ' added to cart');
    return cart;
  }

  function removeFromCart(productId) {
    var cart = getCart();
    var title = cart[productId] ? cart[productId].title : 'Item';
    if (cart[productId]) {
      delete cart[productId];
      saveCart(cart);
      showCartToast(title + ' removed from cart');
    }
    refreshCartPage();
    return cart;
  }

  function updateQuantity(productId, quantity) {
    quantity = parseInt(quantity, 10);
    if (isNaN(quantity) || quantity <= 0) return removeFromCart(productId);

    var cart = getCart();
    if (!cart[productId]) return cart;

    // Respect quantity_available cap stored in cookie
    var cap = parseInt(cart[productId].maxQty, 10);
    if (cap && quantity > cap) {
      showCartToast('Max available: ' + cap + ' ' + (cart[productId].unit || 'units'));
      quantity = cap;
    }

    cart[productId].quantity = quantity;
    saveCart(cart);
    refreshCartPage();
    return cart;
  }

  function clearCart() {
    saveCart({});
    showCartToast('Cart cleared');
    refreshCartPage();
  }

  /* ──────────────────────────────────────────────
     CART TOTALS
  ────────────────────────────────────────────── */
  function getCartItemCount() {
    var cart  = getCart();
    var total = 0;
    Object.keys(cart).forEach(function (id) {
      total += parseInt(cart[id].quantity, 10) || 0;
    });
    return total;
  }

  function getCartValue() {
    // Returns grand total in KES as a float
    var cart  = getCart();
    var total = 0;
    Object.keys(cart).forEach(function (id) {
      var item  = cart[id];
      var price = parseFloat(String(item.price).replace(/[^0-9.]/g, '')) || 0;
      total    += price * (parseInt(item.quantity, 10) || 0);
    });
    return total;
  }

  function getProductCount(productId) {
    var cart = getCart();
    return cart[productId] ? parseInt(cart[productId].quantity, 10) : 0;
  }

  /* ──────────────────────────────────────────────
     UI — NAVBAR BADGE + ANY [data-cart-count]
  ────────────────────────────────────────────── */
  function updateCartDisplay() {
    var count = getCartItemCount();

    // #cart-total in navbar
    var badge = document.getElementById('cart-total');
    if (badge) {
      badge.textContent      = count;
      badge.style.transition = 'transform 0.15s ease';
      badge.style.transform  = 'scale(1.4)';
      setTimeout(function () { badge.style.transform = 'scale(1)'; }, 160);
    }

    // Any other count elements
    document.querySelectorAll('[data-cart-count]').forEach(function (el) {
      el.textContent = count;
    });

    // Cart value display (e.g. in a mini-cart dropdown)
    var valueEl = document.getElementById('cart-value');
    if (valueEl) {
      valueEl.textContent = 'KES ' + getCartValue().toLocaleString();
    }
  }

  /* ──────────────────────────────────────────────
     UI — TOAST NOTIFICATION
  ────────────────────────────────────────────── */
  function showCartToast(message) {
    var existing = document.getElementById('soko-cart-toast');
    if (existing) existing.remove();

    var toast = document.createElement('div');
    toast.id  = 'soko-cart-toast';
    toast.textContent = message;

    Object.assign(toast.style, {
      position:     'fixed',
      bottom:       '7rem',
      right:        '2.4rem',
      background:   '#113821',
      color:        '#fff',
      padding:      '1.1rem 2rem',
      borderRadius: '8px',
      fontSize:     '1.4rem',
      fontWeight:   '600',
      boxShadow:    '0 4px 20px rgba(0,0,0,0.18)',
      zIndex:       '9999',
      borderLeft:   '4px solid #f1c40f',
      opacity:      '0',
      transform:    'translateY(10px)',
      transition:   'opacity 0.25s ease, transform 0.25s ease',
      fontFamily:   "'Inter', sans-serif",
      maxWidth:     '32rem',
      pointerEvents:'none',
    });

    document.body.appendChild(toast);
    requestAnimationFrame(function () {
      toast.style.opacity   = '1';
      toast.style.transform = 'translateY(0)';
    });

    setTimeout(function () {
      toast.style.opacity   = '0';
      toast.style.transform = 'translateY(10px)';
      setTimeout(function () { if (toast.parentNode) toast.remove(); }, 280);
    }, 2600);
  }

  /* ──────────────────────────────────────────────
     BUTTON WIRING
     Data attributes on any element:

     Add to cart button:
       data-action="add"
       data-id="{{ product.id }}"
       data-title="{{ product.title }}"
       data-price="{{ product.price }}"
       data-unit="{{ product.unit }}"
       data-image="{{ product.imageURL }}"
       data-county="{{ product.county }}"
       data-max-qty="{{ product.quantity_available }}"
       data-qty="1"   (optional, defaults to 1)

     Other actions:
       data-action="remove"   + data-id="..."
       data-action="increase" + data-id="..."
       data-action="decrease" + data-id="..."
       data-action="clear"
  ────────────────────────────────────────────── */
  function initCartButtons() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-action]');
      if (!btn) return;

      var action    = btn.getAttribute('data-action');
      var productId = btn.getAttribute('data-id');

      if (action === 'add' && productId) {
        e.preventDefault();
        var qty  = parseInt(btn.getAttribute('data-qty') || '1', 10);
        var meta = {
          title:    btn.getAttribute('data-title')   || '',
          price:    btn.getAttribute('data-price')   || '0',
          unit:     btn.getAttribute('data-unit')    || '',
          imageURL: btn.getAttribute('data-image')   || '',
          county:   btn.getAttribute('data-county')  || '',
          maxQty:   btn.getAttribute('data-max-qty') || '',
        };
        addToCart(productId, qty, meta);
        flashAddButton(btn);
      }

      if (action === 'remove' && productId) {
        e.preventDefault();
        removeFromCart(productId);
      }

      if (action === 'increase' && productId) {
        e.preventDefault();
        var current = getProductCount(productId);
        updateQuantity(productId, current + 1);
      }

      if (action === 'decrease' && productId) {
        e.preventDefault();
        var current = getProductCount(productId);
        updateQuantity(productId, current - 1);
      }

      if (action === 'clear') {
        e.preventDefault();
        if (window.confirm('Clear your entire cart? This cannot be undone.')) {
          clearCart();
        }
      }
    });

    // Manual quantity input on cart page
    document.addEventListener('change', function (e) {
      if (e.target.matches('input[data-product-id]')) {
        var productId = e.target.getAttribute('data-product-id');
        updateQuantity(productId, e.target.value);
      }
    });
  }

  /* ──────────────────────────────────────────────
     ADD BUTTON FLASH FEEDBACK
     "Add to Cart" → "✓ Added" for 1.8s
  ────────────────────────────────────────────── */
  function flashAddButton(btn) {
    var original   = btn.innerHTML;
    var origBg     = btn.style.background;
    btn.innerHTML  = '✓ Added';
    btn.style.background = '#113821';
    btn.disabled   = true;

    setTimeout(function () {
      btn.innerHTML  = original;
      btn.style.background = origBg;
      btn.disabled   = false;
    }, 1800);
  }

  /* ──────────────────────────────────────────────
     CART PAGE — LIVE REFRESH
     If .cart-item-list exists on the page, updates
     quantities and totals without a page reload.

     Expected HTML structure per cart row:
     <tr class="cart-item"
         data-item-id="{{ product.id }}"
         data-price="{{ product.price }}">

       <td><img src="{{ product.imageURL }}"> {{ product.title }}</td>
       <td>{{ product.unit }}</td>
       <td>
         <button data-action="decrease" data-id="{{ product.id }}">−</button>
         <span data-qty-display="{{ product.id }}">1</span>
         <button data-action="increase" data-id="{{ product.id }}">+</button>
       </td>
       <td data-subtotal="{{ product.id }}">KES 150</td>
       <td><button data-action="remove" data-id="{{ product.id }}">Remove</button></td>
     </tr>
  ────────────────────────────────────────────── */
  function refreshCartPage() {
    var itemList = document.querySelector('.cart-item-list');
    if (!itemList) return;

    var cart       = getCart();
    var items      = document.querySelectorAll('.cart-item[data-item-id]');
    var grandTotal = 0;
    var visible    = 0;

    items.forEach(function (row) {
      var pid   = row.getAttribute('data-item-id');
      var price = parseFloat(String(row.getAttribute('data-price') || '0').replace(/[^0-9.]/g, '')) || 0;

      if (!cart[pid] || cart[pid].quantity <= 0) {
        // Slide row out
        row.style.transition = 'opacity 0.28s ease';
        row.style.opacity    = '0';
        setTimeout(function () { row.remove(); checkEmptyCart(); }, 300);
      } else {
        var qty      = parseInt(cart[pid].quantity, 10);
        var subtotal = price * qty;
        grandTotal  += subtotal;
        visible++;

        // Qty display
        var qtyEl = row.querySelector('[data-qty-display="' + pid + '"]');
        if (qtyEl) qtyEl.textContent = qty;

        // Per-row subtotal
        var subEl = row.querySelector('[data-subtotal="' + pid + '"]');
        if (subEl) subEl.textContent = 'KES ' + subtotal.toLocaleString();

        // Sync quantity input if present
        var qtyInput = row.querySelector('input[data-product-id="' + pid + '"]');
        if (qtyInput) qtyInput.value = qty;
      }
    });

    // Grand total
    var totalEl = document.querySelector('.cart-summary-total');
    if (totalEl) totalEl.textContent = 'KES ' + grandTotal.toLocaleString();

    // Item count summary
    var countEl = document.querySelector('.cart-summary-count');
    if (countEl) countEl.textContent = visible + ' item' + (visible !== 1 ? 's' : '');

    updateCartDisplay();
  }

  function checkEmptyCart() {
    var remaining = document.querySelectorAll('.cart-item[data-item-id]');
    var emptyMsg  = document.querySelector('.cart-empty-msg');
    var cartTable = document.querySelector('.cart-item-list');

    if (remaining.length === 0) {
      if (emptyMsg)  emptyMsg.style.display  = 'block';
      if (cartTable) cartTable.style.display = 'none';
    }
  }

  /* ──────────────────────────────────────────────
     PUBLIC API — window.SokoCart.*
     Use from Django templates or other scripts:

     SokoCart.add(productId, qty, { title, price, unit, imageURL, county })
     SokoCart.remove(productId)
     SokoCart.update(productId, qty)
     SokoCart.clear()
     SokoCart.getCart()          → full cart object
     SokoCart.getTotal()         → item count (int)
     SokoCart.getValue()         → grand total in KES (float)
     SokoCart.getCount(pid)      → qty of one product (int)
  ────────────────────────────────────────────── */
  window.SokoCart = {
    add:      addToCart,
    remove:   removeFromCart,
    update:   updateQuantity,
    clear:    clearCart,
    getCart:  getCart,
    getTotal: getCartItemCount,
    getValue: getCartValue,
    getCount: getProductCount,
    refresh:  refreshCartPage,
  };

  /* ──────────────────────────────────────────────
     INIT
  ────────────────────────────────────────────── */
  function init() {
    updateCartDisplay();
    initCartButtons();
    refreshCartPage();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();