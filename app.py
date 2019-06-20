from flask import Flask, request, jsonify
from pymongo import MongoClient
import json


MESSAGES_KEYS = ['message', 'sender', 'receptant', 'lat', 'long', 'date']

uri = "mongodb://grupo25:grupo25@146.155.13.149/grupo25?authSource=admin"

client = MongoClient(uri)

db = client.get_database()

messages = db.messages

users = db.users

messages.create_index([('message', 'text')])

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>API Homepage</h1>"

@app.route("/messages")
def get_messages():
    required = []
    prohibited = []
    desirable = []
    parameters = request.json
    if parameters:
        required = parameters['required'] if 'required' in parameters else []
        prohibited = parameters['prohibited'] if 'prohibited' in parameters \
            else []
        desirable = parameters['desirable'] if 'desirable' in parameters else []
    filtered = ""
    for r in required:
        filtered += f"\"{r}\" "
    for d in desirable:
        filtered += f"{d} "
    if filtered:
        for p in prohibited:
            filtered += f"-{p} "
        result = messages.find({"$text": {"$search": filtered}}, {"_id": 0})
    else:
        result = messages.find({}, {"_id": 0})
    output = [msg for msg in result]
    return jsonify(output)

@app.route("/messages/<int:mid>")
def get_message(mid):
    msgs = list(messages.find({"mid": mid}, {"_id": 0}))
    return jsonify(msgs)

@app.route("/messages", methods=['POST'])
def create_message():
    data = {key: request.json[key] for key in MESSAGES_KEYS}
    count = messages.count_documents({})
    data["mid"] = count + 1
    result = messages.insert_one(data)
    if result:
        message = "Mensaje creado con éxito!"
        success = True
    else:
        message = "No se pudo crear el mensaje!"
        success = False
    return jsonify({'success': success, 'message': message})


@app.route('/messages/<int:mid>', methods=['DELETE'])
def delete_message(mid):
    messages.delete_one({"mid": mid})
    message = f'El mensaje con ID {mid} ha sido eliminado!'
    return jsonify({'result': 'success', 'message': message})

@app.route('/users/<int:uid>')
def get_user(uid):
    user = list(users.find({"uid": uid}, {"_id": 0}))
    required = []
    prohibited = []
    desirable = []
    parameters = request.json
    if parameters:
        required = parameters['required'] if 'required' in parameters else []
        prohibited = parameters['prohibited'] if 'prohibited' in parameters \
            else []
        desirable = parameters['desirable'] if 'desirable' in parameters else []
    filtered = ""
    for r in required:
        filtered += f"\"{r}\" "
    for d in desirable:
        filtered += f"{d} "
    if filtered:
        for p in prohibited:
            filtered += f"-{p} "
        result = messages.find({"$text": {"$search": filtered},
                                "sender": uid}, {"_id": 0})
    else:
        result = messages.find({"sender": uid}, {"_id": 0})
    user_messages = [msg for msg in result]
    user[0]['messages'] = user_messages
    return jsonify(user)


@app.route('/communication/<int:uid_1>/<int:uid_2>')
def get_communication(uid_1, uid_2):
    msgs = list(messages.find({'$or': [
        {'$and': [{'sender': uid_1}, {'receptant': uid_2}]},
        {'$and': [{'sender': uid_2}, {'receptant': uid_1}]}]}, {'_id': 0}))
    return jsonify(msgs) 


if __name__ == '__main__':
    app.run()
