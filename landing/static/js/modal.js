// ===== Ambil Elemen =====
const loginModal = document.getElementById('loginModal');
const registerModal = document.getElementById('registerModal');
const verifyModal = document.getElementById('verifyModal');

// ===== Buka Modal Login =====
document.getElementById('openLoginModal').onclick = () => {
  loginModal.style.display = 'flex';
};

// ===== Tutup Modal =====
document.querySelectorAll('.close').forEach(btn => {
  btn.onclick = () => document.getElementById(btn.dataset.close).style.display = 'none';
});

// ===== Ganti Login <-> Register =====
document.getElementById('openRegisterLink').onclick = e => {
  e.preventDefault();
  loginModal.style.display = 'none';
  registerModal.style.display = 'flex';
};

document.getElementById('openLoginLink').onclick = e => {
  e.preventDefault();
  registerModal.style.display = 'none';
  loginModal.style.display = 'flex';
};

// ===== Klik di luar modal untuk menutup =====
window.onclick = e => {
  if (e.target.classList.contains('modal')) e.target.style.display = 'none';
};

// ===== Submit Register Form (AJAX) =====
const registerForm = document.getElementById('registerForm');
registerForm.addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(registerForm);
  const response = await fetch(registerForm.action, {
    method: 'POST',
    headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
    body: formData,
  });

  const result = await response.json();
  const msg = document.getElementById('registerMessage');

  msg.textContent = result.message || result.error || 'Terjadi kesalahan.';
  msg.style.color = result.status === 'success' ? 'green' : 'red';

  if (result.status === 'success') {
    registerModal.style.display = 'none';
    verifyModal.style.display = 'flex';
  }
});

// ===== Submit Login Form (AJAX) =====
const loginForm = document.getElementById('loginForm');
loginForm.addEventListener('submit', async e => {
  e.preventDefault();
  const formData = new FormData(loginForm);
  const response = await fetch(loginForm.action, {
    method: 'POST',
    headers: { 'X-CSRFToken': formData.get('csrfmiddlewaretoken') },
    body: formData,
  });

  const result = await response.json();
  const msg = document.getElementById('loginMessage');

  msg.textContent = result.message || result.error || 'Terjadi kesalahan.';
  msg.style.color =
    result.status === 'success'
      ? 'green'
      : result.status === 'warning'
      ? 'orange'
      : 'red';

  if (result.status === 'success') {
    setTimeout(() => window.location.reload(), 1000);
  }
});

// ===== Tutup Modal Verifikasi =====
document.getElementById('closeVerifyModal').onclick = () => {
  verifyModal.style.display = 'none';
};
