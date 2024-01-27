from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test', methods=['POST'])
def test():
    link = request.json['link']
    return jsonify({'msg': "success"})

if __name__ == '__main__':
    app.run(debug=True)