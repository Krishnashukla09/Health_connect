let currentSlide = 0;
const slides = document.querySelectorAll(".slide");
const dots = document.querySelectorAll(".dot");

function showSlide(index) {
    // Hide all slides
    slides.forEach(slide => slide.classList.remove("active"));
    dots.forEach(dot => dot.classList.remove("active"));

    // Show the selected slide and activate the dot
    slides[index].classList.add("active");
    dots[index].classList.add("active");

    currentSlide = index;
}

// Auto-slide every 5 seconds
function autoSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
}

// Start the slider
document.addEventListener("DOMContentLoaded", () => {
    showSlide(0); // Show the first slide on load
    setInterval(autoSlide, 5000); // Change slide every 5s
});
