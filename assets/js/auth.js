export function initAuth() {
    const authOverlay = document.getElementById('authOverlay');
    const loginBox = document.getElementById('loginBox');
    const loginForm = document.getElementById('loginForm');
    const loginError = document.getElementById('loginError');
    const logoutBtn = document.getElementById('logoutBtn');
    const sidePanel = document.getElementById('sidePanel');
    const menuToggle = document.getElementById('menuToggle');
    const overlay = document.getElementById('overlay');

    // Check session
    const checkSession = () => {
        if (sessionStorage.getItem('isLoggedIn') === 'true') {
            authOverlay.classList.add('hidden');
            authOverlay.setAttribute('aria-hidden', 'true');
            setTimeout(() => { if(sessionStorage.getItem('isLoggedIn') === 'true') authOverlay.style.display = 'none'; }, 500);
        }
    };

    if (authOverlay && loginBox) {
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

        if (loginForm) {
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
        }
    }

    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            sessionStorage.removeItem('isLoggedIn');
            sessionStorage.removeItem('currentUser');
            checkSession();
            
            // Reset forms
            if (loginForm) loginForm.reset();
            if (loginError) loginError.textContent = '';
            
            // Ensure side menu closes
            if (sidePanel) {
                sidePanel.classList.remove('open');
                sidePanel.setAttribute('aria-hidden', 'true');
            }
            if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
            if (overlay) overlay.classList.remove('visible');
        });
    }

    // Password Visibility Toggle
    document.querySelectorAll('.password-toggle').forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.password-wrapper');
            const input = wrapper.querySelector('input');
            const isPassword = input.type === 'password';
            
            input.type = isPassword ? 'text' : 'password';
            button.classList.toggle('visible', isPassword);
            
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
}
