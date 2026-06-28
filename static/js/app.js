/* ============================================================
   Soko Direct — app.js
   Global JavaScript — loaded on every page via main.html
   Covers:
     1. Alert / message auto-dismiss
     2. Mobile navbar toggle
     3. Image upload preview
     4. Client-side form validation
     5. Active nav link highlighting
     6. Smooth scroll
     7. Confirm dialogs (delete actions)
     8. Character counters
     9. Button loading states
    10. Back-to-top button
   ============================================================ */

(function () {
  'use strict';

  /* ──────────────────────────────────────────────
     1. ALERT / MESSAGE AUTO-DISMISS
     Dismisses Django messages after 4 seconds.
     Also wires the × close button.
  ────────────────────────────────────────────── */
  function initAlerts() {
    const alerts = document.querySelectorAll('.alert, .dash-alert, .pf-alert');

    alerts.forEach(function (alert) {
      // Auto-dismiss after 4 s
      setTimeout(function () {
        dismissAlert(alert);
      }, 4000);

      // Manual close button
      const closeBtn = alert.querySelector('.alert__close, [data-dismiss="alert"]');
      if (closeBtn) {
        closeBtn.addEventListener('click', function () {
          dismissAlert(alert);
        });
      }
    });
  }

  function dismissAlert(alert) {
    alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    alert.style.opacity = '0';
    alert.style.transform = 'translateY(-8px)';
    setTimeout(function () {
      if (alert.parentNode) alert.parentNode.removeChild(alert);
    }, 420);
  }

  /* ──────────────────────────────────────────────
     2. MOBILE NAVBAR TOGGLE
     Works with the checkbox toggle pattern in
     navbar.html (#responsive-menu checkbox).
     Also closes menu when a nav link is clicked.
  ────────────────────────────────────────────── */
  function initNavbar() {
    const menuCheckbox = document.getElementById('responsive-menu');
    if (!menuCheckbox) return;

    // Close menu when any nav link is tapped (mobile UX)
    const navLinks = document.querySelectorAll('.header__menu a');
    navLinks.forEach(function (link) {
      link.addEventListener('click', function () {
        menuCheckbox.checked = false;
      });
    });

    // Close menu when clicking outside the header
    document.addEventListener('click', function (e) {
      const header = document.querySelector('.header');
      if (header && !header.contains(e.target)) {
        menuCheckbox.checked = false;
      }
    });
  }

  /* ──────────────────────────────────────────────
     3. IMAGE UPLOAD PREVIEW
     Works with .pf-upload-zone (productForm.css).
     Shows a preview thumbnail when a file is chosen.
     Also supports plain <input type="file"> with
     data-preview="#someImgId".
  ────────────────────────────────────────────── */
  function initImageUpload() {
    // --- productForm upload zones ---
    const uploadZones = document.querySelectorAll('.pf-upload-zone');
    uploadZones.forEach(function (zone) {
      const input = zone.querySelector('input[type="file"]');
      const preview = zone.querySelector('.pf-upload-preview');
      const previewImg = preview ? preview.querySelector('img') : null;
      const removeBtn = preview ? preview.querySelector('.pf-upload-preview__remove') : null;

      if (!input) return;

      // Drag-over styling
      zone.addEventListener('dragover', function (e) {
        e.preventDefault();
        zone.classList.add('pf-upload-zone--active');
      });
      zone.addEventListener('dragleave', function () {
        zone.classList.remove('pf-upload-zone--active');
      });
      zone.addEventListener('drop', function (e) {
        e.preventDefault();
        zone.classList.remove('pf-upload-zone--active');
        if (e.dataTransfer.files.length) {
          input.files = e.dataTransfer.files;
          input.dispatchEvent(new Event('change'));
        }
      });

      input.addEventListener('change', function () {
        const file = input.files[0];
        if (!file || !file.type.startsWith('image/')) return;

        if (previewImg && preview) {
          const reader = new FileReader();
          reader.onload = function (e) {
            previewImg.src = e.target.result;
            preview.style.display = 'block';
          };
          reader.readAsDataURL(file);
        }
      });

      if (removeBtn) {
        removeBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          input.value = '';
          if (previewImg) previewImg.src = '';
          if (preview) preview.style.display = 'none';
        });
      }
    });

    // --- Generic: <input type="file" data-preview="#imgId"> ---
    const genericInputs = document.querySelectorAll('input[type="file"][data-preview]');
    genericInputs.forEach(function (input) {
      const targetId = input.getAttribute('data-preview');
      const imgEl = document.querySelector(targetId);
      if (!imgEl) return;

      input.addEventListener('change', function () {
        const file = input.files[0];
        if (!file || !file.type.startsWith('image/')) return;
        const reader = new FileReader();
        reader.onload = function (e) { imgEl.src = e.target.result; };
        reader.readAsDataURL(file);
      });
    });
  }

  /* ──────────────────────────────────────────────
     4. CLIENT-SIDE FORM VALIDATION
     Marks required fields on submit if empty.
     Works alongside Django server-side validation.
     Add class="pf-form--validate" to any <form>
     to opt in.
  ────────────────────────────────────────────── */
  function initFormValidation() {
    const forms = document.querySelectorAll('form.pf-form--validate');

    forms.forEach(function (form) {
      form.addEventListener('submit', function (e) {
        let valid = true;

        // Clear previous errors
        form.querySelectorAll('.pf-input--error, .pf-select--error, .pf-textarea--error')
          .forEach(function (el) {
            el.classList.remove('pf-input--error', 'pf-select--error', 'pf-textarea--error');
          });
        form.querySelectorAll('.pf-error-text[data-auto]')
          .forEach(function (el) { el.remove(); });

        // Check required fields
        form.querySelectorAll('[required]').forEach(function (field) {
          if (!field.value.trim()) {
            valid = false;
            markFieldError(field, 'This field is required.');
          }
        });

        // Check min length
        form.querySelectorAll('[data-minlength]').forEach(function (field) {
          const min = parseInt(field.getAttribute('data-minlength'), 10);
          if (field.value.trim().length < min) {
            valid = false;
            markFieldError(field, 'Minimum ' + min + ' characters required.');
          }
        });

        // Check numeric fields
        form.querySelectorAll('input[type="number"]').forEach(function (field) {
          if (field.value && isNaN(parseFloat(field.value))) {
            valid = false;
            markFieldError(field, 'Please enter a valid number.');
          }
          const min = field.getAttribute('min');
          if (min !== null && parseFloat(field.value) < parseFloat(min)) {
            valid = false;
            markFieldError(field, 'Value must be at least ' + min + '.');
          }
        });

        if (!valid) {
          e.preventDefault();
          // Scroll to first error
          const firstError = form.querySelector('.pf-input--error, .pf-select--error, .pf-textarea--error');
          if (firstError) {
            firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
            firstError.focus();
          }
        }
      });
    });
  }

  function markFieldError(field, message) {
    const errorClass = field.tagName === 'SELECT'
      ? 'pf-select--error'
      : field.tagName === 'TEXTAREA'
        ? 'pf-textarea--error'
        : 'pf-input--error';

    field.classList.add(errorClass);

    const errEl = document.createElement('span');
    errEl.className = 'pf-error-text';
    errEl.setAttribute('data-auto', '1');
    errEl.innerHTML = '⚠ ' + message;

    const parent = field.closest('.pf-group') || field.parentNode;
    parent.appendChild(errEl);
  }

  /* ──────────────────────────────────────────────
     5. ACTIVE NAV LINK HIGHLIGHTING
     Adds an active class to the nav link whose
     href matches the current page URL.
  ────────────────────────────────────────────── */
  function initActiveNav() {
    const currentPath = window.location.pathname;

    // Main navbar
    document.querySelectorAll('.header__menu a').forEach(function (link) {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
        link.style.color = '#f1c40f';
        link.style.fontWeight = '700';
      }
    });

    // Dashboard sidebar nav
    document.querySelectorAll('.dash-nav__item a').forEach(function (link) {
      const href = link.getAttribute('href');
      if (!href || href === '#') return;
      const li = link.closest('.dash-nav__item');
      if (!li) return;

      if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
        li.classList.add('dash-nav__item--active');
      } else {
        li.classList.remove('dash-nav__item--active');
      }
    });
  }

  /* ──────────────────────────────────────────────
     6. SMOOTH SCROLL
     All anchor links with href="#something"
     scroll smoothly to the target.
  ────────────────────────────────────────────── */
  function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        const targetId = link.getAttribute('href');
        if (targetId === '#') return;
        const target = document.querySelector(targetId);
        if (target) {
          e.preventDefault();
          target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      });
    });
  }

  /* ──────────────────────────────────────────────
     7. CONFIRM DIALOGS (DELETE ACTIONS)
     Any link or button with data-confirm="message"
     shows a confirmation dialog before navigating.
     Prevents accidental deletes.
  ────────────────────────────────────────────── */
  function initConfirmDialogs() {
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        const msg = el.getAttribute('data-confirm') || 'Are you sure you want to delete this? This action cannot be undone.';
        if (!window.confirm(msg)) {
          e.preventDefault();
          e.stopPropagation();
        }
      });
    });
  }

  /* ──────────────────────────────────────────────
     8. CHARACTER COUNTERS
     Add data-maxlength="200" to any input/textarea
     and pair it with a <span data-counter="fieldId">
     to show a live count.
  ────────────────────────────────────────────── */
  function initCharCounters() {
    document.querySelectorAll('[data-maxlength]').forEach(function (field) {
      const max = parseInt(field.getAttribute('data-maxlength'), 10);
      const counterId = field.id ? '[data-counter="' + field.id + '"]' : null;
      const counter = counterId ? document.querySelector(counterId) : null;

      // Create counter if it doesn't exist but field is inside .pf-group
      let counterEl = counter;
      if (!counterEl) {
        const group = field.closest('.pf-group');
        if (group) {
          counterEl = document.createElement('span');
          counterEl.className = 'pf-char-counter';
          group.appendChild(counterEl);
        }
      }

      function updateCounter() {
        if (!counterEl) return;
        const remaining = max - field.value.length;
        counterEl.textContent = field.value.length + ' / ' + max;
        counterEl.classList.remove('pf-char-counter--warn', 'pf-char-counter--limit');
        if (remaining <= 0) {
          counterEl.classList.add('pf-char-counter--limit');
        } else if (remaining <= max * 0.1) {
          counterEl.classList.add('pf-char-counter--warn');
        }
      }

      field.setAttribute('maxlength', max);
      field.addEventListener('input', updateCounter);
      updateCounter();
    });
  }

  /* ──────────────────────────────────────────────
     9. BUTTON LOADING STATES
     Add data-loading="Saving..." to any submit
     button to show a spinner text while the
     form submits and prevent double-clicks.
  ────────────────────────────────────────────── */
  function initLoadingButtons() {
    document.querySelectorAll('[data-loading]').forEach(function (btn) {
      const originalText = btn.innerHTML;
      const loadingText  = btn.getAttribute('data-loading') || 'Loading...';

      const form = btn.closest('form');
      if (form) {
        form.addEventListener('submit', function () {
          // Only trigger if form is valid (no pf-input--error visible)
          const hasErrors = form.querySelector('.pf-input--error, .pf-select--error, .pf-textarea--error');
          if (!hasErrors) {
            btn.disabled = true;
            btn.innerHTML = '<span style="display:inline-flex;align-items:center;gap:0.6rem;">'
              + '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" style="animation:pf-spin 0.8s linear infinite;">'
              + '<path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>'
              + '</svg>' + loadingText + '</span>';
          }
        });
      }

      // Reset if user navigates back
      window.addEventListener('pageshow', function () {
        btn.disabled = false;
        btn.innerHTML = originalText;
      });
    });

    // Inject spin keyframe once
    if (!document.getElementById('pf-spin-style')) {
      const style = document.createElement('style');
      style.id = 'pf-spin-style';
      style.textContent = '@keyframes pf-spin { to { transform: rotate(360deg); } }';
      document.head.appendChild(style);
    }
  }

  /* ──────────────────────────────────────────────
     10. BACK-TO-TOP BUTTON
     Injects a floating button that appears after
     scrolling 300px. Smooth-scrolls back to top.
  ────────────────────────────────────────────── */
  function initBackToTop() {
    const btn = document.createElement('button');
    btn.id = 'soko-back-top';
    btn.title = 'Back to top';
    btn.innerHTML = '↑';
    btn.setAttribute('aria-label', 'Back to top');

    Object.assign(btn.style, {
      position:       'fixed',
      bottom:         '2.4rem',
      right:          '2.4rem',
      width:          '4.4rem',
      height:         '4.4rem',
      borderRadius:   '50%',
      background:     '#1e8a57',
      color:          '#fff',
      border:         'none',
      fontSize:       '2rem',
      fontWeight:     '700',
      cursor:         'pointer',
      boxShadow:      '0 4px 14px rgba(0,0,0,0.15)',
      opacity:        '0',
      transform:      'translateY(12px)',
      transition:     'opacity 0.3s ease, transform 0.3s ease',
      pointerEvents:  'none',
      zIndex:         '9000',
      lineHeight:     '1',
      display:        'flex',
      alignItems:     'center',
      justifyContent: 'center',
    });

    document.body.appendChild(btn);

    window.addEventListener('scroll', function () {
      if (window.scrollY > 300) {
        btn.style.opacity      = '1';
        btn.style.transform    = 'translateY(0)';
        btn.style.pointerEvents = 'auto';
      } else {
        btn.style.opacity      = '0';
        btn.style.transform    = 'translateY(12px)';
        btn.style.pointerEvents = 'none';
      }
    });

    btn.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  /* ──────────────────────────────────────────────
     INIT — run everything on DOM ready
  ────────────────────────────────────────────── */
  function init() {
    initAlerts();
    initNavbar();
    initImageUpload();
    initFormValidation();
    initActiveNav();
    initSmoothScroll();
    initConfirmDialogs();
    initCharCounters();
    initLoadingButtons();
    initBackToTop();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();