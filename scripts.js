// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
  const burger = document.querySelector('.burger');
  const mobileNav = document.querySelector('.mobile-nav');
  const mobileNavClose = document.querySelector('.mobile-nav-close');
  const modal = document.getElementById('image-modal');
  const modalClose = document.querySelector('.modal-close');
  const modalPrev = document.querySelector('.modal-prev');
  const modalNext = document.querySelector('.modal-next');

  if (burger && mobileNav) {
    burger.addEventListener('click', function() {
      mobileNav.classList.toggle('active');
      burger.classList.toggle('open');
    });
  }

  if (mobileNavClose) {
    mobileNavClose.addEventListener('click', function() {
      mobileNav.classList.remove('active');
      burger.classList.remove('open');
    });
  }

  const mobileLinks = mobileNav ? mobileNav.querySelectorAll('a') : [];
  mobileLinks.forEach(link => {
    link.addEventListener('click', function() {
      mobileNav.classList.remove('active');
      burger.classList.remove('open');
    });
  });

  // Modal Lightbox
  if (modal && modalClose) {
    modalClose.addEventListener('click', function() {
      modal.classList.remove('active');
    });

    modal.addEventListener('click', function(e) {
      if (e.target === modal) {
        modal.classList.remove('active');
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        modal.classList.remove('active');
      } else if (e.key === 'ArrowLeft') {
        if (typeof showPrevImage === 'function') showPrevImage();
      } else if (e.key === 'ArrowRight') {
        if (typeof showNextImage === 'function') showNextImage();
      }
    });

    // Touch-Swipe für Mobile
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;

    modal.addEventListener('touchstart', function(e) {
      touchStartX = e.changedTouches[0].screenX;
      touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    modal.addEventListener('touchend', function(e) {
      touchEndX = e.changedTouches[0].screenX;
      touchEndY = e.changedTouches[0].screenY;

      const dx = touchEndX - touchStartX;
      const dy = touchEndY - touchStartY;
      const absDx = Math.abs(dx);
      const absDy = Math.abs(dy);

      // Swipe nach oben → Modal schließen
      if (absDy > absDx && dy < -60) {
        modal.classList.remove('active');
        return;
      }

      // Horizontaler Swipe → Bild wechseln
      if (absDx > absDy && absDx > 50) {
        if (dx < 0) {
          if (typeof showNextImage === 'function') showNextImage();
        } else {
          if (typeof showPrevImage === 'function') showPrevImage();
        }
      }
    }, { passive: true });
  }

  // Modal-Navigation Buttons (nur auf Seiten mit Gallery vorhanden)
  if (modalPrev) {
    modalPrev.addEventListener('click', function() {
      if (typeof showPrevImage === 'function') showPrevImage();
    });
  }
  if (modalNext) {
    modalNext.addEventListener('click', function() {
      if (typeof showNextImage === 'function') showNextImage();
    });
  }

  // News-Popup schließen
  const newsPopupClose = document.querySelector('.news-popup-close');
  if (newsPopupClose) {
    newsPopupClose.addEventListener('click', function() {
      const popup = document.getElementById('news-popup');
      if (!popup) return;
      popup.classList.add('is-closing');
      popup.addEventListener('animationend', function() {
        popup.style.display = 'none';
        sessionStorage.setItem('news-popup-seen', '1');
      }, { once: true });
    });
  }
});
