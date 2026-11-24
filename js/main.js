"use strict";

/* Photos: until a real image file is added in /images, show a soft
   placeholder with the expected file name instead of a broken image. */
function watchPhoto(img) {
  const frame = img.closest(".photo");
  if (!frame) return;

  const markEmpty = () => frame.classList.add("is-empty");
  const markLoaded = () => frame.classList.remove("is-empty");

  if (img.complete) {
    if (img.naturalWidth === 0) markEmpty();
  }
  img.addEventListener("error", markEmpty);
  img.addEventListener("load", markLoaded);
}

document.querySelectorAll(".photo img").forEach(watchPhoto);

/* Respect "reduce motion": keep looping videos on their first frame. */
if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  document.querySelectorAll("video[autoplay]").forEach((video) => {
    video.removeAttribute("autoplay");
    video.pause();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  /* Mobile menu */
  const menuButton = document.querySelector("[data-menu-toggle]");
  const navigation = document.querySelector("[data-navigation]");

  if (menuButton && navigation) {
    const setOpen = (open) => {
      navigation.classList.toggle("is-open", open);
      menuButton.setAttribute("aria-expanded", String(open));
    };

    menuButton.addEventListener("click", () => {
      setOpen(menuButton.getAttribute("aria-expanded") !== "true");
    });

    navigation.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", () => setOpen(false));
    });

    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && navigation.classList.contains("is-open")) {
        setOpen(false);
        menuButton.focus();
      }
    });

    window.matchMedia("(min-width: 72rem)").addEventListener("change", (event) => {
      if (event.matches) setOpen(false);
    });
  }

  /* Header border once the page is scrolled */
  const header = document.querySelector(".site-header");
  if (header) {
    const update = () => header.classList.toggle("is-scrolled", window.scrollY > 8);
    update();
    window.addEventListener("scroll", update, { passive: true });
  }

  /* Current year in the footer */
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = new Date().getFullYear();
  });
});
