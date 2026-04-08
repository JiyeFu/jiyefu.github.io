document.addEventListener("DOMContentLoaded", function () {
  var revealTargets = document.querySelectorAll(".landing-hero, .section-card, .featured-paper");

  if (!revealTargets.length) {
    return;
  }

  revealTargets.forEach(function (element, index) {
    element.classList.add("reveal-on-scroll");
    element.style.transitionDelay = Math.min(index * 70, 360) + "ms";
  });

  if (!("IntersectionObserver" in window)) {
    revealTargets.forEach(function (element) {
      element.classList.add("is-visible");
    });
    return;
  }

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: "0px 0px -40px 0px"
  });

  revealTargets.forEach(function (element) {
    observer.observe(element);
  });
});
