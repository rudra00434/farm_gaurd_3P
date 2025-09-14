from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.models import NetworkPost, NetworkComment
from app import db

bp = Blueprint('network', __name__)

@bp.route('/network/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_post = NetworkPost(
        user_id=user_id,
        title=data.get('title'),
        content=data.get('content')
    )
    
    db.session.add(new_post)
    db.session.commit()
    
    return jsonify({
        "msg": "Post created successfully",
        "post": {
            "id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "created_at": new_post.created_at.isoformat()
        }
    }), 201

@bp.route('/network/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = NetworkPost.query.order_by(NetworkPost.created_at.desc()).all()
    
    return jsonify([{
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "created_at": post.created_at.isoformat(),
        "user_id": post.user_id,
        "comments_count": len(post.comments)
    } for post in posts])

@bp.route('/network/posts/<int:post_id>/comments', methods=['POST'])
@jwt_required()
def create_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    post = NetworkPost.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404
    
    new_comment = NetworkComment(
        post_id=post_id,
        user_id=user_id,
        content=data.get('content')
    )
    
    db.session.add(new_comment)
    db.session.commit()
    
    return jsonify({
        "msg": "Comment added successfully",
        "comment": {
            "id": new_comment.id,
            "content": new_comment.content,
            "created_at": new_comment.created_at.isoformat(),
            "user_id": new_comment.user_id
        }
    }), 201

@bp.route('/network/posts/<int:post_id>/comments', methods=['GET'])
@jwt_required()
def get_comments(post_id):
    post = NetworkPost.query.get(post_id)
    if not post:
        return jsonify({"msg": "Post not found"}), 404
    
    comments = NetworkComment.query.filter_by(post_id=post_id)\
        .order_by(NetworkComment.created_at.desc()).all()
    
    return jsonify([{
        "id": comment.id,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
        "user_id": comment.user_id
    } for comment in comments])