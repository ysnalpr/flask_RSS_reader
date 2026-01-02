// Search (client-side filter)
const searchBar = document.getElementById("searchBar");
const grid = document.getElementById("newsGrid");
const cards = () => Array.from(grid.querySelectorAll(".news-card"));

if (searchBar) {
  searchBar.addEventListener("input", () => {
    const q = searchBar.value.trim().toLowerCase();
    cards().forEach((card) => {
      const t = card.dataset.title || "";
      const d = card.dataset.desc || "";
      card.style.display = (t.includes(q) || d.includes(q)) ? "" : "none";
    });
  });
}

// Copy link buttons
document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".copyBtn");
  if (!btn) return;

  const link = btn.getAttribute("data-link");
  try {
    await navigator.clipboard.writeText(link);
    btn.textContent = "کپی شد ✅";
    setTimeout(() => (btn.textContent = "کپی لینک"), 1200);
  } catch {
    btn.textContent = "ناموفق ❌";
    setTimeout(() => (btn.textContent = "کپی لینک"), 1200);
  }
});

// Theme toggle (dark/light)
const themeBtn = document.getElementById("themeBtn");
const themeIcon = document.getElementById("themeIcon");

function setTheme(mode) {
  document.documentElement.setAttribute("data-theme", mode);
  localStorage.setItem("theme", mode);
  if (themeIcon) themeIcon.textContent = (mode === "light") ? "☀️" : "🌙";
}

const saved = localStorage.getItem("theme");
if (saved) setTheme(saved);

if (themeBtn) {
  themeBtn.addEventListener("click", () => {
    const current = document.documentElement.getAttribute("data-theme") || "dark";
    setTheme(current === "dark" ? "light" : "dark");
  });
}


// server-side search submit
const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchBar");

let searchTimer = null;

if (searchForm && searchInput) {
  searchInput.addEventListener("input", () => {
    clearTimeout(searchTimer);

    searchTimer = setTimeout(() => {
      // always reset to page 1 on a new query
      const pageInput = searchForm.querySelector('input[name="page"]');
      if (pageInput) pageInput.value = "1";

      searchForm.submit();
    }, 500); // 500ms is default (change to 300 if you want faster)
  });
}
