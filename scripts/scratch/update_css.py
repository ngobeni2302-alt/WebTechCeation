import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace('--bg-deep', '--base-dark')
css = css.replace('--bg-light', '--base-light')
css = css.replace('--navy-blue', '--border-subtle')
css = css.replace('--text-primary', '--text-main')
css = css.replace('--text-secondary', '--text-muted')
css = css.replace('--accent-blue', '--accent-highlight')
css = css.replace('--font-main: \'Inter\'', '--font-main: \'Outfit\'')

css = re.sub(r':root\s*\{[^}]+\}', ''':root {
    /* High-Contrast Orange/Black Palette */
    --base-dark: #000000;
    --base-light: #111111;
    --border-subtle: #333333;
    --text-main: #FFFFFF;
    --text-muted: #AAAAAA;
    --accent-highlight: #FF9800; 
    --accent-glow: rgba(255, 152, 0, 0.1);
    
    --nav-bg: rgba(0, 0, 0, 0.85);
    --overlay-bg: rgba(0, 0, 0, 0.7);
    --hero-overlay: rgba(0, 0, 0, 0.8);
    --card-border: rgba(255, 255, 255, 0.05);
    --modal-bg: rgba(0, 0, 0, 0.95);
    --hero-text-start: #FFFFFF;
    
    --transition: all 0.3s cubic-bezier(0.645, 0.045, 0.355, 1);
    --font-main: 'Outfit', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}''', css, count=1)

css = re.sub(r'\[data-theme="light"\]\s*\{[^}]+\}', '''[data-theme="light"] {
    --base-dark: #FFFFFF;
    --base-light: #F5F5F5;
    --border-subtle: #CCCCCC;
    --text-main: #000000;
    --text-muted: #555555;
    --accent-highlight: #FF9800;
    --accent-glow: rgba(255, 152, 0, 0.2);
    
    --nav-bg: rgba(255, 255, 255, 0.85);
    --overlay-bg: rgba(0, 0, 0, 0.3);
    --hero-overlay: rgba(255, 255, 255, 0.85);
    --card-border: rgba(0, 0, 0, 0.1);
    --modal-bg: rgba(255, 255, 255, 0.95);
    --hero-text-start: #000000;
}''', css, count=1)

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
