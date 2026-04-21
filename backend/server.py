import http.server
import json
import os
import sqlite3
import hashlib

PORT = 8080
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "users.db")

# Part 2: Database Modernization (SQLite)
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def hash_password(password):
    # Securely store passwords using SHA-256
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class AuthHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/signup':
            self.handle_signup()
        elif self.path == '/api/login':
            self.handle_login()
        else:
            self.send_error(404, "Not Found")

    def get_post_data(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode('utf-8'))

    def handle_signup(self):
        try:
            data = self.get_post_data()
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                self.send_response_json({"success": False, "message": "Missing required fields"}, 400)
                return

            password_hash = hash_password(password)

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            try:
                # Use parameterization (?) to prevent SQL injection
                cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                             (username, email, password_hash))
                conn.commit()
                self.send_response_json({"success": True, "message": "User created successfully"})
            except sqlite3.IntegrityError as e:
                # Since we have UNIQUE constraints, IntegrityError spots duplicates
                if 'username' in str(e).lower() or 'users.username' in str(e).lower():
                    self.send_response_json({"success": False, "message": "Username already exists"}, 400)
                elif 'email' in str(e).lower() or 'users.email' in str(e).lower():
                    self.send_response_json({"success": False, "message": "Email already exists"}, 400)
                else:
                    self.send_response_json({"success": False, "message": "Database error"}, 500)
            finally:
                conn.close()
                
        except Exception as e:
            self.send_response_json({"success": False, "message": str(e)}, 500)

    def handle_login(self):
        try:
            data = self.get_post_data()
            ident = data.get('ident')
            password = data.get('password')

            if not ident or not password:
                self.send_response_json({"success": False, "message": "Missing credentials"}, 400)
                return

            password_hash = hash_password(password)

            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Check by username or email using standard SQL
            cursor.execute("SELECT username, password_hash FROM users WHERE username = ? OR email = ?", (ident, ident))
            user = cursor.fetchone()
            conn.close()

            if user and user[1] == password_hash:
                self.send_response_json({"success": True, "username": user[0]})
            else:
                self.send_response_json({"success": False, "message": "Invalid credentials"}, 401)
                
        except Exception as e:
            self.send_response_json({"success": False, "message": str(e)}, 500)

    def send_response_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

print(f"Starting server on port {PORT}...")
http.server.HTTPServer(('', PORT), AuthHandler).serve_forever()
