from database import init_db
from routes.auth import auth_bp
from flask import Flask, jsonify
from flask_cors import CORS
from routes.describe import describe_bp
import os

app = Flask(__name__)

CORS(app)

# ✅ REGISTER BLUEPRINTS
app.register_blueprint(describe_bp)
app.register_blueprint(auth_bp)

# ✅ HOME
@app.route('/')
def home():
    return "AI Service Running 🚀"

# ✅ HEALTH
@app.route('/health')
def health():
    return jsonify({
        "status": "OK"
    })

# ✅ INIT DB
init_db()

# 🔥 DEBUG: SHOW ALL ROUTES
print("\n🔥 AVAILABLE ROUTES:")
print(app.url_map)
print("🔥--------------------\n")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=True)