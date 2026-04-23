from flask import Blueprint, request, jsonify
from services.ai_service import generate_description

describe_bp = Blueprint('describe', __name__)

@describe_bp.route('/describe', methods=['POST'])
def describe():
    data = request.json
    user_input = data.get("input")

    result = generate_description(user_input)

    return jsonify({
        "response": result
    })