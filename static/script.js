const chips = document.querySelectorAll(".chip");
const cards = document.querySelectorAll("#property-list li");

chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
        chips.forEach(function (c) {
            c.classList.remove("active");
        });
        chip.classList.add("active");

        const filter = chip.getAttribute("data-filter");

        cards.forEach(function (card) {
            if (filter === "all" || card.getAttribute("data-area") === filter) {
                card.style.display = "";
            } else {
                card.style.display = "none";
            }
        });
    });
});

const stars = document.querySelectorAll("#star-input i");
const ratingInput = document.getElementById("rating-value");

stars.forEach(function (star) {
    star.addEventListener("click", function () {
        const value = star.getAttribute("data-value");
        ratingInput.value = value;

        stars.forEach(function (s) {
            if (s.getAttribute("data-value") <= value) {
                s.classList.add("selected");
                s.classList.remove("ti-star");
                s.classList.add("ti-star-filled");
            } else {
                s.classList.remove("selected");
                s.classList.remove("ti-star-filled");
                s.classList.add("ti-star");
            }
        });
    });
});

const reviewTexts = document.querySelectorAll(".review-text");

reviewTexts.forEach(function (text) {
    const button = text.nextElementSibling;

    if (text.scrollHeight > text.clientHeight) {
        button.style.display = "inline";
    }

    button.addEventListener("click", function () {
        text.classList.toggle("expanded");
        button.textContent = text.classList.contains("expanded") ? "Read less" : "Read more";
    });
});