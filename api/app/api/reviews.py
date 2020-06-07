from flask import jsonify, request, url_for, g
from app import db
from app.models import Review
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request

bp.route('/reviews/<int:id>', methods=['GET'])
@token_auth.login_required
def get_review():
    return jsonify(Review.query.get_or_404(id).to_dict())

bp.route('/reviews', methods=['POST'])
@token_auth.login_required
def save_review():
    data = request.get_json() or {}
    if 'rating' not in data:
        return bad_request("must include like or dislike")
    if Review.query.filter_by(reviewer_id=data['reviewer_id']).filter_by(lesson_id=data['lesson_id']).all():
        return bad_request("there's already a review for this lesson by this user")
    review = Review()
    review.from_dict(data)
    db.session.add(review)
    db.session.commit()
    response = jsonify(review.to_dict())
    response.status = 201
    response.headers['Location'] = url_for('api.get_review', id=review.id)
    return response

@bp.route('/reviews/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_review(id):
    if 'reviewer_id' not in data or g.current_user.id != data['reviewer_id']:
        return error_response(403)
    review = Review.query.get_or_404(id)
    data = request.get_json() or {}
    if 'rating' not in data:
        return bad_request("must include like or dislike")
    review.from_dict(data)
    db.session.commit()
    return jsonify(review.to_dict())

@bp.route('/review/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_review(id):
    if 'reviewer_id' not in data or g.current_user.id != data['reviewer_id']:
        return error_response(403)
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    return '', 204
