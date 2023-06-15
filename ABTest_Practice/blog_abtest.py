from flask import Flask, jsonify, make_response, session, request
from flask_login import LoginManager
from flask_cors import CORS

from blog_controller.user_mgmt import User
from blog_view import blog
import os

# https 만을 지원 하는 기능을 http 에서 테스트 할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

app = Flask(__name__, static_url_path='/static')
CORS(app)
# 세션을 별도로 관리 안하기 때문에 고정함
app.secret_key = 'wonpyol_server3'
app.register_blueprint(blog.blog_abtest, url_prefix='/blog')

login_manager = LoginManager()
login_manager.init_app(app)
# 세션 보안 레벨
login_manager.session_protection = 'strong'


# 로그인 유저 객체 생성
@login_manager.user_loader
def load_user(user_id): # 세션의 로긴 아이디
    return User.get(user_id)


# 인증 오류 핸들러
@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(succes=False), 401)


@app.before_request
def app_before_request():
    if 'client_id' not in session:
        session['client_id'] = request.environ.get("HTTP_X_REAL_IP", request.remote_addr)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
