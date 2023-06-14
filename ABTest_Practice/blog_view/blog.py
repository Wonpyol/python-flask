from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for
from flask_login import login_user, logout_user, current_user
from blog_controller.user_mgmt import User
from blog_controller.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['POST'])
def set_email():
    print(request.form)  # form body data
    user = User.create(request.form.get('user_email'), request.form.get('A'))
    login_user(user, remember=True, duration=datetime.timedelta(days=365))  # 세션 아이디 정보 등록

    return redirect(url_for('blog.test_blog'))


@blog_abtest.route('/test_blog')
def test_blog():
    if current_user.is_authenticated:
        return render_template('blog_A.html', user_email=current_user.user_email)
    else:
        return render_template('blog_A.html')


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return render_template('blog_A.html')


@blog_abtest.route('/blog_golf')
def blog_golf():
    BlogSession.get_blog_page()

