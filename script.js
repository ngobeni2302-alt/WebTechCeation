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
        sidePanel.classList.toggle('open');
        overlay.classList.toggle('visible');
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
            modalImage.src = img.src;
        });
    });

    closeModal.addEventListener('click', () => {
        imageModal.classList.remove('visible');
    });

    imageModal.addEventListener('click', (e) => {
        if (e.target === imageModal) {
            imageModal.classList.remove('visible');
        }
    });

    // Console greeting
    console.log('%cWEBHub Premium Loaded!', 'color: #64ffda; font-size: 1.2rem; font-weight: bold;');

    // Auth Logic
    const authOverlay = document.getElementById('authOverlay');
    const loginBox = document.getElementById('loginBox');
    const signupBox = document.getElementById('signupBox');
    
    const showSignupBtn = document.getElementById('showSignup');
    const showLoginBtn = document.getElementById('showLogin');
    
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');
    
    const loginError = document.getElementById('loginError');
    const signupError = document.getElementById('signupError');
    
    const logoutBtn = document.getElementById('logoutBtn');

    // Regex for: 8+ chars, 1 uppercase, 1 number, 1 special char (!#$&-.,)
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!#$&-.,])[A-Za-z\d!#$&-.,]{8,}$/;

    // Check session
    const checkSession = () => {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            authOverlay.classList.add('hidden');
            setTimeout(() => { if(sessionStorage.getItem('isLoggedIn') === 'true') authOverlay.style.display = 'none'; }, 500);
        } else {
            authOverlay.style.display = 'flex';
            setTimeout(() => { authOverlay.classList.remove('hidden'); }, 10);
        }
    };

    checkSession();

    showSignupBtn.addEventListener('click', () => {
        loginBox.classList.add('hidden');
        signupBox.classList.remove('hidden');
        loginError.textContent = '';
    });

    showLoginBtn.addEventListener('click', () => {
        signupBox.classList.add('hidden');
        loginBox.classList.remove('hidden');
        signupError.textContent = '';
    });

    signupForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = document.getElementById('signupUser').value.trim();
        const email = document.getElementById('signupEmail').value.trim();
        const pass = document.getElementById('signupPass').value;

        if (!passwordRegex.test(pass)) {
            signupError.textContent = 'Password does not meet requirements.';
            return;
        }

        const users = JSON.parse(localStorage.getItem('users') || '{}');
        
        // Check if username or email already exists
        if (users[user]) {
            signupError.textContent = 'Username already exists.';
            return;
        }
        
        const emailExists = Object.values(users).some(u => 
            (typeof u === 'object' && u.email === email) || (typeof u === 'string' && u === email)
        );
        if (emailExists) {
            signupError.textContent = 'Email already registered.';
            return;
        }

        // Store user with email and password
        users[user] = {
            pass: pass,
            email: email
        };
        localStorage.setItem('users', JSON.stringify(users));
        
        // Auto login (Session based)
        sessionStorage.setItem('isLoggedIn', 'true');
        sessionStorage.setItem('currentUser', user);
        checkSession();
    });

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const ident = document.getElementById('loginUser').value.trim();
        const pass = document.getElementById('loginPass').value;

        const users = JSON.parse(localStorage.getItem('users') || '{}');
        
        // Search by username or email
        let foundUser = null;
        let username = null;

        if (users[ident]) {
            foundUser = users[ident];
            username = ident;
        } else {
            // Check if 'ident' matches any user's email
            for (const [uname, udata] of Object.entries(users)) {
                if (typeof udata === 'object' && udata.email === ident) {
                    foundUser = udata;
                    username = uname;
                    break;
                }
            }
        }

        if (foundUser) {
            const storedPass = (typeof foundUser === 'object') ? foundUser.pass : foundUser;
            if (storedPass === pass) {
                sessionStorage.setItem('isLoggedIn', 'true');
                sessionStorage.setItem('currentUser', username);
                checkSession();
                return;
            }
        }
        
        loginError.textContent = 'Invalid username/email or password.';
    });

    logoutBtn.addEventListener('click', () => {
        sessionStorage.removeItem('isLoggedIn');
        sessionStorage.removeItem('currentUser');
        checkSession();
        
        // Reset forms
        loginForm.reset();
        signupForm.reset();
        loginError.textContent = '';
        signupError.textContent = '';
        
        // Ensure side menu closes
        sidePanel.classList.remove('open');
        overlay.classList.remove('visible');
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
