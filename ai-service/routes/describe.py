from flask import Blueprint, request, jsonify
from services.ai_service import generate_description
from storage import history

describe_bp = Blueprint('describe', __name__)

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.json
    user_input = data.get("input")

    result = generate_description(user_input)

    history.append({
        "input": user_input,
        "response": result
    })

    return jsonify({
        "response": result
    })


@describe_bp.route('/history', methods=['GET'])
def get_history():
    return jsonify(history)


# 👇 YE NAYA ADD KIYA
@describe_bp.route('/clear-history', methods=['POST'])
def clear_history():
    history.clear()
    
    return jsonify({
        "message": "History cleared"
    })