# WEBHub Premium Web Design

A premium, dark navy-themed web experience built with highly modern modular code structure. 

## 🚀 Features

- **Responsive Design**: Flawlessly adapts to desktop, tablet, and mobile viewing.
- **Theme Toggling**: Uiverse animated theme toggle for switching between dark and light modes.
- **Modular JavaScript**: Clean, ES-Module architecture avoiding monolithic scripts.
- **ORM Powered Backend**: Modernized Python backend using SQLAlchemy for robust database management.
- **Performance Optimized**: Lightweight and efficient static file serving with secure Auth handling.

## 📂 Project Structure

We value clean and manageable code, dividing our resources so they are easy to navigate and extend.

```
WebTechCeation/
├── index.html               # Main entry point for the frontend
├── README.md                # Project documentation
├── backend/                 # Backend APIs and Server Logic
│   ├── server.py            # Python server (HTTP API)
│   ├── models.py            # SQLAlchemy Database Models
│   ├── database.py          # SQLAlchemy Engine & Session Configuration
│   ├── init_db.py           # Database Initialization Script
│   └── users.db             # SQLite database for admin access
├── src/                     # Source files
│   └── scss/                # SCSS partials (variables, components, layout)
└── assets/                  # Public web assets served to the client
    ├── css/
    │   └── main.css         # Main stylesheet 
    ├── js/
    │   ├── main.js          # Main ES Module entry
    │   ├── auth.js          # Authentication logic
    │   ├── nav.js           # Navigation logic and smooth scroll
    │   ├── theme.js         # Theme toggle logic
    │   └── ui.js            # UI Modals and Animations
    └── images/              # Image assets
```

## 🛠 Getting Started

### 1. Backend Setup

This project uses SQLAlchemy for database management. Ensure you have the required dependencies installed:

```bash
# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install sqlalchemy psycopg2-binary
```

### 2. Running the Server

Since this project utilizes ES Modules (`<script type="module">`), you **must** serve it using a local web server to avoid CORS issues.

Fortunately, we provide a convenient script to start the server and automatically open the application in your default web browser. Run the following command from the root directory:

```bash
bash scripts/open_web.sh
```

Alternatively, you can manually start the custom Python backend from the root directory:

```bash
python3 backend/server.py
```
*(After starting it manually, you will need to open `http://localhost:8080` in your web browser.)*

### 3. SCSS to CSS 

If you wish to modify the styles, we highly recommend modifying the SCSS files in the `src/scss/` directory. You can use any simple compiler like the **Live Sass Compiler** extension in VSCode to output to `assets/css/main.css`. No complex `node_modules` or build chains are required!

---
> Created by TechMINDS for the People.
