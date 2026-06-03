// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
  const burger = document.querySelector('.burger');
  const mobileNav = document.querySelector('.mobile-nav');
  const mobileNavClose = document.querySelector('.mobile-nav-close');
  const modal = document.getElementById('image-modal');
  const modalClose = document.querySelector('.modal-close');
  const modalImg = modal ? modal.querySelector('.modal-image') : null;
  const spinner = document.getElementById('modal-spinner');

  if (burger && mobileNav) {
    burger.addEventListener('click', function() {
      mobileNav.classList.toggle('active');
    });
  }

  if (mobileNavClose) {
    mobileNavClose.addEventListener('click', function() {
      mobileNav.classList.remove('active');
    });
  }

  const mobileLinks = mobileNav ? mobileNav.querySelectorAll('a') : [];
  mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
      mobileNav.classList.remove('active');
    });
  });

  // ── Modal Lightbox ───────────────────────────────────────────────
  if (modal && modalClose) {
    modalClose.addEventListener('click', () => modal.classList.remove('active'));

    modal.addEventListener('click', function(e) {
      if (e.target === modal) modal.classList.remove('active');
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape')       modal.classList.remove('active');
      else if (e.key === 'ArrowLeft')  showPrevImage();
      else if (e.key === 'ArrowRight') showNextImage();
    });
  }

  // ── Loading indicator for modal image ───────────────────────────
  if (modalImg && spinner) {
    modalImg.addEventListener('load', () => {
      modalImg.classList.remove('loading');
      spinner.classList.remove('visible');
    });
  }

  // ── Swipe gesture for modal ──────────────────────────────────────
  if (modal) {
    let touchStartX = null;
    let touchStartY = null;

    modal.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].clientX;
      touchStartY = e.changedTouches[0].clientY;
    }, { passive: true });

    modal.addEventListener('touchend', function(e) {
      if (touchStartX === null) return;
      const dx = e.changedTouches[0].clientX - touchStartX;
      const dy = e.changedTouches[0].clientY - touchStartY;
      // only act on clearly horizontal swipes
      if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        if (dx < 0) showNextImage();
        else        showPrevImage();
      }
      touchStartX = null;
      touchStartY = null;
    }, { passive: true });
  }

  // ── Filter animation ─────────────────────────────────────────────
  const filterBtns = document.querySelectorAll('.filter-btn');
  const gallery = document.querySelector('.gallery');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      const target = this.dataset.filter;
      filterBtns.forEach(b => b.classList.remove('active'));
      this.classList.add('active');

      const items = gallery ? gallery.querySelectorAll('.gallery-item') : [];
      // Fade out all first, then swap visibility and fade in
      items.forEach(item => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(8px)';
        item.style.transition = 'opacity 0.12s ease, transform 0.12s ease';
      });

      setTimeout(() => {
        items.forEach(item => {
          const cat = item.dataset.category;
          const visible = target === 'all' || cat === target;
          item.style.display = visible ? 'block' : 'none';
        });
        // Re-trigger fade-in for visible items with slight stagger
        const visible = gallery ? gallery.querySelectorAll('.gallery-item[style*="block"]') : [];
        visible.forEach((item, i) => {
          item.style.transition = '';
          item.style.opacity = '0';
          item.style.transform = 'translateY(8px)';
          // small stagger capped so it stays fast
          const delay = Math.min(i * 20, 80);
          setTimeout(() => {
            item.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
          }, delay);
        });
      }, 130);
    });
  });
});

// ── Modal open helper (called from gallery templates) ───────────────
function openModal(src, alt, images, index) {
  const modal = document.getElementById('image-modal');
  const modalImg = modal ? modal.querySelector('.modal-image') : null;
  const spinner = document.getElementById('modal-spinner');
  if (!modal || !modalImg) return;

  window._modalImages = images || [src];
  window._modalIndex  = index  || 0;

  _setModalImage(src, alt);
  modal.classList.add('active');
}

function _setModalImage(src, alt) {
  const modal    = document.getElementById('image-modal');
  const modalImg = modal ? modal.querySelector('.modal-image') : null;
  const spinner  = document.getElementById('modal-spinner');
  if (!modalImg) return;

  // show spinner, hide image until loaded
  modalImg.classList.add('loading');
  if (spinner) spinner.classList.add('visible');
  modalImg.src = src;
  modalImg.alt = alt || '';
}

function showPrevImage() {
  if (!window._modalImages) return;
  window._modalIndex = (window._modalIndex - 1 + window._modalImages.length) % window._modalImages.length;
  const img = window._modalImages[window._modalIndex];
  _setModalImage(img.src || img, img.alt || '');
}

function showNextImage() {
  if (!window._modalImages) return;
  window._modalIndex = (window._modalIndex + 1) % window._modalImages.length;
  const img = window._modalImages[window._modalIndex];
  _setModalImage(img.src || img, img.alt || '');
}
