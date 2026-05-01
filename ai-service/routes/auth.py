from flask import Blueprint, request, jsonify
from database import get_connection
import jwt
import datetime
from functools import wraps

SECRET_KEY = "mysecretkey"   # later env me shift karenge

auth_bp = Blueprint('auth', __name__)

# 🔐 REGISTER
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()


# 🔑 LOGIN (JWT TOKEN)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        token = jwt.encode({
            "user_id": user["id"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY, algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "token": token
        })
    else:
        return jsonify({"error": "Invalid credentials"}), 401


# 🔐 TOKEN VERIFY DECORATOR
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 📌 Header se token lena
        if 'Authorization' in request.headers:
            try:
                token = request.headers['Authorization'].split(" ")[1]
            except:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user_id = data["user_id"]
        except:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(current_user_id, *args, **kwargs)

    return decorated


# 🔥 PROTECTED ROUTE
@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user_id):
    return jsonify({
        "message": "Protected route access granted",
        "user_id": current_user_id
    })