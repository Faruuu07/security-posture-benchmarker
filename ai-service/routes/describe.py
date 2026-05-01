from flask import Blueprint, request, jsonify
from services.ai_service import generate_description
from database import get_connection
import jwt
from functools import wraps

SECRET_KEY = "mysecretkey"

describe_bp = Blueprint('describe', __name__)

# 🔐 TOKEN VERIFY
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

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


# 🔥 DESCRIBE (SAVE TO DB)
@describe_bp.route('/describe', methods=['POST'])
@token_required
def describe(current_user_id):
    data = request.json
    user_input = data.get("input")

    result = generate_description(user_input)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history (user_id, input, response) VALUES (?, ?, ?)",
        (current_user_id, user_input, result)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "response": result
    })


# 📜 USER HISTORY
@describe_bp.route('/history', methods=['GET'])
@token_required
def get_history(current_user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT input, response FROM history WHERE user_id=? ORDER BY id DESC",
        (current_user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    history = [
        {"input": row["input"], "response": row["response"]}
        for row in rows
    ]

    return jsonify(history)


# 🧹 CLEAR USER HISTORY
@describe_bp.route('/clear-history', methods=['POST'])
@token_required
def clear_history(current_user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE user_id=?",
        (current_user_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "User history cleared"
    })