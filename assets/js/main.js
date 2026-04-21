import { initTheme } from './theme.js';
import { initNav } from './nav.js';
import { initUI } from './ui.js';
import { initAuth } from './auth.js';

document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initNav();
    initUI();
    initAuth();
});
