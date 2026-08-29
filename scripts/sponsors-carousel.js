const carousel = document.querySelector("[data-sponsor-carousel]");

if (carousel) {
  const controls = document.querySelector("[data-carousel-controls]");
  const previous = controls?.querySelector("[data-carousel-previous]");
  const next = controls?.querySelector("[data-carousel-next]");

  const cardStep = () => {
    const firstCard = carousel.querySelector(".sponsor-card");
    const gap = Number.parseFloat(getComputedStyle(carousel).columnGap) || 0;
    return firstCard ? firstCard.getBoundingClientRect().width + gap : carousel.clientWidth;
  };

  const updateControls = () => {
    const maximum = carousel.scrollWidth - carousel.clientWidth;
    const hasOverflow = maximum > 1;

    if (controls) controls.hidden = !hasOverflow;
    if (previous) previous.disabled = carousel.scrollLeft <= 1;
    if (next) next.disabled = carousel.scrollLeft >= maximum - 1;
  };

  previous?.addEventListener("click", () => {
    carousel.scrollBy({ left: -cardStep(), behavior: "smooth" });
  });

  next?.addEventListener("click", () => {
    carousel.scrollBy({ left: cardStep(), behavior: "smooth" });
  });

  carousel.addEventListener("scroll", updateControls, { passive: true });
  window.addEventListener("resize", updateControls);
  updateControls();
}
