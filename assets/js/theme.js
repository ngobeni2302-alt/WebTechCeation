export function initTheme() {
    const themeButtons = document.querySelectorAll('.theme__toggle');
    const currentTheme = localStorage.getItem('theme') || 'dark';

    if (currentTheme === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        themeButtons.forEach(btn => btn.checked = false); // Unchecked is light mode
    } else {
        themeButtons.forEach(btn => btn.checked = true); // Checked is dark mode
    }

    themeButtons.forEach(btn => {
        btn.addEventListener('change', (e) => {
            const isDark = e.target.checked;
            if (!isDark) {
                // Switch to light
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            } else {
                // Switch to dark
                document.documentElement.removeAttribute('data-theme');
                localStorage.setItem('theme', 'dark');
            }
            
            // Sync all toggles
            themeButtons.forEach(b => {
                if(b !== e.target) b.checked = e.target.checked;
            });
        });
    });
}
