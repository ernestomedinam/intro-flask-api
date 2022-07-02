from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Thought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1024), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    tags = db.relationship("Tag", backref="thought", cascade="all, delete-orphan")

    def __init__(self, content):
        self.content = content

    @classmethod
    def record(cls, content, tags):
        """
            method to create a thought and its
            related tags. Saludos a la clase32. 
        """
        new_thought = cls(content)
        db.session.add(new_thought)
        try:
            db.session.commit()
            for tag in tags:
                new_tag = Tag(tag, new_thought.id)
                db.session.add(new_tag)
            db.session.commit()
            return new_thought
        except Exception as error:
            print(error.args)
            return None

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "tags": [tag.text for tag in self.tags],
            "date": self.date.isoformat()
        }

    def delete(self):
        """ borra la instancia de la base de datos """
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

    def update(self, content):
        self.content = content
        try: 
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False

    def update_tags(self, tags):
        for tag in self.tags:
            tag.delete()
        for tag in tags:
            new_tag = Tag(tag, self.id)
            db.session.add(new_tag)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False        

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), nullable=False)
    thought_id = db.Column(db.Integer, db.ForeignKey("thought.id", ondelete="CASCADE"), nullable=False)

    def __init__(self, text, thought_id):
        self.text = text
        self.thought_id = thought_id

    def delete(self):
        """ borra la instancia de la base de datos """
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception as error:
            print(error.args)
            return False
    
    def serialize(self):
        return {
            "text": self.text
        }