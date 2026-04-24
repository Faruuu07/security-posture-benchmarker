from flask import Flask, jsonify
from flask_cors import CORS   # 👈 ADDED
from routes.describe import describe_bp

app = Flask(__name__)

CORS(app)   # 👈 ADDED (VERY IMPORTANT)

app.register_blueprint(describe_bp)

@app.route('/')
def home():
    return "AI Service Running 🚀"

@app.route('/health')
def health():
    return jsonify({
        "status": "OK"
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)