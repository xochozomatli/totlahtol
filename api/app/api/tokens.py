from flask import jsonify, g, make_response, request, redirect
from app import db
from app.models import User
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.api.errors import bad_request, error_response
from pytz import timezone

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    tokens_dict = g.current_user.get_token() #Returns dict {token, token_expiration, refresh_token, refresh_token_expiration}
    response = jsonify({ 'token':tokens_dict['token'], 'token_expiration':tokens_dict['token_expiration']})
    response.set_cookie(
        key='refresh_token', value=tokens_dict['refresh_token'],
        expires=tokens_dict['refresh_token_expiration'], httponly=True)
    # response.headers.add('Set-Cookie','refresh_token='+tokens_dict['refresh_token']+'; Expires='+timezone('GMT').localize(tokens_dict['refresh_token_expiration']).strftime('%a, %d-%b-%Y %H:%M:%S %Z')+'; SameSite=Lax; Path=/')
    db.session.commit()
    return response
    
@bp.route('/verify-email/<token>', methods=['GET'])
def verify_user_email(token):
    user = User.verify_email(token)
    g.current_user = user
    if not user:
        return error_response(404)
    user.verified = True
    db.session.commit()
    return redirect(app.config['FRONTEND_URL'], code=303)

@bp.route('/refresh', methods=['GET'])
def refresh_token():
    if 'refresh_token' not in request.cookies:
        return bad_request('no refresh token found')
    tokens_dict = User.refresh(request.cookies['refresh_token'])
    if tokens_dict is None:
        return error_response(401)
    response = jsonify({ 'token':tokens_dict['token'], 'token_expiration':tokens_dict['token_expiration']})
    response.set_cookie(
        key='refresh_token', value=tokens_dict['refresh_token'],
        expires=tokens_dict['refresh_token_expiration'], httponly=True)
    db.session.commit()
    return response

@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
    g.current_user.revoke_token()
    db.session.commit()
    return '', 204
