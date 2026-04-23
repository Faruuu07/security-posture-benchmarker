from flask import Flask, jsonify
from routes.describe import describe_bp

app = Flask(__name__)

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
