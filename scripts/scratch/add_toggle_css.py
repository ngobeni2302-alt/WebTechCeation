with open('assets/css/style.css', 'a', encoding='utf-8') as f:
    f.write("""
/* --- Custom Uiverse Theme Toggle --- */
.theme {
  display: flex;
  align-items: center;
  -webkit-tap-highlight-color: transparent;
  font-size: 8px; /* Resize relative to navbar */
  cursor: pointer;
  margin-top: 5px;
}

.theme__icon {
  transition: 0.3s;
}

.theme__icon,
.theme__toggle {
  z-index: 1;
}

.theme__icon,
.theme__icon-part {
  position: absolute;
}

.theme__icon {
  display: block;
  top: 0.5em;
  left: 0.5em;
  width: 1.5em;
  height: 1.5em;
}

/* Checked (Moon) - Default on Website */
.theme__icon-part {
  border-radius: 50%;
  box-shadow: 0.4em -0.4em 0 0.5em var(--base-dark) inset;
  top: calc(50% - 0.5em);
  left: calc(50% - 0.5em);
  width: 1em;
  height: 1em;
  transition: box-shadow 0.3s ease-in-out, opacity 0.3s ease-in-out, transform 0.3s ease-in-out;
  transform: scale(0.5);
}

/* Sun Rays */
.theme__icon-part ~ .theme__icon-part {
  background-color: var(--base-dark);
  border-radius: 0.05em;
  top: 50%;
  left: calc(50% - 0.05em);
  transform: rotate(0deg) translateY(0.5em);
  transform-origin: 50% 0;
  width: 0.1em;
  height: 0.2em;
}

.theme__icon-part:nth-child(3) { transform: rotate(45deg) translateY(0.45em); }
.theme__icon-part:nth-child(4) { transform: rotate(90deg) translateY(0.45em); }
.theme__icon-part:nth-child(5) { transform: rotate(135deg) translateY(0.45em); }
.theme__icon-part:nth-child(6) { transform: rotate(180deg) translateY(0.45em); }
.theme__icon-part:nth-child(7) { transform: rotate(225deg) translateY(0.45em); }
.theme__icon-part:nth-child(8) { transform: rotate(270deg) translateY(0.5em); }
.theme__icon-part:nth-child(9) { transform: rotate(315deg) translateY(0.5em); }

.theme__toggle-wrap {
  position: relative;
  margin: 0;
}

/* Unchecked State (Sun / Light Mode) */
.theme__toggle {
  display: block;
  background-color: var(--border-subtle);
  border-radius: 1.5em;
  box-shadow: 0 0 0 0.125em transparent;
  padding: 0.25em;
  width: 6em;
  height: 3em;
  -webkit-appearance: none;
  appearance: none;
  transition: background-color 0.3s ease-in-out, box-shadow 0.15s ease-in-out, transform 0.3s ease-in-out;
  cursor: pointer;
}

.theme__toggle:before {
  display: block;
  background-color: var(--accent-highlight); /* Sun core */
  border-radius: 50%;
  content: "";
  width: 2.5em;
  height: 2.5em;
  transition: 0.3s;
}

.theme__toggle:focus {
  box-shadow: 0 0 0 0.125em var(--accent-highlight);
  outline: transparent;
}

/* Checked State (Moon / Dark Mode) */
.theme__toggle:checked {
  background-color: var(--base-light);
}

.theme__toggle:checked:before,
.theme__toggle:checked ~ .theme__icon {
  transform: translateX(3em);
}

.theme__toggle:checked:before {
  background-color: var(--text-main); /* Moon base */
}

/* Internal Moon Crescent Cut Out Shadow */
.theme__toggle:checked ~ .theme__icon .theme__icon-part:nth-child(1) {
  box-shadow: 0.2em -0.2em 0 0.2em var(--base-light) inset; /* Blend into pill background */
  transform: scale(1);
  top: 0.2em;
  left: -0.2em;
}

.theme__toggle:checked ~ .theme__icon .theme__icon-part ~ .theme__icon-part {
  opacity: 0; /* Hide rays */
}
""")
