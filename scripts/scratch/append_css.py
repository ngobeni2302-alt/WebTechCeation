with open('assets/css/style.css', 'a', encoding='utf-8') as f:
    f.write('''\n/* --- Services & Team Grids --- */
.services-grid, .team-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

@media (min-width: 1024px) {
    .services-grid, .team-grid {
        grid-template-columns: repeat(4, 1fr);
    }
}

/* Text Card Base */
.text-card {
    background: var(--base-dark);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    border-top: 4px solid transparent; 
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 250px;
    transition: var(--transition);
    overflow: hidden;
}

.text-card h3 {
    margin-bottom: 1rem;
    font-size: 1.25rem;
    color: var(--text-main);
    transition: var(--transition);
}

/* Hidden Content */
.text-card .card-content {
    opacity: 0;
    max-height: 0;
    transition: all 0.4s ease;
    overflow: hidden;
}

.text-card p {
    color: var(--text-muted);
    font-size: 0.95rem;
}

/* Arrow Container Default */
.text-card .arrow-container {
    margin-top: auto;
    align-self: flex-start; /* Bottom Left */
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    color: var(--text-muted);
    background: transparent;
    transition: var(--transition);
}

.text-card .arrow-container i {
    font-size: 1rem;
    transition: var(--transition);
}

/* Text Card Hover States */
.text-card:hover {
    border-top: 4px solid var(--accent-highlight);
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.text-card:hover .card-content {
    opacity: 1;
    max-height: 150px; /* Expands to reveal */
    margin-bottom: 2rem;
}

.text-card:hover .arrow-container {
    background: var(--accent-highlight);
    color: #000000; /* Black arrow */
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

/* Team Card */
.team-card {
    background: var(--base-light);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid var(--border-subtle);
    text-align: center;
    transition: var(--transition);
}

.team-card:hover {
    border-color: var(--accent-highlight);
    transform: translateY(-5px);
}

.team-card h3 {
    color: var(--text-main);
    margin-bottom: 0.5rem;
}

.team-card .role {
    color: var(--text-muted);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.team-card .email {
    color: var(--accent-highlight);
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
}

.team-card .email:hover {
    text-decoration: underline;
}
''')
