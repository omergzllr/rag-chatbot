// Hamburger menu
document.getElementById('hamburger')?.addEventListener('click', () => {
    document.getElementById('mobileMenu').classList.toggle('open');
});

// Counter animation
document.querySelectorAll('.stat-number[data-target]').forEach(el => {
    const target = parseInt(el.dataset.target);
    let count = 0;
    const step = Math.ceil(target / 50);
    const timer = setInterval(() => {
        count = Math.min(count + step, target);
        el.textContent = count + '+';
        if (count >= target) clearInterval(timer);
    }, 30);
});

// Scroll animations
const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.style.opacity = '1';
            e.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.feature-card, .about-card, .contact-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});
