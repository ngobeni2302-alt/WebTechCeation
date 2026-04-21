import os
import re

css_file = 'assets/css/style.css'
out_dir = 'src/scss'

os.makedirs(out_dir, exist_ok=True)

with open(css_file, 'r') as f:
    css_content = f.read()

# Very basic chunking based on comments
chunks = {
    '_variables.scss': '',
    '_base.scss': '',
    '_layout.scss': '',
    '_components.scss': '',
    '_auth.scss': '',
    '_theme.scss': '',
}

lines = css_content.split('\n')
current_file = '_variables.scss'

for line in lines:
    if line.startswith('/* Scrollbar */') or line.startswith('* {'):
        current_file = '_base.scss'
    elif line.startswith('/* Layout */'):
        current_file = '_layout.scss'
    elif line.startswith('/* Sections */') or line.startswith('/* Animations */') or line.startswith('/* Image Modal */') or line.startswith('/* --- Services & Team Grids --- */'):
        current_file = '_components.scss'
    elif line.startswith('/* Authentication Overlay */'):
        current_file = '_auth.scss'
    elif line.startswith('/* --- Custom Uiverse Theme Toggle --- */'):
        current_file = '_theme.scss'
    
    chunks[current_file] += line + '\n'

for filename, content in chunks.items():
    with open(os.path.join(out_dir, filename), 'w') as f:
        f.write(content)

with open(os.path.join(out_dir, 'main.scss'), 'w') as f:
    f.write('''@import 'variables';
@import 'base';
@import 'layout';
@import 'components';
@import 'auth';
@import 'theme';
''')

print("Split completed.")
