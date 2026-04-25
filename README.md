# Ntsako

A premium, dark navy-themed web experience built with highly modern modular code structure, powered by a secure FastAPI backend. 

## 🚀 Features

- **Responsive Design**: Flawlessly adapts to desktop, tablet, and mobile viewing.
- **Theme Toggling**: Uiverse animated theme toggle for switching between dark and light modes.
- **Modular JavaScript**: Clean, ES-Module architecture avoiding monolithic scripts.
- **Performance Optimized**: No external node modules needed for deployment. Just static files with lightweight Python backend for Auth!

## 📂 Project Structure

We value clean and manageable code, dividing our resources so they are easy to navigate and extend.

```
WebTechCeation/
├── index.html               # Main entry point for the frontend
├── README.md                # Project documentation
├── backend/                 # Backend APIs and Server Logic
│   ├── main.py              # FastAPI server, JWT auth, and routing
│   ├── requirements.txt     # Python dependencies
│   └── users.db             # SQLite database
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

### 1. Running the Server

Since this project utilizes ES Modules (`<script type="module">`), you **must** serve it using a local web server to avoid CORS issues.

Fortunately, we provide a convenient script to start the server and automatically open the application in your default web browser. Run the following command from the root directory:

```bash
bash scripts/open_web.sh
```

Alternatively, you can manually start the FastAPI backend from the `backend` directory. First install the requirements:

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```
*(After starting it, the API will be available at `http://localhost:8000`. You can test endpoints via the Swagger UI at `http://localhost:8000/docs`.)*

## 🚀 Backend Architecture Upgrade (FastAPI)

- **FastAPI Framework**: Migrated from a basic `http.server` to FastAPI for automatic Pydantic validation and asynchronous request handling.
- **Secure Authentication**: Replaced basic JSON payload login with an OAuth2-compliant form data submission.
- **JWT Protection**: Integrated a `get_current_user` dependency to ensure protected routes (like `/bookings` and `/bookings/me`) are securely locked with JSON Web Tokens.
- **Frontend Sync**: The frontend `auth.js` automatically handles token storage in `sessionStorage` and attaches it to authenticated requests.

### 2. SCSS to CSS 

If you wish to modify the styles, we highly recommend modifying the SCSS files in the `src/scss/` directory. You can use any simple compiler like the **Live Sass Compiler** extension in VSCode to output to `assets/css/main.css`. No complex `node_modules` or build chains are required!

---
> Created by TechMINDS for the People.
