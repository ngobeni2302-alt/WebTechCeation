export function initNav() {
    const nav = document.querySelector('nav');
    const menuToggle = document.getElementById('menuToggle');
    const sidePanel = document.getElementById('sidePanel');
    const overlay = document.getElementById('overlay');

    const toggleMenu = () => {
        const isOpen = sidePanel.classList.toggle('open');
        overlay.classList.toggle('visible');
        menuToggle.setAttribute('aria-expanded', isOpen);
        sidePanel.setAttribute('aria-hidden', !isOpen);
    };

    menuToggle.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', toggleMenu);

    // Close side panel on link click
    document.querySelectorAll('.side-panel a').forEach(link => {
        link.addEventListener('click', toggleMenu);
    });

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.padding = '1rem 10%';
            nav.style.boxShadow = '0 10px 30px -10px rgba(0, 0, 0, 0.5)';
        } else {
            nav.style.padding = '1.5rem 10%';
            nav.style.boxShadow = 'none';
        }
    });

    // Smooth jump to sections
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
}
