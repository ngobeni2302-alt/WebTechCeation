// Interactivity and animations
document.addEventListener('DOMContentLoaded', () => {
    // Theme toggling
    const themeButtons = document.querySelectorAll('.theme-toggle-btn');
    const currentTheme = localStorage.getItem('theme') || 'dark';

    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeButtons.forEach(btn => btn.textContent = '🌙');
    }

    themeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const isLight = document.documentElement.getAttribute('data-theme') === 'light';
            if (isLight) {
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'dark');
                themeButtons.forEach(b => b.textContent = '☀️');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
                themeButtons.forEach(b => b.textContent = '🌙');
            }
        });
    });

    // Header background change on scroll
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

    // Console greeting
    console.log('%cWEBHub Premium Loaded!', 'color: #64ffda; font-size: 1.2rem; font-weight: bold;');

    // Auth Logic
    const authOverlay = document.getElementById('authOverlay');
    const loginBox = document.getElementById('loginBox');
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    
    const logoutBtn = document.getElementById('logoutBtn');

    // Regex for: 8+ chars, 1 uppercase, 1 number, 1 special char (!#$&-.,)
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!#$&-.,])[A-Za-z\d!#$&-.,]{8,}$/;

    // Check session
    const checkSession = () => {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            authOverlay.classList.add('hidden');
            authOverlay.setAttribute('aria-hidden', 'true');
            setTimeout(() => { if(sessionStorage.getItem('isLoggedIn') === 'true') authOverlay.style.display = 'none'; }, 500);
        }
    };

    checkSession();

    // Admin Access Modal Button
    const adminAccessBtn = document.getElementById('adminAccessBtn');
    if(adminAccessBtn) {
        adminAccessBtn.addEventListener('click', (e) => {
            e.preventDefault();
            authOverlay.style.display = 'flex';
            setTimeout(() => { 
                authOverlay.classList.remove('hidden'); 
                authOverlay.setAttribute('aria-hidden', 'false');
            }, 10);
        });
    }

    const closeAuthBtn = document.getElementById('closeAuth');
    if(closeAuthBtn) {
        closeAuthBtn.addEventListener('click', () => {
            authOverlay.classList.add('hidden');
            authOverlay.setAttribute('aria-hidden', 'true');
            setTimeout(() => { authOverlay.style.display = 'none'; }, 500);
        });
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const ident = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ ident, password: pass })
            });
            const result = await response.json();
            
            if (result.success) {
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('currentUser', result.username);
                checkSession();
            } else {
                loginError.textContent = result.message;
            }
        } catch (error) {
            loginError.textContent = 'Error connecting to server.';
        }
    });

    logoutBtn.addEventListener('click', () => {
        sessionStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('currentUser');
        checkSession();
        
        // Reset forms
        loginForm.reset();
        loginError.textContent = '';
        
        // Ensure side menu closes
        sidePanel.classList.remove('open');
        sidePanel.setAttribute('aria-hidden', 'true');
        menuToggle.setAttribute('aria-expanded', 'false');
        overlay.classList.remove('visible');
    });

    // Password Visibility Toggle
    document.querySelectorAll('.password-toggle').forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.password-wrapper');
            const input = wrapper.querySelector('input');
            const isPassword = input.type === 'password';
            
            input.type = isPassword ? 'text' : 'password';
            button.classList.toggle('visible', isPassword);
            
            // Optional: update icon path to "eye-off"
            if (isPassword) {
                button.innerHTML = `
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
                        <line x1="1" y1="1" x2="23" y2="23"></line>
                    </svg>
                `;
            } else {
                button.innerHTML = `
                    <svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                    </svg>
                `;
            }
        });
    });
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
