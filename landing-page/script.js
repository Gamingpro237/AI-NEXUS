
document.addEventListener("DOMContentLoaded", function () {
    const sections = document.querySelectorAll("section");

    const options = {
        threshold: 0.3,
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("fade-in");
            }
        });
    }, options);

    sections.forEach(section => {
        section.classList.add("fade-out");
        observer.observe(section);
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".card");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("fade-in");
            }
        });
    }, { threshold: 0.3 });

    steps.forEach(step => {
        step.classList.add("fade-out");
        observer.observe(step);
    });
});

