#!flask/bin/python
from flask import Flask, jsonify, abort, request


app = Flask(__name__)

@app.route('/api/hashtag/<string:hashtag>', methods=['GET'])
def get_obama(hashtag):

    if hashtag == "obama":
        return jsonify("Obama"), 200
    return jsonify({"message": "No content"}), 404

if __name__ == '__main__':
    app.run(debug=True)
    