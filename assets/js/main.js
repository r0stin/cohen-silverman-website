/* Cohen & Silverman Law Firm: site behaviour (no dependencies) */
(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Page ready (hero load-in) ---------- */
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { doc.body.classList.add("is-ready"); });
  });

  /* ---------- Header state via a sentinel (no scroll listeners) ---------- */
  var header = doc.querySelector("[data-header]");
  var sentinel = doc.querySelector(".scroll-sentinel");
  if (header && sentinel && "IntersectionObserver" in window) {
    new IntersectionObserver(function (entries) {
      header.classList.toggle("is-scrolled", !entries[0].isIntersecting);
    }).observe(sentinel);
  }

  /* ---------- Mega menu ---------- */
  var mega = doc.querySelector("[data-mega]");
  if (mega) {
    var trigger = mega.querySelector(".nav-trigger");
    var hoverCapable = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    var closeTimer;
    var hoverOpenedAt = 0;

    var setMega = function (open) {
      mega.classList.toggle("is-open", open);
      trigger.setAttribute("aria-expanded", open ? "true" : "false");
    };

    trigger.addEventListener("click", function () {
      // A click that lands right after hover opened the menu should not close it again.
      if (Date.now() - hoverOpenedAt < 600) return;
      setMega(trigger.getAttribute("aria-expanded") !== "true");
    });

    if (hoverCapable) {
      mega.addEventListener("mouseenter", function () {
        clearTimeout(closeTimer);
        if (!mega.classList.contains("is-open")) hoverOpenedAt = Date.now();
        setMega(true);
      });
      mega.addEventListener("mouseleave", function () { closeTimer = setTimeout(function () { setMega(false); }, 160); });
    }

    mega.addEventListener("focusout", function (e) {
      if (!mega.contains(e.relatedTarget)) setMega(false);
    });

    doc.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && mega.classList.contains("is-open")) {
        setMega(false);
        trigger.focus();
      }
    });

    doc.addEventListener("click", function (e) {
      if (!mega.contains(e.target)) setMega(false);
    });
  }

  /* ---------- Mobile navigation ---------- */
  var mobileNav = doc.getElementById("mobile-nav");
  var menuToggle = doc.querySelector(".menu-toggle");
  if (mobileNav && menuToggle) {
    var closeBtn = mobileNav.querySelector(".mobile-close");
    var lastFocus = null;

    var focusables = function () {
      return Array.prototype.slice.call(
        mobileNav.querySelectorAll("a[href], button, summary, [tabindex]:not([tabindex='-1'])")
      );
    };

    var openNav = function () {
      lastFocus = doc.activeElement;
      mobileNav.classList.add("is-open");
      mobileNav.removeAttribute("aria-hidden");
      menuToggle.setAttribute("aria-expanded", "true");
      doc.body.classList.add("is-locked");
      doc.documentElement.classList.add("is-locked");
      setTimeout(function () { closeBtn.focus(); }, 60);
    };

    var closeNav = function () {
      mobileNav.classList.remove("is-open");
      mobileNav.setAttribute("aria-hidden", "true");
      menuToggle.setAttribute("aria-expanded", "false");
      doc.body.classList.remove("is-locked");
      doc.documentElement.classList.remove("is-locked");
      if (lastFocus) lastFocus.focus();
    };

    menuToggle.addEventListener("click", openNav);
    closeBtn.addEventListener("click", closeNav);

    mobileNav.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { closeNav(); return; }
      if (e.key !== "Tab") return;
      var items = focusables();
      var first = items[0];
      var last = items[items.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    mobileNav.addEventListener("click", function (e) {
      var link = e.target.closest("a[href]");
      if (link && link.getAttribute("href").charAt(0) !== "#") closeNav();
    });

    window.matchMedia("(min-width: 1024px)").addEventListener("change", function (mq) {
      if (mq.matches && mobileNav.classList.contains("is-open")) closeNav();
    });
  }

  /* ---------- Quick-contact bar: step aside while typing (iOS keyboard) ---------- */
  var mobileBar = doc.querySelector(".mobile-bar");
  if (mobileBar) {
    var heroActions = doc.querySelector(".hero-actions, .page-hero-actions");
    if (heroActions && "IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        mobileBar.classList.toggle("is-tucked", entries[0].isIntersecting);
      }).observe(heroActions);
    }
    var isField = function (el) { return el && el.matches && el.matches("input, textarea, select"); };
    doc.addEventListener("focusin", function (e) { if (isField(e.target)) mobileBar.classList.add("is-hidden"); });
    doc.addEventListener("focusout", function (e) {
      if (!isField(e.target)) return;
      setTimeout(function () { if (!isField(doc.activeElement)) mobileBar.classList.remove("is-hidden"); }, 120);
    });
  }

  /* ---------- Scroll reveal ---------- */
  var revealEls = doc.querySelectorAll("[data-reveal]");
  doc.querySelectorAll("[data-reveal-group]").forEach(function (group) {
    Array.prototype.forEach.call(group.querySelectorAll("[data-reveal]"), function (el, i) {
      el.style.setProperty("--d", String(i));
    });
  });

  if (reduceMotion || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  }

  /* ---------- Tabs (situations) ---------- */
  doc.querySelectorAll("[data-tabs]").forEach(function (wrap) {
    var tabs = Array.prototype.slice.call(wrap.querySelectorAll('[role="tab"]'));
    var select = function (tab, focus) {
      tabs.forEach(function (t) {
        var selected = t === tab;
        t.setAttribute("aria-selected", selected ? "true" : "false");
        t.tabIndex = selected ? 0 : -1;
        var panel = doc.getElementById(t.getAttribute("aria-controls"));
        if (!panel) return;
        if (selected) {
          panel.hidden = false;
          panel.classList.remove("is-entering");
          void panel.offsetWidth;
          panel.classList.add("is-entering");
        } else {
          panel.hidden = true;
        }
      });
      if (focus) tab.focus();
      if (window.matchMedia("(max-width: 1023px)").matches) {
        tab.scrollIntoView({ block: "nearest", inline: "nearest", behavior: reduceMotion ? "auto" : "smooth" });
      }
    };
    tabs.forEach(function (tab, i) {
      tab.addEventListener("click", function () { select(tab, false); });
      tab.addEventListener("keydown", function (e) {
        var next = null;
        if (e.key === "ArrowDown" || e.key === "ArrowRight") next = tabs[(i + 1) % tabs.length];
        if (e.key === "ArrowUp" || e.key === "ArrowLeft") next = tabs[(i - 1 + tabs.length) % tabs.length];
        if (e.key === "Home") next = tabs[0];
        if (e.key === "End") next = tabs[tabs.length - 1];
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  });

  /* ---------- Accordions ---------- */
  doc.querySelectorAll(".accordion-trigger").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var item = btn.closest(".accordion-item");
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", open ? "false" : "true");
      item.classList.toggle("is-open", !open);
    });
  });

  /* ---------- Attorney bio dialogs ---------- */
  var openDialog = function (id) {
    var dlg = doc.getElementById(id);
    if (dlg && typeof dlg.showModal === "function" && !dlg.open) {
      dlg.showModal();
      doc.body.classList.add("is-locked");
    }
  };
  doc.querySelectorAll("[data-dialog-open]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      openDialog(btn.getAttribute("data-dialog-open"));
      if (history.replaceState) history.replaceState(null, "", "#" + btn.getAttribute("data-dialog-open").replace("bio-", ""));
    });
  });
  doc.querySelectorAll("dialog.bio-dialog").forEach(function (dlg) {
    dlg.addEventListener("close", function () {
      doc.body.classList.remove("is-locked");
      if (history.replaceState) history.replaceState(null, "", location.pathname + location.search);
    });
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) dlg.close();
    });
    dlg.querySelectorAll("[data-dialog-close]").forEach(function (b) {
      b.addEventListener("click", function () { dlg.close(); });
    });
  });
  if (location.hash && doc.getElementById("bio-" + location.hash.slice(1))) {
    openDialog("bio-" + location.hash.slice(1));
  }

  /* ---------- Legal page: active section in the table of contents ---------- */
  var tocLinks = doc.querySelectorAll(".legal-toc a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[a.getAttribute("href").slice(1)] = a; });
    var tocIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-active"); });
          var link = byId[entry.target.id];
          if (link) link.classList.add("is-active");
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(byId).forEach(function (id) {
      var sec = doc.getElementById(id);
      if (sec) tocIo.observe(sec);
    });
  }

  /* ---------- Contact form ---------- */
  var form = doc.querySelector("[data-contact-form]");
  if (form) {
    var params = new URLSearchParams(location.search);
    var matter = params.get("matter");
    var matterSelect = form.querySelector("#matter");
    if (matter && matterSelect && matterSelect.querySelector('option[value="' + matter + '"]')) {
      matterSelect.value = matter;
    }

    var alertBox = form.querySelector(".form-alert");
    var submitBtn = form.querySelector('button[type="submit"]');
    var success = doc.querySelector(".form-success");

    var messages = {
      first_name: "Please enter your first name.",
      last_name: "Please enter your last name.",
      email: "Please enter a valid email address.",
      phone: "Please enter your phone number.",
      matter: "Please choose the type of matter.",
      message: "Please tell us briefly what happened.",
      acknowledge: "Please confirm you have read this statement."
    };

    var fieldFor = function (input) { return input.closest(".field") || input.closest(".check-field"); };

    var validate = function (input) {
      var field = fieldFor(input);
      if (!field) return true;
      var valid = input.checkValidity();
      if (input.name === "phone" && valid && input.value.trim()) {
        valid = input.value.replace(/[^0-9]/g, "").length >= 7;
      }
      field.classList.toggle("has-error", !valid);
      input.setAttribute("aria-invalid", valid ? "false" : "true");
      var err = field.querySelector(".field-error span");
      if (err && !valid) err.textContent = messages[input.name] || "Please check this field.";
      return valid;
    };

    var inputs = form.querySelectorAll("input[required], select[required], textarea[required], input[type='tel']");
    inputs.forEach(function (input) {
      input.addEventListener("blur", function () { if (input.value || input.type === "checkbox") validate(input); });
      input.addEventListener("input", function () {
        if (fieldFor(input) && fieldFor(input).classList.contains("has-error")) validate(input);
      });
      input.addEventListener("change", function () {
        if (fieldFor(input) && fieldFor(input).classList.contains("has-error")) validate(input);
      });
    });

    var setBusy = function (busy) {
      submitBtn.setAttribute("aria-busy", busy ? "true" : "false");
      submitBtn.querySelector(".btn-label").textContent = busy ? "Sending" : "Send request";
    };

    var showSuccess = function (viaEmail) {
      form.hidden = true;
      if (success) {
        var variant = success.querySelector(viaEmail ? "[data-success-email]" : "[data-success-sent]");
        if (variant) variant.hidden = false;
        success.classList.add("is-visible");
        success.setAttribute("tabindex", "-1");
        success.focus();
      }
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      alertBox.classList.remove("is-visible");

      if (form.querySelector(".hp input") && form.querySelector(".hp input").value) return; // spam trap

      var firstInvalid = null;
      inputs.forEach(function (input) {
        if (!validate(input) && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) {
        alertBox.querySelector("span").textContent = "Please correct the highlighted fields and try again.";
        alertBox.classList.add("is-visible");
        firstInvalid.focus();
        return;
      }

      var data = new FormData(form);
      var endpoint = form.getAttribute("data-endpoint");

      if (!endpoint) {
        // No form service configured yet: hand the message to the visitor's email app.
        var to = form.getAttribute("data-email");
        var lines = [
          "Name: " + data.get("first_name") + " " + data.get("last_name"),
          "Email: " + data.get("email"),
          "Phone: " + data.get("phone"),
          "Matter: " + (matterSelect.options[matterSelect.selectedIndex] || {}).text,
          "Preferred contact: " + (data.get("contact_pref") || "Either"),
          "Urgent: " + (data.get("urgent") ? "Yes" : "No"),
          "",
          data.get("message")
        ];
        var href = "mailto:" + to + "?subject=" + encodeURIComponent("Consultation request: " + data.get("first_name") + " " + data.get("last_name")) +
          "&body=" + encodeURIComponent(lines.join("\n"));
        window.location.href = href;
        showSuccess(true);
        return;
      }

      setBusy(true);
      fetch(endpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("Request failed");
          showSuccess(false);
        })
        .catch(function () {
          alertBox.querySelector("span").textContent = "We couldn't send your message. Please try again, or call us directly.";
          alertBox.classList.add("is-visible");
        })
        .then(function () { setBusy(false); });
    });
  }

  /* ---------- Footer year ---------- */
  doc.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = String(new Date().getFullYear()); });
})();
