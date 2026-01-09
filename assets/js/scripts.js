var body = document.querySelector("body");
// mobile menu toggle handled via delegated click listener below so it continues to work after DOM replacements

// Removed stray audio call which caused console errors when audioElement was undefined.

// Language toggle enhancement: fetch translated page and replace wrapper for fast toggle
(function () {
  function queryWrapperFromHTML(htmlText) {
    var tmp = document.implementation.createHTMLDocument("tmp");
    tmp.documentElement.innerHTML = htmlText;
    return {
      wrapper: tmp.querySelector("#wrapper"),
      title: tmp.querySelector("title"),
      langButton: tmp.querySelector("#language-toggle-button"),
      mainMenuMobile: tmp.querySelector("#main-menu-mobile"),
      mainMenu: tmp.querySelector("#main-menu"),
    };
  }

  // Delegated click handler handles both mobile menu toggling and language switching
  document.addEventListener("click", function (e) {
    // Mobile menu toggle
    var menuBtn = e.target.closest("#toggle-main-menu-mobile");
    if (menuBtn) {
      var menu = document.querySelector("#main-menu-mobile");
      if (!menu) return;
      menu.classList.toggle("open");
      menuBtn.classList.toggle("is-active");
      body.classList.toggle("lock-scroll");
      return;
    }

    // Language toggle
    var langAnchor = e.target.closest("#language-toggle-button");
    if (!langAnchor) return;
    var href = langAnchor.getAttribute("href");
    if (!href) return;
    // If href is an absolute URL that is not same-origin, let browser handle it
    if (href.indexOf("://") !== -1 && href.indexOf(location.origin) !== 0) {
      return;
    }
    e.preventDefault();

    fetch(href, { credentials: "same-origin" })
      .then(function (resp) {
        if (!resp.ok) throw new Error("Fetch failed");
        return resp.text();
      })
      .then(function (text) {
        var parsed = queryWrapperFromHTML(text);
        if (parsed.wrapper) {
          var currentWrapper = document.querySelector("#wrapper");
          currentWrapper.innerHTML = parsed.wrapper.innerHTML;
        }
        if (parsed.title) {
          document.title = parsed.title.textContent;
        }
        // update language button to new one from fetched page
        if (parsed.langButton) {
          var curBtn = document.querySelector("#language-toggle-button");
          if (curBtn && parsed.langButton) {
            curBtn.outerHTML = parsed.langButton.outerHTML;
          }
        }
        // update mobile menu to new one from fetched page
        if (parsed.mainMenuMobile) {
          var curMenu = document.querySelector("#main-menu-mobile");
          if (curMenu) curMenu.outerHTML = parsed.mainMenuMobile.outerHTML;
        }
        // update desktop main menu to new one from fetched page
        if (parsed.mainMenu) {
          var curMainMenu = document.querySelector("#main-menu");
          if (curMainMenu) curMainMenu.outerHTML = parsed.mainMenu.outerHTML;
        }
        history.pushState({ path: href }, "", href);
        window.scrollTo(0, 0);
      })
      .catch(function () {
        // fallback to full navigation
        window.location.href = href;
      });
  });

  // handle back/forward
  window.addEventListener("popstate", function (e) {
    if (!e.state || !e.state.path) return;
    fetch(e.state.path)
      .then(function (r) {
        return r.text();
      })
      .then(function (text) {
        var parsed = queryWrapperFromHTML(text);
        if (parsed.wrapper) {
          document.querySelector("#wrapper").innerHTML =
            parsed.wrapper.innerHTML;
        }
        if (parsed.title) {
          document.title = parsed.title.textContent;
        }
        if (parsed.langButton) {
          var curBtn = document.querySelector("#language-toggle-button");
          if (curBtn) curBtn.outerHTML = parsed.langButton.outerHTML;
        }
        if (parsed.mainMenuMobile) {
          var curMenu = document.querySelector("#main-menu-mobile");
          if (curMenu) curMenu.outerHTML = parsed.mainMenuMobile.outerHTML;
        }
        if (parsed.mainMenu) {
          var curMainMenu = document.querySelector("#main-menu");
          if (curMainMenu) curMainMenu.outerHTML = parsed.mainMenu.outerHTML;
        }
      });
  });
})();
