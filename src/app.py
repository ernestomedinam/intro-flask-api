from flask import Flask, jsonify, request
from datetime import datetime


app = Flask(__name__)


class Thought:
    all_thoughts = []

    def __init__(self, content, tags):
        self.id = len(self.__class__.all_thoughts) + 1
        self.content = content
        self.date = datetime.utcnow
        self.tags = tags
        self.__class__.all_thoughts.append(self)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "tags": self.tags
        }

@app.route("/thoughts", methods=['GET', 'POST'])
def handle_thoughts():
    if request.method == "GET":
        return jsonify(
            [thought.serialize() for thought in Thought.all_thoughts]
        )
    else:
        body = request.json
        new_thought = Thought(
            body["content"],
            body["tags"]
        )
        return jsonify(new_thought.serialize()), 201

@app.route("/thoughts/<int:thought_id>", methods=["GET", "PATCH", "DELETE"])
def handle_thought(thought_id):
    thoughts = list(
        filter(
            lambda thought: thought.id == thought_id,
            Thought.all_thoughts
        )
    )
    if len(thoughts) == 0: return "no such thought", 404
    thought = thoughts[0]
    if request.method == "GET":
        return jsonify(thought.serialize()), 200
    elif request.method == "DELETE":
        Thought.all_thoughts = list(
            filter(
                lambda thought: thought.id != thought_id,
                Thought.all_thoughts
            )
        )
        return "", 204
    else:
        body = request.json
        if 'content' in body:
            # actualizo el objeto
            thought.content = body["content"]
        if 'tags' in body:
            # actualizco el objeto
            thought.tags = body["tags"]
        return jsonify(thought.serialize()), 200 # el objeto, serializado


@app.route("/hello")
def hello_api():
    return "hello user"








app.run(
    host="127.0.0.1",
    port=5000,
    debug=True
)