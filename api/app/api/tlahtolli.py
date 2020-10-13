from flask import jsonify, request, url_for, g
from app import db
from app.models import Tlahtolli
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request

@bp.route('/tlahtolli/<word>', methods=['GET'])
@token_auth.login_required
def get_tlahtolli(word):
    return jsonify(Tlahtolli.query.filter_by(user_id=g.current_user.id, word=word).first_or_404().to_dict())

@bp.route('/tlahtolli', methods=['GET'])
@token_auth.login_required
def get_mochi_tlahtolli():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 200)
    data = Tlahtolli.to_collection_dict(Tlahtolli.query, page, per_page, 'api.get_mochi_tlahtolli')
    return jsonify(data)

@bp.route('/tlahtolli', methods=['POST'])
@token_auth.login_required
def create_tlahtolli():
    data = request.get_json() or {}
    if 'word' not in data or 'state' not in data:
        return bad_request('must include word and state')
    if Tlahtolli.query.filter_by(word=data['word']):
        return bad_request("there's already a Tlahtolli for that word")
    tlahtolli = Tlahtolli()
    tlahtolli.from_dict(data)
    db.session.add(tlahtolli)
    db.session.commit()
    response = jsonify(tlahtolli.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_tlahtolli', word=tlahtolli.word)
    return response

@bp.route('/tlahtolli/<word>', methods=['PUT'])
@token_auth.login_required
def update_tlahtolli(word):
    tlahtolli = Tlahtolli.query.filter_by(word=word).first_or_404()
    if g.current_user.id != tlahtolli.user_id:
        return error_response(403)
    data = request.get_json() or {}
    tlahtolli.from_dict(data)
    db.session.commit()
    return jsonify(tlahtolli.to_dict())