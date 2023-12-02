document.addEventListener("DOMContentLoaded", function () {
    console.log("DOMContentLoaded event fired");

    const sections = document.querySelectorAll(".section");

    window.addEventListener("scroll", function () {
        console.log("Scroll event fired");

        let currentSection = "";

        sections.forEach(function (section) {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (pageYOffset >= sectionTop - sectionHeight / 2) {
                currentSection = section.getAttribute("id");
            }
        });

        console.log("Current Section:", currentSection);

        setActiveNav(currentSection);
    });

    function setActiveNav(currentSection) {
        console.log("Setting active nav for section:", currentSection);

        const navLinks = document.querySelectorAll("nav a");

        navLinks.forEach(function (link) {
            link.classList.remove("active");
            if (link.getAttribute("href").slice(1) === currentSection) {
                link.classList.add("active");
            }
        });
    }
});
