from fastapi import FastAPI, HTTPException, Response, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import hashlib
import jwt
import datetime
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from .database import SessionLocal, engine
from .models import User, Base

PORT = 8080
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

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

# Pydantic models
class LoginRequest(BaseModel):
    ident: str
    password: str

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/signup")
def signup(req: SignupRequest, db: SessionLocal = Depends(get_db)):
    password_hash = hash_password(req.password)
    try:
        new_user = User(username=req.username, email=req.email, password_hash=password_hash)
        db.add(new_user)
        db.commit()
        return {"success": True, "message": "User created successfully"}
    except Exception as e:
        db.rollback()
        error_msg = str(e).lower()
        if 'username' in error_msg:
            return JSONResponse(status_code=400, content={"success": False, "message": "Username already exists"})
        elif 'email' in error_msg:
            return JSONResponse(status_code=400, content={"success": False, "message": "Email already exists"})
        else:
            return JSONResponse(status_code=500, content={"success": False, "message": "Database error"})

@app.post("/api/login")
@limiter.limit("5/minute")
def login(request: Request, req: LoginRequest, response: Response, db: SessionLocal = Depends(get_db)):
    user = db.query(User).filter((User.username == req.ident) | (User.email == req.ident)).first()
    
    if user and verify_password(user.password_hash, req.password):
        token = create_access_token({"sub": user.username})
        
        # Set HttpOnly cookie
        response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=1800 # 30 minutes
        )
        
        return {"success": True, "username": user.username}
    else:
        return JSONResponse(status_code=401, content={"success": False, "message": "Invalid credentials"})

# Mount static files
app.mount("/assets", StaticFiles(directory="assets"), name="assets")
app.mount("/src", StaticFiles(directory="src"), name="src")

@app.get("/")
def read_index():
    return FileResponse("index.html")

@app.get("/robots.txt")
def read_robots():
    return FileResponse("robots.txt")

@app.get("/sitemap.xml")
def read_sitemap():
    return FileResponse("sitemap.xml")
