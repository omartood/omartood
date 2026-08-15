(function () {
  var root = document.documentElement;
  var checkbox = document.getElementById("color-mode");
  var stored = localStorage.getItem("theme");
  var prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  var isDark = stored ? stored === "dark" : prefersDark;

  function applyTheme(dark) {
    root.setAttribute("data-theme", dark ? "dark" : "light");
    if (checkbox) checkbox.checked = dark;
  }

  applyTheme(isDark);

  if (checkbox) {
    checkbox.addEventListener("change", function () {
      var dark = checkbox.checked;
      applyTheme(dark);
      localStorage.setItem("theme", dark ? "dark" : "light");
    });
  }
})();
