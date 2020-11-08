from flask import jsonify, request, url_for, g, abort, make_response
from app import db
from app.models import User
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request
from datetime import datetime, timedelta

@bp.route('/users/current', methods=['GET'])
@token_auth.login_required
def get_current_user():
    return jsonify(g.current_user.to_dict())

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('there is already a user with that username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('there is already a user with that email')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    token = user.get_token()
    user_dict = user.to_dict()
    user_dict['token'] = token
    response = jsonify(user_dict)
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    if g.current_user.id != id:
        return error_response(403)
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'action' in data and data['action'] == 'deauth':
        user.revoke_token()
        response=make_response('',200)
        response.set_cookie(#If you don't set this cookie, something weird happens and we tokens keep refreshing;
            key='refresh_token', value='', #TODO: fix the above
            expires=datetime.utcnow()-timedelta(hours=24), httponly=True)
        return response
    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())

@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    if g.current_user.id != id:
        return error_response(403)
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
