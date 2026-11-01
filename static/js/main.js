// Небольшие улучшения интерфейса. Без них сайт тоже полностью работает:
// карточки видны, ссылки открываются, меню доступно.

const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealItems = document.querySelectorAll("[data-reveal]");

// 1. Плавное появление карточек при прокрутке.
// Класс js добавляем только когда анимация действительно возможна.
if (prefersReducedMotion || !("IntersectionObserver" in window)) {
  revealItems.forEach((item) => item.classList.add("is-visible"));
} else {
  document.documentElement.classList.add("js");

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  revealItems.forEach((item) => revealObserver.observe(item));
}

// 2. Анимированный чип в ядре hero: видео вместо статичной надписи.
const coreVideo = document.querySelector(".core-video");

if (coreVideo) {
  const core = coreVideo.closest(".core");

  const showCorePoster = () => {
    coreVideo.pause();
    core?.classList.add("is-static");
  };

  if (prefersReducedMotion || !coreVideo.canPlayType("video/mp4")) {
    showCorePoster();
  } else {
    coreVideo.muted = true;
    coreVideo.playsInline = true;

    const playCoreVideo = () => {
      coreVideo
        .play()
        .then(() => core?.classList.remove("is-static"))
        .catch(showCorePoster);
    };

    playCoreVideo();

    // По правилу бренда перезапускаем ролик каждые 30 секунд.
    window.setInterval(() => {
      if (!document.hidden && !coreVideo.paused && !core?.classList.contains("is-static")) {
        try {
          coreVideo.currentTime = 0;
        } catch {
          showCorePoster();
        }
      }
    }, 30000);

    document.addEventListener("visibilitychange", () => {
      if (document.hidden) {
        coreVideo.pause();
      } else if (!core?.classList.contains("is-static")) {
        playCoreVideo();
      }
    });
  }

  coreVideo.addEventListener("error", showCorePoster);
}

// 3. Подсветка активного пункта меню при прокрутке главной страницы.
const navLinks = document.querySelectorAll("[data-nav]");
const sections = [...document.querySelectorAll("main section[id]")];

function setActiveNav(sectionId) {
  navLinks.forEach((link) => {
    const isActive = link.dataset.nav === sectionId;
    link.classList.toggle("is-active", isActive);
    if (isActive) {
      link.setAttribute("aria-current", "true");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

if (sections.length > 0) {
  let scrollFrame = null;

  const updateActiveNav = () => {
    const headerHeight = document.querySelector(".site-header")?.offsetHeight || 0;
    const marker = window.scrollY + headerHeight + 90;
    let current = "digest";

    sections.forEach((section) => {
      if (section.offsetTop <= marker) {
        current = section.id;
      }
    });

    setActiveNav(current);
    scrollFrame = null;
  };

  const requestActiveNavUpdate = () => {
    if (scrollFrame === null) {
      scrollFrame = window.requestAnimationFrame(updateActiveNav);
    }
  };

  window.addEventListener("scroll", requestActiveNavUpdate, { passive: true });
  window.addEventListener("resize", requestActiveNavUpdate);
  updateActiveNav();
} else {
  // На странице материала разделов нет, поэтому отмечаем «Дайджест» вручную.
  setActiveNav("digest");
}

// 4. Тень у шапки после начала прокрутки.
const header = document.querySelector(".site-header");

if (header) {
  const updateHeader = () => {
    header.classList.toggle("is-scrolled", window.scrollY > 8);
  };

  window.addEventListener("scroll", updateHeader, { passive: true });
  updateHeader();
}

// 5. Мягкое свечение, которое следует за курсором в первом экране.
const hero = document.querySelector(".hero");
const finePointer = window.matchMedia("(pointer: fine)");

if (hero && finePointer.matches && !prefersReducedMotion) {
  hero.addEventListener("pointermove", (event) => {
    const rect = hero.getBoundingClientRect();
    const x = ((event.clientX - rect.left) / rect.width) * 100;
    const y = ((event.clientY - rect.top) / rect.height) * 100;

    hero.style.setProperty("--pointer-x", `${x}%`);
    hero.style.setProperty("--pointer-y", `${y}%`);
    hero.classList.add("has-pointer");
  });

  hero.addEventListener("pointerleave", () => {
    hero.classList.remove("has-pointer");
  });
}
