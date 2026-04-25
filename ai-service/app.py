from flask import Flask, jsonify
from flask_cors import CORS
from routes.describe import describe_bp
import os   # 👈 ADD THIS

app = Flask(__name__)

CORS(app)

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
    port = int(os.environ.get("PORT", 5000))   # 👈 IMPORTANT
    app.run(host="0.0.0.0", port=port)         # 👈 IMPORTANT