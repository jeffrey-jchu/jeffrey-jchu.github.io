const themBtn = document.getElementById('theme-toggle');
const langBtn = document.getElementById('lang-toggle');

/* ── Theme ── */
const SUN  = `<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="5"/><line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/><line x1="19" y1="12" x2="22" y2="12"/><line x1="4.93" y1="4.93" x2="7.05" y2="7.05"/><line x1="16.95" y1="16.95" x2="19.07" y2="19.07"/><line x1="4.93" y1="19.07" x2="7.05" y2="16.95"/><line x1="16.95" y1="7.05" x2="19.07" y2="4.93"/></svg>`;
const MOON = `<svg viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  themBtn.innerHTML = theme === 'dark' ? SUN : MOON;
}
function toggleTheme() {
  const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  localStorage.setItem('theme', next);
}

/* ── Language ── */
function applyLang(lang) {
  document.documentElement.setAttribute('data-lang', lang);
  langBtn.textContent = lang === 'zh' ? 'EN' : '中文';
  const t = document.documentElement.dataset;
  document.title = (lang === 'zh' ? t.titleZh : t.titleEn) || document.title;
}
function toggleLang() {
  const next = document.documentElement.getAttribute('data-lang') === 'zh' ? 'en' : 'zh';
  applyLang(next);
  localStorage.setItem('lang', next);
}

/* ── Init ── */
(function () {
  const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  applyTheme(savedTheme);
  applyLang(localStorage.getItem('lang') || 'en');
})();
