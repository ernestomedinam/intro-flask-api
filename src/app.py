import os
from flask import Flask, jsonify, request
from datetime import datetime
from models import db, Thought
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
db.init_app(app)
Migrate(app, db)


@app.route("/thoughts", methods=['GET', 'POST'])
def handle_thoughts():
    if request.method == "GET":
        all_thoughts = Thought.query.all()
        return jsonify(
            [thought.serialize() for thought in all_thoughts]
        ), 200
    else:
        body = request.json
        new_thought = Thought.record(
            body["content"],
            body["tags"]
        )
        if new_thought is None:
            return jsonify("algo salio mal"), 400
        return jsonify(new_thought.serialize()), 201

@app.route("/thoughts/<int:thought_id>", methods=["GET", "PATCH", "DELETE"])
def handle_thought(thought_id):
    thought = Thought.query.filter_by(id=thought_id).one_or_none()
    if thought is None: return "no such thought", 404
    if request.method == "GET":
        return jsonify(thought.serialize()), 200
    elif request.method == "DELETE":
        deleted = thought.delete()
        if deleted == False: return jsonify("algo salio mal"), 500 
        return "", 204
    else:
        body = request.json
        if 'content' in body:
            # actualizo el objeto
            thought.update(body["content"])
            # thought.content = body["content"]
        if 'tags' in body:
            # actualizco el objeto
            thought.update_tags(body["tags"])
            # thought.tags = body["tags"]
        return jsonify(thought.serialize()), 200 # el objeto, serializado


@app.route("/hello")
def hello_api():
    return "hello user"


app.run(
    host="127.0.0.1",
    port=5000,
    debug=True
)