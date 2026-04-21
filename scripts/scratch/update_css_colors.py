import re

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace colors
css = css.replace('#FF9800', '#32CD32')
css = css.replace('rgba(255, 152, 0, 0.1)', 'rgba(50, 205, 50, 0.1)')
css = css.replace('rgba(255, 152, 0, 0.2)', 'rgba(50, 205, 50, 0.2)')

# Replace animation logic for text-card
old_slider_logic = """/* Hidden Content */
.text-card .card-content {
    opacity: 0;
    max-height: 0;
    transition: all 0.4s ease;
    overflow: hidden;
}"""

new_slider_logic = """/* Hidden Content */
.text-card .card-content {
    opacity: 0;
    max-height: 0;
    margin-bottom: 0;
    transition: max-height 0.6s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.6s cubic-bezier(0.4, 0, 0.2, 1), margin-bottom 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    overflow: hidden;
}"""
css = css.replace(old_slider_logic, new_slider_logic)

old_hover_logic = """.text-card:hover .card-content {
    opacity: 1;
    max-height: 150px; /* Expands to reveal */
    margin-bottom: 2rem;
}"""

new_hover_logic = """.text-card:hover .card-content {
    opacity: 1;
    max-height: 180px; /* Fully expands to reveal smoothly without clashing */
    margin-bottom: 1.5rem;
}"""
css = css.replace(old_hover_logic, new_hover_logic)

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)
