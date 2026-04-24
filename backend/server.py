import http.server
import json
import os
import hashlib
import jwt
import datetime
from database import SessionLocal, engine
from models import User, Base

PORT = 8080
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Initialize database tables
Base.metadata.create_all(bind=engine)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    elif isinstance(salt, str):
        salt = bytes.fromhex(salt)
    
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000,
        dklen=32
    )
    return f"{salt.hex()}:{key.hex()}"

def verify_password(stored_password_hash, provided_password):
    if ':' not in stored_password_hash:
        return hashlib.sha256(provided_password.encode('utf-8')).hexdigest() == stored_password_hash
    salt_hex = stored_password_hash.split(':')[0]
    return hash_password(provided_password, salt_hex) == stored_password_hash

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

            db = SessionLocal()
            try:
                new_user = User(username=username, email=email, password_hash=password_hash)
                db.add(new_user)
                db.commit()
                self.send_response_json({"success": True, "message": "User created successfully"})
            except Exception as e:
                db.rollback()
                error_msg = str(e).lower()
                if 'username' in error_msg:
                    self.send_response_json({"success": False, "message": "Username already exists"}, 400)
                elif 'email' in error_msg:
                    self.send_response_json({"success": False, "message": "Email already exists"}, 400)
                else:
                    self.send_response_json({"success": False, "message": "Database error"}, 500)
            finally:
                db.close()
                
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

            db = SessionLocal()
            user = db.query(User).filter((User.username == ident) | (User.email == ident)).first()
            db.close()

            if user and verify_password(user.password_hash, password):
                token = create_access_token({"sub": user.username})
                self.send_response_json({
                    "success": True, 
                    "username": user.username,
                    "token": token
                })
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
