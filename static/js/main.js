/* ============================================================
   Soko Direct — main.js
   Page-specific interactions and UI enhancements
   Covers:
     1. Product search — live filter on listings page
     2. Product image gallery switcher
     3. Farmer profile card hover effects
     4. Dashboard stat counter animation
     5. Login form UX (show/hide password)
     6. Sticky navbar shadow on scroll
     7. Lazy loading images
     8. Product card quick-view tooltip
     9. Form select → styled tag display
    10. Mobile sidebar toggle (dashboard)
   ============================================================ */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────
     1. PRODUCT SEARCH — LIVE FILTER
     Filters .product-card elements on the
     products listing page as the user types,
     without a page reload. Falls back to
     Django's server-side search on submit.
  ────────────────────────────────────────────── */
  function initLiveSearch() {
    var searchInput = document.querySelector('input[name="search_query"]');
    var productGrid = document.querySelector('.products__grid, .produce-grid, #product-grid');

    if (!searchInput || !productGrid) return;

    var debounceTimer;

    searchInput.addEventListener('input', function () {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(function () {
        var query = searchInput.value.trim().toLowerCase();
        var cards = productGrid.querySelectorAll('.product__card, .produce-card, [data-product-name]');
        var visible = 0;

        cards.forEach(function (card) {
          var name = (
            card.getAttribute('data-product-name') ||
            (card.querySelector('[data-product-name]') || {}).textContent ||
            card.querySelector('h3, h4, .product__title, .produce-card__name') &&
            card.querySelector('h3, h4, .product__title, .produce-card__name').textContent ||
            ''
          ).toLowerCase();

          var matches = !query || name.includes(query);
          card.style.transition = 'opacity 0.2s ease';
          card.style.opacity    = matches ? '1' : '0.25';
          card.style.pointerEvents = matches ? '' : 'none';
          if (matches) visible++;
        });

        // Show/hide empty state
        var emptyState = productGrid.querySelector('.products__no-results, .dash-empty');
        if (emptyState) {
          emptyState.style.display = visible === 0 ? 'block' : 'none';
        }
      }, 220);
    });
  }

  /* ──────────────────────────────────────────────
     2. PRODUCT IMAGE GALLERY SWITCHER
     On the product detail page, clicking a
     thumbnail swaps the main image.
     Expects: .gallery__main img + .gallery__thumb
  ────────────────────────────────────────────── */
  function initGallery() {
    var mainImg = document.querySelector('.gallery__main img, #product-main-img');
    var thumbs  = document.querySelectorAll('.gallery__thumb, [data-gallery-thumb]');

    if (!mainImg || !thumbs.length) return;

    thumbs.forEach(function (thumb) {
      thumb.style.cursor = 'pointer';
      thumb.style.opacity = '0.7';
      thumb.style.transition = 'opacity 0.2s ease, border-color 0.2s ease';

      thumb.addEventListener('click', function () {
        var src = thumb.getAttribute('data-src') || thumb.src || thumb.getAttribute('src');
        if (!src) return;

        // Fade swap
        mainImg.style.transition = 'opacity 0.2s ease';
        mainImg.style.opacity    = '0';
        setTimeout(function () {
          mainImg.src           = src;
          mainImg.style.opacity = '1';
        }, 200);

        // Active state
        thumbs.forEach(function (t) {
          t.style.opacity     = '0.7';
          t.style.border      = '2px solid transparent';
        });
        thumb.style.opacity = '1';
        thumb.style.border  = '2px solid #1e8a57';
      });
    });
  }

  /* ──────────────────────────────────────────────
     3. FARMER PROFILE CARD HOVER EFFECTS
     Subtle lift and border glow on profile cards.
     Works with .profile__card or [data-farmer-card]
  ────────────────────────────────────────────── */
  function initProfileCards() {
    var cards = document.querySelectorAll('.profile__card, [data-farmer-card]');

    cards.forEach(function (card) {
      card.addEventListener('mouseenter', function () {
        card.style.transition  = 'transform 0.22s ease, box-shadow 0.22s ease';
        card.style.transform   = 'translateY(-4px)';
        card.style.boxShadow   = '0 8px 28px rgba(17,56,33,0.13)';
      });

      card.addEventListener('mouseleave', function () {
        card.style.transform = 'translateY(0)';
        card.style.boxShadow = '';
      });
    });
  }

  /* ──────────────────────────────────────────────
     4. DASHBOARD STAT COUNTER ANIMATION
     Animates .stat-card__value numbers from 0
     up to their final value on page load.
  ────────────────────────────────────────────── */
  function initStatCounters() {
    var counters = document.querySelectorAll('.stat-card__value');
    if (!counters.length) return;

    counters.forEach(function (el) {
      var raw    = el.textContent.trim();
      var target = parseInt(raw.replace(/[^0-9]/g, ''), 10);
      if (isNaN(target) || target === 0) return;

      var start    = 0;
      var duration = 900; // ms
      var startTime = null;

      function step(timestamp) {
        if (!startTime) startTime = timestamp;
        var progress = Math.min((timestamp - startTime) / duration, 1);
        // Ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(eased * target);
        if (progress < 1) requestAnimationFrame(step);
        else el.textContent = raw; // restore original (may have symbols)
      }

      // Use IntersectionObserver so it fires when visible
      if ('IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) {
              requestAnimationFrame(step);
              observer.unobserve(el);
            }
          });
        }, { threshold: 0.3 });
        observer.observe(el);
      } else {
        requestAnimationFrame(step);
      }
    });
  }

  /* ──────────────────────────────────────────────
     5. LOGIN FORM — SHOW / HIDE PASSWORD
     Injects a toggle button next to password
     fields so users can verify what they typed.
  ────────────────────────────────────────────── */
  function initPasswordToggle() {
    var passwordFields = document.querySelectorAll('input[type="password"]');

    passwordFields.forEach(function (field) {
      var wrapper = field.parentNode;

      // Wrap if not already wrapped
      var wrapDiv = document.createElement('div');
      wrapDiv.style.cssText = 'position:relative;display:flex;align-items:center;';
      field.parentNode.insertBefore(wrapDiv, field);
      wrapDiv.appendChild(field);

      var toggle = document.createElement('button');
      toggle.type = 'button';
      toggle.innerHTML = '👁';
      toggle.title = 'Show / hide password';
      toggle.setAttribute('aria-label', 'Toggle password visibility');

      Object.assign(toggle.style, {
        position:   'absolute',
        right:      '1.2rem',
        background: 'none',
        border:     'none',
        cursor:     'pointer',
        fontSize:   '1.5rem',
        padding:    '0',
        color:      '#64748b',
        lineHeight: '1',
        opacity:    '0.7',
      });

      wrapDiv.appendChild(toggle);

      toggle.addEventListener('click', function () {
        var isPassword = field.type === 'password';
        field.type     = isPassword ? 'text' : 'password';
        toggle.innerHTML = isPassword ? '🙈' : '👁';
        toggle.title     = isPassword ? 'Hide password' : 'Show password';
      });
    });
  }

  /* ──────────────────────────────────────────────
     6. STICKY NAVBAR SHADOW ON SCROLL
     Adds a deeper shadow to the header when the
     user scrolls down, giving depth to the nav.
  ────────────────────────────────────────────── */
  function initNavbarScroll() {
    var header = document.querySelector('.header');
    if (!header) return;

    var scrolled = false;

    window.addEventListener('scroll', function () {
      if (window.scrollY > 10 && !scrolled) {
        scrolled = true;
        header.style.boxShadow = '0 4px 24px rgba(0,0,0,0.22)';
      } else if (window.scrollY <= 10 && scrolled) {
        scrolled = false;
        header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
      }
    });
  }

  /* ──────────────────────────────────────────────
     7. LAZY LOADING IMAGES
     Images with data-src get their src swapped
     in when they enter the viewport.
     Also adds a fade-in on load.
  ────────────────────────────────────────────── */
  function initLazyImages() {
    var lazyImgs = document.querySelectorAll('img[data-src]');
    if (!lazyImgs.length) return;

    if (!('IntersectionObserver' in window)) {
      // Fallback: load all immediately
      lazyImgs.forEach(function (img) { img.src = img.getAttribute('data-src'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var img = entry.target;
        img.style.opacity    = '0';
        img.style.transition = 'opacity 0.4s ease';
        img.src = img.getAttribute('data-src');
        img.removeAttribute('data-src');
        img.onload = function () { img.style.opacity = '1'; };
        observer.unobserve(img);
      });
    }, { rootMargin: '100px' });

    lazyImgs.forEach(function (img) { observer.observe(img); });
  }

  /* ──────────────────────────────────────────────
     8. PRODUCT CARD QUICK-VIEW TOOLTIP
     Shows a subtle price/unit tooltip on hover
     over product cards that have data-price set.
  ────────────────────────────────────────────── */
  function initQuickView() {
    var cards = document.querySelectorAll('[data-price][data-product-name]');
    if (!cards.length) return;

    var tip = document.createElement('div');
    tip.id = 'soko-quicktip';
    Object.assign(tip.style, {
      position:     'fixed',
      background:   '#113821',
      color:        '#fff',
      padding:      '0.6rem 1.2rem',
      borderRadius: '6px',
      fontSize:     '1.2rem',
      fontWeight:   '600',
      pointerEvents:'none',
      zIndex:       '8000',
      opacity:      '0',
      transition:   'opacity 0.15s ease',
      whiteSpace:   'nowrap',
      borderLeft:   '3px solid #f1c40f',
      fontFamily:   "'Inter', sans-serif",
    });
    document.body.appendChild(tip);

    cards.forEach(function (card) {
      card.addEventListener('mouseenter', function (e) {
        var price = card.getAttribute('data-price');
        var name  = card.getAttribute('data-product-name');
        if (!price) return;
        tip.textContent = name + ' — KES ' + parseFloat(price).toLocaleString();
        tip.style.opacity = '1';
      });

      card.addEventListener('mousemove', function (e) {
        tip.style.left = (e.clientX + 14) + 'px';
        tip.style.top  = (e.clientY - 10) + 'px';
      });

      card.addEventListener('mouseleave', function () {
        tip.style.opacity = '0';
      });
    });
  }

  /* ──────────────────────────────────────────────
     9. SELECT → STYLED TAG DISPLAY
     When a <select data-tag-display> changes,
     shows the selected option as a pill tag
     below the select.
  ────────────────────────────────────────────── */
  function initSelectTags() {
    var selects = document.querySelectorAll('select[data-tag-display]');

    selects.forEach(function (select) {
      var containerId = select.getAttribute('data-tag-display');
      var container   = document.querySelector(containerId);
      if (!container) return;

      function render() {
        var selected = Array.from(select.selectedOptions).map(function (o) { return o.text; });
        container.innerHTML = selected.map(function (label) {
          return '<span style="display:inline-flex;align-items:center;gap:0.4rem;padding:4px 12px;'
            + 'background:#d4edda;color:#113821;border-radius:99px;font-size:1.2rem;font-weight:600;margin:2px;">'
            + label + '</span>';
        }).join('');
      }

      select.addEventListener('change', render);
      render();
    });
  }

  /* ──────────────────────────────────────────────
     10. MOBILE DASHBOARD SIDEBAR TOGGLE
     For the dashboard layout on small screens,
     a hamburger button with id="dash-menu-toggle"
     slides the sidebar in/out.
  ────────────────────────────────────────────── */
  function initDashSidebar() {
    var toggleBtn = document.getElementById('dash-menu-toggle');
    var sidebar   = document.querySelector('.dash-sidebar');
    var overlay   = document.getElementById('dash-overlay');

    if (!toggleBtn || !sidebar) return;

    function openSidebar() {
      sidebar.style.transform  = 'translateX(0)';
      sidebar.style.transition = 'transform 0.28s ease';
      if (overlay) {
        overlay.style.display  = 'block';
        overlay.style.opacity  = '1';
      }
    }

    function closeSidebar() {
      sidebar.style.transform = 'translateX(-100%)';
      if (overlay) overlay.style.opacity = '0';
    }

    toggleBtn.addEventListener('click', function () {
      var isOpen = sidebar.style.transform === 'translateX(0px)' ||
                   sidebar.style.transform === 'translateX(0)';
      isOpen ? closeSidebar() : openSidebar();
    });

    if (overlay) {
      overlay.addEventListener('click', closeSidebar);
    }

    // Close on nav link click
    sidebar.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeSidebar);
    });
  }

  /* ──────────────────────────────────────────────
     INIT — run everything on DOM ready
  ────────────────────────────────────────────── */
  function init() {
    initLiveSearch();
    initGallery();
    initProfileCards();
    initStatCounters();
    initPasswordToggle();
    initNavbarScroll();
    initLazyImages();
    initQuickView();
    initSelectTags();
    initDashSidebar();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();