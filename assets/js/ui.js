export function initUI() {
    // Smooth reveal for scroll animations
    const observerOptions = {
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Add visible class in CSS for reveal effect
    document.querySelectorAll('.animate').forEach(el => {
        observer.observe(el);
    });

    // Image Modal Logic
    const imageModal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const closeModal = document.getElementById('closeModal');

    if(imageModal && modalImage && closeModal) {
        document.querySelectorAll('.clickable-image').forEach(img => {
            img.addEventListener('click', () => {
                imageModal.classList.add('visible');
                imageModal.setAttribute('aria-hidden', 'false');
                modalImage.src = img.src;
            });
        });

        closeModal.addEventListener('click', () => {
            imageModal.classList.remove('visible');
            imageModal.setAttribute('aria-hidden', 'true');
        });

        imageModal.addEventListener('click', (e) => {
            if (e.target === imageModal) {
                imageModal.classList.remove('visible');
                imageModal.setAttribute('aria-hidden', 'true');
            }
        });
    }

    // Console greeting
    console.log('%cWEBHub Premium Loaded!', 'color: #64ffda; font-size: 1.2rem; font-weight: bold;');
}
