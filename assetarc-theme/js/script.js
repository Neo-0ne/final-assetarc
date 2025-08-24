// main.js — AssetArc Theme Scripts

document.addEventListener('DOMContentLoaded', function () {
  // Example: Toggle mobile navigation
  const menuToggle = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (menuToggle && navMenu) {
    menuToggle.addEventListener('click', function () {
      navMenu.classList.toggle('active');
    });
  }

  // Example: Preloader fade out
  const preloader = document.querySelector('.preloader');
  if (preloader) {
    window.addEventListener('load', () => {
      preloader.classList.add('fade-out');
      setTimeout(() => preloader.style.display = 'none', 1000);
    });
  }

  // Smooth scroll for anchor links
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach(link => {
    link.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Vault access form handler
  const vaultLoginForm = document.getElementById('vault-login');
  if (vaultLoginForm) {
    vaultLoginForm.addEventListener('submit', function (e) {
      e.preventDefault();
      const token = document.getElementById('token').value;
      const vaultContent = document.getElementById('vault-content');
      const vaultDocuments = document.getElementById('vault-documents');

      // Make an API call to the vault
      fetch('/wp-content/themes/assetarc-theme/Vault_API/vault-access.php', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          vaultContent.innerHTML = '';
          data.files.forEach(file => {
            const link = document.createElement('a');
            link.href = file.url;
            link.textContent = 'Download ' + file.name;
            link.className = 'block p-4 bg-gray-800 rounded';
            vaultContent.appendChild(link);
          });
          vaultDocuments.classList.remove('hidden');
        } else {
          alert(data.message);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while accessing the vault.');
      });
    });
  }
});
