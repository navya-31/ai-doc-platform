# # models.py
# from db import db
# from datetime import datetime
# import json

# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(240), unique=True, nullable=False)
#     password_hash = db.Column(db.String(240), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

# class Project(db.Model):
#     __tablename__ = "projects"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     doc_type = db.Column(db.String(10), nullable=False)  # 'docx' or 'pptx'
#     topic = db.Column(db.String(500), nullable=False)
#     config = db.Column(db.Text, default="{}")  # store outline/slide titles as JSON
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)

#     def get_config(self):
#         return json.loads(self.config or "{}")

#     def set_config(self, obj):
#         self.config = json.dumps(obj)

# class Section(db.Model):
#     __tablename__ = "sections"
#     id = db.Column(db.Integer, primary_key=True)
#     project_id = db.Column(db.Integer, nullable=False)
#     title = db.Column(db.String(500), nullable=False)
#     content = db.Column(db.Text, default="")
#     comments = db.Column(db.Text, default="")  # JSON array string
#     likes = db.Column(db.Integer, default=0)
#     dislikes = db.Column(db.Integer, default=0)
#     order = db.Column(db.Integer, default=0)

#     def add_comment(self, comment):
#         import json
#         arr = json.loads(self.comments or "[]")
#         arr.append(comment)
#         self.comments = json.dumps(arr)



# models.py - Updated with revision history tracking
from db import db
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(240), unique=True, nullable=False)
    password_hash = db.Column(db.String(240), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    doc_type = db.Column(db.String(10), nullable=False)
    topic = db.Column(db.String(500), nullable=False)
    config = db.Column(db.Text, default="{}")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_config(self):
        return json.loads(self.config or "{}")

    def set_config(self, obj):
        self.config = json.dumps(obj)

class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, default="")
    comments = db.Column(db.Text, default="")
    likes = db.Column(db.Integer, default=0)
    dislikes = db.Column(db.Integer, default=0)
    order = db.Column(db.Integer, default=0)

    def add_comment(self, comment):
        arr = json.loads(self.comments or "[]")
        arr.append(comment)
        self.comments = json.dumps(arr)

class RevisionHistory(db.Model):
    """Track all AI refinements and edits for each section"""
    __tablename__ = "revision_history"
    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=False)
    instruction = db.Column(db.Text, nullable=False)
    old_content = db.Column(db.Text, nullable=False)
    new_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    section = db.relationship('Section', backref=db.backref('revisions', lazy=True))