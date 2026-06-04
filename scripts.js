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
        showPrevImage();
      } else if (e.key === 'ArrowRight') {
        showNextImage();
      }
    });
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
