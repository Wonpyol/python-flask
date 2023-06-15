from flask import Blueprint, request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from blog_controller.user_mgmt import User
from blog_controller.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['POST'])
def set_email():
    print(request.form)  # form body data
    user = User.create(request.form.get('user_email'), request.form.get('blog_id'))
    login_user(user, remember=True, duration=datetime.timedelta(days=365))  # 세션 아이디 정보 등록

    return redirect(url_for('blog.blog_golf'))


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.blog_golf'))


@blog_abtest.route('/blog_golf')
def blog_golf():
    if current_user.is_authenticated:
        user = User.get(current_user.id)
        BlogSession.save_session_info(session['client_id'], current_user.user_email, user.blog_id)
        page_name = BlogSession.get_blog_page(user.blog_id)
        return render_template(page_name, user_email=current_user.user_email)
    else:
        page_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'anonymous', page_name)
        return render_template(page_name)


