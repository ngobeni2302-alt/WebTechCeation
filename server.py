import http.server
import json
import os

PORT = 8080
DB_FILE = "database/users.json"

# Ensure database file exists
if not os.path.exists(DB_FILE):
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with open(DB_FILE, 'w') as f:
        json.dump({}, f)

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
        data = self.get_post_data()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        with open(DB_FILE, 'r+') as f:
            users = json.load(f)
            if username in users:
                self.send_response_json({"success": False, "message": "Username already exists"}, 400)
                return
            
            # Check email
            if any(u.get('email') == email for u in users.values()):
                self.send_response_json({"success": False, "message": "Email already exists"}, 400)
                return

            users[username] = {"pass": password, "email": email}
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()

        self.send_response_json({"success": True, "message": "User created successfully"})

    def handle_login(self):
        data = self.get_post_data()
        ident = data.get('ident')
        password = data.get('password')

        with open(DB_FILE, 'r') as f:
            users = json.load(f)
        
        found_user = None
        username = None

        if ident in users:
            found_user = users[ident]
            username = ident
        else:
            for uname, udata in users.items():
                if udata.get('email') == ident:
                    found_user = udata
                    username = uname
                    break

        if found_user and found_user.get('pass') == password:
            self.send_response_json({"success": True, "username": username})
        else:
            self.send_response_json({"success": False, "message": "Invalid credentials"}, 401)

    def send_response_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

print(f"Starting server on port {PORT}...")
http.server.HTTPServer(('', PORT), AuthHandler).serve_forever()
