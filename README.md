# WEBHub Premium Web Design

A premium, dark navy-themed web experience built with highly modern modular code structure. 

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
│   ├── server.py            # Python server and SQLite database handler
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

### 1. Running the Server

Since this project utilizes ES Modules (`<script type="module">`), you **must** serve it using a local web server to avoid CORS issues.

Fortunately, we have a custom Python backend that handles this for you:

```bash
cd backend
python server.py
```
*Note: Make sure to run `server.py` from the root directory if you want it to serve the `index.html` from the root, or adjust the path in the python file.*

To run from the root directory:
```bash
python backend/server.py
```

### 2. SCSS to CSS 

If you wish to modify the styles, we highly recommend modifying the SCSS files in the `src/scss/` directory. You can use any simple compiler like the **Live Sass Compiler** extension in VSCode to output to `assets/css/main.css`. No complex `node_modules` or build chains are required!

---
> Created by TechMINDS for the People.
