from flask import Flask, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({
        'message': 'Hello World from Weather API!',
        'timestamp': datetime.datetime.now().isoformat(),
        'status': 'running'
    })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'weather-api',
        'timestamp': datetime.datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)