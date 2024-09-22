from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import uuid
import os

app = Flask(__name__)

# Allow CORS for all domains (for development)
CORS(app)

# If you want to restrict CORS to a specific origin (for example, Vue frontend running on localhost:8080):
# CORS(app, origins="http://localhost:8080")

# MongoDB Atlas connection (replace <username>, <password>, <cluster-url>)
MONGO_URI = os.environ.get('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client.todo_db
todos_collection = db.todos

# Helper function to serialize MongoDB documents
def serialize_doc(doc):
    return {
        "_id": str(doc["_id"]),
        "task": doc["task"],
        "completed": doc["completed"]
    }

# Route to get all todos
@app.route('/todos', methods=['GET'])
@cross_origin(origin='*')
def get_todos():
    todos = todos_collection.find()
    return jsonify([serialize_doc(todo) for todo in todos])

# Route to add a new todo
@app.route('/todos', methods=['POST'])
@cross_origin(origin='*')
def add_todo():
    new_todo = request.json
    todo_id = str(uuid.uuid4())
    todos_collection.insert_one({
        "_id": todo_id,
        "task": new_todo["task"],
        "completed": False
    })
    return jsonify({"_id": todo_id}), 201

# Route to update a todo
@app.route('/todos/<id>', methods=['PUT'])
@cross_origin(origin='*')
def update_todo(id):
    updated_data = request.json
    todos_collection.update_one({"_id": id}, {"$set": {"completed": updated_data["completed"]}})
    return jsonify({"message": "Todo updated"}), 200

# Route to delete a todo
@app.route('/todos/<id>', methods=['DELETE'])
@cross_origin(origin='*')
def delete_todo(id):
    todos_collection.delete_one({"_id": id})
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001, host="0.0.0.0")
