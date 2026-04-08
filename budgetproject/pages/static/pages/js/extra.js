document.addEventListener("DOMContentLoaded", function () {
    const bars = document.querySelectorAll(".progress-bar");

    bars.forEach(bar => {
        let progress = parseFloat(bar.dataset.progress) || 0;

        // cap at 100%
        if (progress > 100) progress = 100;

        const text = bar.parentElement.querySelector(".progress-text");

        // color logic
        if (progress < 70) {
            bar.style.backgroundColor = "#16a34a"; // green
        } else if (progress < 100) {
            bar.style.backgroundColor = "#f59e0b"; // orange
        } else {
            bar.style.backgroundColor = "#dc2626"; // red
        }



        // animate
        setTimeout(() => {
            bar.style.width = progress + "%";
        }, 100);

        let start = 0;
        let duration = 800;
        let increment = progress / (duration / 16);
        function animateCounter() {
            start += (progress - start) * 0.1;

            if (start >= progress) {
                start = progress;
            }
            text.innerText = Math.round(start) + "%"
            if (start < progress) {
                requestAnimationFrame(animateCounter);
            }
        }
        animateCounter();
    });
});

console.log("extra.js loaded");


const nav = document.querySelector('.ozel');

// Restore scroll position on page load
document.addEventListener('DOMContentLoaded', () => {
    const savedScroll = localStorage.getItem('ozelScroll');
        if (savedScroll && nav) {
            nav.scrollLeft = parseInt(savedScroll);
        }
        });

// Save scroll position before leaving page
        if (nav) {
            nav.addEventListener('scroll', () => {
            localStorage.setItem('ozelScroll', nav.scrollLeft);
        });
}

