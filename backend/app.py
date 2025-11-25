# # app.py - main Flask server

# import os
# from dotenv import load_dotenv
# load_dotenv()
# from flask import Flask, request, jsonify, send_file
# from db import db
# from models import User, Project, Section
# from auth import hash_password, verify_password, create_token, auth_required
# from llm import generate_section_content, refine_content
# from export_docx import build_docx_bytes
# from export_pptx import build_pptx_bytes
# import json
# from flask_cors import CORS
# from dotenv import load_dotenv


# def make_app():
#     app = Flask(__name__)
#     CORS(app)

#     basedir = os.path.abspath(os.path.dirname(__file__))
#     app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "data.db")
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db.init_app(app)

#     with app.app_context():
#         db.create_all()

#     #### AUTH ROUTES
#     @app.route("/api/register", methods=["POST"])
#     def register():
#         data = request.json or {}
#         email = data.get("email")
#         password = data.get("password")
#         if not email or not password:
#             return jsonify({"error": "email and password required"}), 400
#         if User.query.filter_by(email=email).first():
#             return jsonify({"error": "user exists"}), 400
#         u = User(email=email, password_hash=hash_password(password))
#         db.session.add(u)
#         db.session.commit()
#         token = create_token(u.id)
#         return jsonify({"token": token, "user": {"id": u.id, "email": u.email}})

#     @app.route("/api/login", methods=["POST"])
#     def login():
#         data = request.json or {}
#         email = data.get("email")
#         password = data.get("password")
#         u = User.query.filter_by(email=email).first()
#         if not u or not verify_password(u.password_hash, password):
#             return jsonify({"error": "invalid credentials"}), 401
#         token = create_token(u.id)
#         return jsonify({"token": token, "user": {"id": u.id, "email": u.email}})

#     #### PROJECTS
#     @app.route("/api/projects", methods=["GET"])
#     @auth_required
#     def list_projects(current_user_id):
#         projects = Project.query.filter_by(user_id=current_user_id).all()
#         out = []
#         for p in projects:
#             out.append({
#                 "id": p.id, "doc_type": p.doc_type, "topic": p.topic, "config": p.get_config()
#             })
#         return jsonify(out)

#     @app.route("/api/projects", methods=["POST"])
#     @auth_required
#     def create_project(current_user_id):
#         data = request.json or {}
#         doc_type = data.get("doc_type")
#         topic = data.get("topic")
#         config = data.get("config", {})
#         if doc_type not in ("docx", "pptx"):
#             return jsonify({"error": "doc_type must be 'docx' or 'pptx'"}), 400

#         p = Project(user_id=current_user_id, doc_type=doc_type, topic=topic)
#         p.set_config(config)
#         db.session.add(p)
#         db.session.commit()

#         # Create initial sections
#         if doc_type == "docx":
#             for idx, s in enumerate(config.get("sections", [])):
#                 sec = Section(project_id=p.id, title=s.get("title", ""), order=idx)
#                 db.session.add(sec)
#         else:
#             for idx, s in enumerate(config.get("slides", [])):
#                 sec = Section(project_id=p.id, title=s.get("title", ""), order=idx)
#                 db.session.add(sec)

#         db.session.commit()
#         return jsonify({"id": p.id, "doc_type": p.doc_type, "topic": p.topic, "config": config})

#     @app.route("/api/projects/<int:project_id>", methods=["GET"])
#     @auth_required
#     def get_project(project_id, current_user_id):
#         p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
#         if not p:
#             return jsonify({"error": "not found"}), 404

#         sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
#         secs = []
#         for s in sections:
#             try:
#                 comments = json.loads(s.comments or "[]")
#             except:
#                 comments = []
#             secs.append({
#                 "id": s.id,
#                 "title": s.title,
#                 "content": s.content or "",
#                 "comments": comments,
#                 "likes": s.likes,
#                 "dislikes": s.dislikes,
#                 "order": s.order
#             })

#         return jsonify({
#             "id": p.id,
#             "doc_type": p.doc_type,
#             "topic": p.topic,
#             "config": p.get_config(),
#             "sections": secs
#         })

#     #### GENERATE CONTENT
#     @app.route("/api/projects/<int:project_id>/generate", methods=["POST"])
#     @auth_required
#     def generate_project(project_id, current_user_id):
#         p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
#         if not p:
#             return jsonify({"error": "not found"}), 404

#         sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
#         results = []
#         for s in sections:
#             if not s.content:
#                 s.content = generate_section_content(s.title, p.topic)
#                 db.session.add(s)
#                 db.session.commit()

#             results.append({
#                 "section_id": s.id,
#                 "title": s.title,
#                 "content": s.content
#             })

#         return jsonify({"generated": results})

#     #### REFINE SECTION
#     @app.route("/api/sections/<int:section_id>/refine", methods=["POST"])
#     @auth_required
#     def refine_section(section_id, current_user_id):
#         data = request.json or {}
#         instruction = data.get("instruction", "")
#         s = Section.query.filter_by(id=section_id).first()

#         if not s:
#             return jsonify({"error": "no section"}), 404

#         p = Project.query.filter_by(id=s.project_id, user_id=current_user_id).first()
#         if not p:
#             return jsonify({"error": "not allowed"}), 403

#         new_text = refine_content(s.content or "", instruction)
#         s.content = new_text
#         db.session.add(s)
#         db.session.commit()

#         return jsonify({"id": s.id, "title": s.title, "content": s.content})

#     #### FEEDBACK
#     @app.route("/api/sections/<int:section_id>/feedback", methods=["POST"])
#     @auth_required
#     def section_feedback(section_id, current_user_id):
#         data = request.json or {}
#         action = data.get("action")
#         s = Section.query.filter_by(id=section_id).first()

#         if not s:
#             return jsonify({"error": "no section"}), 404

#         p = Project.query.filter_by(id=s.project_id, user_id=current_user_id).first()
#         if not p:
#             return jsonify({"error": "not allowed"}), 403

#         if action == "like":
#             s.likes = (s.likes or 0) + 1
#         elif action == "dislike":
#             s.dislikes = (s.dislikes or 0) + 1
#         elif action == "comment":
#             comment = data.get("comment", "")
#             s.add_comment({"user_id": current_user_id, "text": comment})

#         db.session.add(s)
#         db.session.commit()
#         return jsonify({
#             "id": s.id,
#             "likes": s.likes,
#             "dislikes": s.dislikes
#         })

#     #### EXPORT DOCUMENT
#     @app.route("/api/projects/<int:project_id>/export", methods=["GET"])
#     @auth_required
#     def export_project(project_id, current_user_id):
#         export_type = request.args.get("type", "docx")
#         p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()

#         if not p:
#             return jsonify({"error": "not found"}), 404

#         sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
#         sec_list = [{"title": s.title, "content": s.content or ""} for s in sections]

#         if export_type == "docx":
#             bio = build_docx_bytes(sec_list)
#             return send_file(
#                 bio, as_attachment=True,
#                 download_name=f"{p.topic[:40]}.docx",
#                 mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
#             )
#         else:
#             bio = build_pptx_bytes(sec_list)
#             return send_file(
#                 bio, as_attachment=True,
#                 download_name=f"{p.topic[:40]}.pptx",
#                 mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
#             )

#     #### ADD NEW SECTION TO PROJECT
#     @app.route("/api/projects/<int:project_id>/sections", methods=["POST"])
#     @auth_required
#     def add_section(project_id, current_user_id):
#         data = request.json or {}
#         title = data.get("title", "").strip()

#         if not title:
#             return jsonify({"error": "title required"}), 400

#         p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
#         if not p:
#             return jsonify({"error": "not allowed"}), 403

#         max_order = db.session.query(db.func.max(Section.order)).filter_by(project_id=project_id).scalar()
#         next_order = (max_order + 1) if max_order is not None else 0

#         sec = Section(project_id=project_id, title=title, order=next_order)
#         db.session.add(sec)
#         db.session.commit()

#         return jsonify({
#             "id": sec.id,
#             "title": sec.title,
#             "order": sec.order
#         })

#     return app


# if __name__ == "__main__":
#     app = make_app()
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=False)

# app.py - Complete Flask server with all features

import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify, send_file
from db import db
from models import User, Project, Section, RevisionHistory
from auth import hash_password, verify_password, create_token, auth_required
from llm import generate_section_content, refine_content, generate_outline
from export_docx import build_docx_bytes
from export_pptx import build_pptx_bytes
import json
from flask_cors import CORS
from datetime import datetime


def make_app():
    app = Flask(__name__)
    CORS(app)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    #### AUTH ROUTES
    @app.route("/api/register", methods=["POST"])
    def register():
        data = request.json or {}
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            return jsonify({"error": "email and password required"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "user exists"}), 400
        u = User(email=email, password_hash=hash_password(password))
        db.session.add(u)
        db.session.commit()
        token = create_token(u.id)
        return jsonify({"token": token, "user": {"id": u.id, "email": u.email}})

    @app.route("/api/login", methods=["POST"])
    def login():
        data = request.json or {}
        email = data.get("email")
        password = data.get("password")
        u = User.query.filter_by(email=email).first()
        if not u or not verify_password(u.password_hash, password):
            return jsonify({"error": "invalid credentials"}), 401
        token = create_token(u.id)
        return jsonify({"token": token, "user": {"id": u.id, "email": u.email}})

    #### PROJECTS
    @app.route("/api/projects", methods=["GET"])
    @auth_required
    def list_projects(current_user_id):
        projects = Project.query.filter_by(user_id=current_user_id).all()
        out = []
        for p in projects:
            out.append({
                "id": p.id, "doc_type": p.doc_type, "topic": p.topic, "config": p.get_config()
            })
        return jsonify(out)

    @app.route("/api/projects", methods=["POST"])
    @auth_required
    def create_project(current_user_id):
        data = request.json or {}
        doc_type = data.get("doc_type")
        topic = data.get("topic")
        config = data.get("config", {})
        if doc_type not in ("docx", "pptx"):
            return jsonify({"error": "doc_type must be 'docx' or 'pptx'"}), 400

        p = Project(user_id=current_user_id, doc_type=doc_type, topic=topic)
        p.set_config(config)
        db.session.add(p)
        db.session.commit()

        # Create initial sections
        if doc_type == "docx":
            for idx, s in enumerate(config.get("sections", [])):
                sec = Section(project_id=p.id, title=s.get("title", ""), order=idx)
                db.session.add(sec)
        else:
            for idx, s in enumerate(config.get("slides", [])):
                sec = Section(project_id=p.id, title=s.get("title", ""), order=idx)
                db.session.add(sec)

        db.session.commit()
        return jsonify({"id": p.id, "doc_type": p.doc_type, "topic": p.topic, "config": config})

    @app.route("/api/projects/<int:project_id>", methods=["GET"])
    @auth_required
    def get_project(project_id, current_user_id):
        p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not found"}), 404

        sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
        secs = []
        for s in sections:
            try:
                comments = json.loads(s.comments or "[]")
            except:
                comments = []
            secs.append({
                "id": s.id,
                "title": s.title,
                "content": s.content or "",
                "comments": comments,
                "likes": s.likes,
                "dislikes": s.dislikes,
                "order": s.order
            })

        return jsonify({
            "id": p.id,
            "doc_type": p.doc_type,
            "topic": p.topic,
            "config": p.get_config(),
            "sections": secs
        })

    #### AI OUTLINE GENERATION (BONUS FEATURE)
    @app.route("/api/projects/suggest-outline", methods=["POST"])
    @auth_required
    def suggest_outline(current_user_id):
        """NEW: AI-generated outline suggestion"""
        data = request.json or {}
        topic = data.get("topic")
        doc_type = data.get("doc_type")
        
        if not topic or not doc_type:
            return jsonify({"error": "topic and doc_type required"}), 400
        
        if doc_type not in ("docx", "pptx"):
            return jsonify({"error": "doc_type must be 'docx' or 'pptx'"}), 400
        
        outline = generate_outline(topic, doc_type)
        
        if doc_type == "docx":
            return jsonify({"sections": outline})
        else:
            return jsonify({"slides": outline})

    #### GENERATE CONTENT
    @app.route("/api/projects/<int:project_id>/generate", methods=["POST"])
    @auth_required
    def generate_project(project_id, current_user_id):
        p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not found"}), 404

        sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
        results = []
        for s in sections:
            if not s.content:
                s.content = generate_section_content(s.title, p.topic)
                db.session.add(s)
                db.session.commit()

            results.append({
                "section_id": s.id,
                "title": s.title,
                "content": s.content
            })

        return jsonify({"generated": results})

    #### REFINE SECTION (with revision history tracking)
    @app.route("/api/sections/<int:section_id>/refine", methods=["POST"])
    @auth_required
    def refine_section(section_id, current_user_id):
        data = request.json or {}
        instruction = data.get("instruction", "")
        s = Section.query.filter_by(id=section_id).first()

        if not s:
            return jsonify({"error": "no section"}), 404

        p = Project.query.filter_by(id=s.project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not allowed"}), 403

        old_content = s.content or ""
        new_text = refine_content(old_content, instruction)
        
        # Save revision history
        revision = RevisionHistory(
            section_id=s.id,
            instruction=instruction,
            old_content=old_content,
            new_content=new_text
        )
        db.session.add(revision)
        
        s.content = new_text
        db.session.add(s)
        db.session.commit()

        return jsonify({"id": s.id, "title": s.title, "content": s.content})

    #### REVISION HISTORY
    @app.route("/api/sections/<int:section_id>/history", methods=["GET"])
    @auth_required
    def get_revision_history(section_id, current_user_id):
        """NEW: Get revision history for a section"""
        s = Section.query.filter_by(id=section_id).first()
        
        if not s:
            return jsonify({"error": "no section"}), 404
        
        p = Project.query.filter_by(id=s.project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not allowed"}), 403
        
        revisions = RevisionHistory.query.filter_by(section_id=section_id).order_by(RevisionHistory.timestamp.desc()).all()
        
        history = []
        for r in revisions:
            history.append({
                "id": r.id,
                "instruction": r.instruction,
                "old": r.old_content,
                "new": r.new_content,
                "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify(history)

    #### FEEDBACK
    @app.route("/api/sections/<int:section_id>/feedback", methods=["POST"])
    @auth_required
    def section_feedback(section_id, current_user_id):
        data = request.json or {}
        action = data.get("action")
        s = Section.query.filter_by(id=section_id).first()

        if not s:
            return jsonify({"error": "no section"}), 404

        p = Project.query.filter_by(id=s.project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not allowed"}), 403

        if action == "like":
            s.likes = (s.likes or 0) + 1
        elif action == "dislike":
            s.dislikes = (s.dislikes or 0) + 1
        elif action == "comment":
            comment = data.get("comment", "")
            s.add_comment({"user_id": current_user_id, "text": comment, "timestamp": datetime.utcnow().isoformat()})

        db.session.add(s)
        db.session.commit()
        return jsonify({
            "id": s.id,
            "likes": s.likes,
            "dislikes": s.dislikes
        })

    #### EXPORT DOCUMENT
    @app.route("/api/projects/<int:project_id>/export", methods=["GET"])
    @auth_required
    def export_project(project_id, current_user_id):
        export_type = request.args.get("type", "docx")
        p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()

        if not p:
            return jsonify({"error": "not found"}), 404

        sections = Section.query.filter_by(project_id=p.id).order_by(Section.order).all()
        sec_list = [{"title": s.title, "content": s.content or ""} for s in sections]

        if export_type == "docx":
            bio = build_docx_bytes(sec_list)
            return send_file(
                bio, as_attachment=True,
                download_name=f"{p.topic[:40]}.docx",
                mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            bio = build_pptx_bytes(sec_list)
            return send_file(
                bio, as_attachment=True,
                download_name=f"{p.topic[:40]}.pptx",
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )

    #### ADD NEW SECTION TO PROJECT
    @app.route("/api/projects/<int:project_id>/sections", methods=["POST"])
    @auth_required
    def add_section(project_id, current_user_id):
        data = request.json or {}
        title = data.get("title", "").strip()

        if not title:
            return jsonify({"error": "title required"}), 400

        p = Project.query.filter_by(id=project_id, user_id=current_user_id).first()
        if not p:
            return jsonify({"error": "not allowed"}), 403

        max_order = db.session.query(db.func.max(Section.order)).filter_by(project_id=project_id).scalar()
        next_order = (max_order + 1) if max_order is not None else 0

        sec = Section(project_id=project_id, title=title, order=next_order)
        db.session.add(sec)
        db.session.commit()

        return jsonify({
            "id": sec.id,
            "title": sec.title,
            "order": sec.order
        })

    return app


if __name__ == "__main__":
    app = make_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)