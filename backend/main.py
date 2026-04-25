from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import sqlite3
import os

app = FastAPI(title="Booking System API")

# Setup CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Mount static files
app.mount("/assets", StaticFiles(directory=os.path.join(PROJECT_ROOT, "assets")), name="assets")
app.mount("/src", StaticFiles(directory=os.path.join(PROJECT_ROOT, "src")), name="src")

@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(PROJECT_ROOT, "index.html"))

# Configuration
SECRET_KEY = "your-ultra-secure-secret" # In production, use env variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "users.db")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    success: bool = True

class BookingRequest(BaseModel):
    service_id: int
    appointment_time: datetime

# --- Database Utils ---
def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

# Part 2: Database Modernization (SQLite)
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            appointment_time DATETIME NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# --- Auth Utils ---
def verify_password(plain_password, hashed_password):
    # Support the old custom hash format for backward compatibility
    import hashlib
    if ':' in hashed_password:
        salt_hex, key_hex = hashed_password.split(':')
        salt = bytes.fromhex(salt_hex)
        key = hashlib.pbkdf2_hmac('sha256', plain_password.encode('utf-8'), salt, 100000, dklen=32)
        return key.hex() == key_hex
    elif len(hashed_password) == 64: # SHA256 length
        return hashlib.sha256(plain_password.encode('utf-8')).hexdigest() == hashed_password
    
    # New standard bcrypt verification
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user is None:
        raise credentials_exception
    return dict(user)

# --- Routes ---

@app.post("/api/signup")
async def signup(user: UserCreate):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Check if username or email already exists
        cursor.execute("SELECT id FROM users WHERE username = ? OR email = ?", (user.username, user.email))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Username or email already exists")
            
        hashed_password = get_password_hash(user.password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (user.username, user.email, hashed_password)
        )
        conn.commit()
        return {"success": True, "message": "User created successfully"}
    finally:
        conn.close()

@app.post("/api/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ? OR email = ?", 
        (form_data.username, form_data.username)
    ).fetchone()
    conn.close()
    
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "id": user["id"]}, expires_delta=access_token_expires
    )
    
    # We return the token with standard fields, but also add username for frontend convenience
    return {"access_token": access_token, "token_type": "bearer", "username": user["username"], "success": True}

@app.post("/bookings", status_code=status.HTTP_201_CREATED)
async def create_booking(booking: BookingRequest, current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Check database for existing conflicts at booking.appointment_time
        cursor.execute(
            "SELECT id FROM bookings WHERE service_id = ? AND appointment_time = ?", 
            (booking.service_id, booking.appointment_time)
        )
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Timeslot already booked")
            
        # 2. Save booking linked to current_user['id']
        cursor.execute(
            "INSERT INTO bookings (user_id, service_id, appointment_time) VALUES (?, ?, ?)",
            (current_user["id"], booking.service_id, booking.appointment_time)
        )
        conn.commit()
        booking_id = cursor.lastrowid
        return {"status": "success", "booking_id": booking_id}
    finally:
        conn.close()

@app.get("/bookings/me")
async def get_my_bookings(current_user: dict = Depends(get_current_user)):
    conn = get_db_connection()
    bookings = conn.execute(
        "SELECT id, service_id, appointment_time FROM bookings WHERE user_id = ?", 
        (current_user["id"],)
    ).fetchall()
    conn.close()
    
    return {"bookings": [dict(b) for b in bookings]}
