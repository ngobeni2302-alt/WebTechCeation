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
        document.addEventListener('click', (event) => {
            const img = event.target.closest('.clickable-image');

            if (img) {
                imageModal.classList.add('visible');
                imageModal.setAttribute('aria-hidden', 'false');
                modalImage.src = img.src;
                modalImage.alt = img.alt;
            }
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

    // Get A Quote Form Logic
    const quoteForm = document.getElementById('quoteForm');
    const quoteSuccess = document.getElementById('quoteSuccessMessage');
    const projectTypeInput = document.getElementById('projectTypeInput');
    const optionCards = document.querySelectorAll('.quote-option-card');

    if (quoteForm && quoteSuccess && projectTypeInput && optionCards.length > 0) {
        optionCards.forEach(card => {
            card.addEventListener('click', () => {
                optionCards.forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                projectTypeInput.value = card.getAttribute('data-value');
            });
        });

        quoteForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const projectType = projectTypeInput.value;
            const dueDate = document.getElementById('dueDate').value;
            const description = document.getElementById('dreamDescription').value;
            const email = document.getElementById('quoteEmail').value;
            const phone = document.getElementById('quotePhone').value;

            if (!projectType) {
                alert('Please select what you want (Website, App, or Design)!');
                return;
            }

            try {
                const response = await fetch('/api/quotes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        project_type: projectType,
                        due_date: dueDate,
                        description: description,
                        email: email,
                        phone: phone
                    })
                });

                if (response.ok) {
                    quoteForm.style.display = 'none';
                    quoteSuccess.classList.remove('hidden');
                } else {
                    const data = await response.json();
                    alert('Error: ' + (data.detail || 'Failed to submit quote request'));
                }
            } catch (err) {
                console.error(err);
                alert('Network error, please try again later.');
            }
        });
    }

    // Console greeting
    console.log('%cWEBHub Premium Loaded!', 'color: #64ffda; font-size: 1.2rem; font-weight: bold;');
}

