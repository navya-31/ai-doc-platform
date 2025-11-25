# auth.py - simple password hashing + jwt utils
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import request, jsonify

JWT_SECRET = os.environ.get("JWT_SECRET", "change_this_secret")
JWT_ALGO = "HS256"
JWT_EXPIRE_HOURS = 24

def hash_password(plain):
    return generate_password_hash(plain)

def verify_password(hash_, plain):
    return check_password_hash(hash_, plain)

def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=int(os.environ.get("JWT_EXPIRE_HOURS", JWT_EXPIRE_HOURS)))
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token):
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return data
    except Exception as e:
        return None

def auth_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Missing token"}), 401
        token = auth_header.split(" ", 1)[1]
        data = decode_token(token)
        if not data:
            return jsonify({"error": "Invalid or expired token"}), 401
        # inject user id into kwargs
        kwargs["current_user_id"] = data.get("user_id")
        return fn(*args, **kwargs)
    return wrapper