from flask import jsonify, request, url_for, g
from app import db
from app.models import Lesson
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response, bad_request

@bp.route('/lessons/<int:id>', methods=['GET'])
@token_auth.login_required
def get_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    user_tlahtolli = lesson.get_user_tlahtolli(g.current_user)
    lesson_dict = lesson.to_dict(include_content=True)
    lesson_dict['user_tlahtolli'] = user_tlahtolli
    return jsonify(lesson_dict)

@bp.route('/lessons', methods=['GET'])
#@token_auth.login_required
def get_lessons():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 5, type=int), 100)
    data = Lesson.to_collection_dict(Lesson.query, page, per_page, 'api.get_lessons')
    return jsonify(data)

@bp.route('/lessons', methods=['POST'])
@token_auth.login_required
def create_lesson():
    data = request.get_json() or {}
    print("create lesson called")
    if 'title' not in data or 'content' not in data:
        return bad_request('must include title and content')
    if Lesson.query.filter_by(title=data['title']).first():
        return bad_request("there is already a lesson with that title")
#    if data['prev']:
#        previous = Lesson.query.filter_by(id=data['prev']).first()
#        if previous.next:
#            return bad_request('there is already a lesson after lesson {}, namely {}'.format(previous.id, previous.next))

    lesson = Lesson()
    lesson.from_dict(data)
    db.session.add(lesson)
#    if data['prev'] and not previous.next:
#            setattr(previous, next, data['id'])
    db.session.commit()
    #handle_lesson()
    response = jsonify(lesson.to_dict())
    response.status_code = 201
    print(lesson.id)
    response.headers['Location'] = url_for('api.get_lesson', id=lesson.id)
    return response

@bp.route('/lessons/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    data = request.get_json() or {}
    print('PUT request data: {}'.format(data))
    if g.current_user.id != lesson.author_id:
        return error_response(403)
    if 'title' in data and data['title'] != lesson.title and \
            Lesson.query.filter_by(title=data['title']).first():
        return bad_request('please use a different title')
    lesson.from_dict(data)
    user_tlahtolli = lesson.get_user_tlahtolli(g.current_user)
    lesson_dict = lesson.to_dict(include_content=True)
    lesson_dict['user_tlahtolli'] = user_tlahtolli
    print(lesson.content)
    db.session.commit()
    return jsonify(lesson_dict)

@bp.route('/lessons/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    if g.current_user.id != lesson.author_id:
        return error_response(403)
    db.session.delete(lesson)
    db.session.commit()
    return '', 204
