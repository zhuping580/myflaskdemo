from flask import Flask, redirect, session
from login import logins
from model import model
from user import users

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def hello_world():
    if 'username' in session:
        return redirect('/index')
    return redirect('/login')


@app.errorhandler(404)
def error(e):
    return '您请求的页面不存在了，请确认后再次访问！%s' % e


@app.route('/index')
def index():
    return 'index'


# 注册蓝图，第一个参数logins是蓝图对象，url_prefix参数默认值是根路由，如果指定，会在蓝图注册的路由url中添加前缀。
url_prefix = '/api/v1'
app.register_blueprint(logins, url_prefix=url_prefix)
app.register_blueprint(users, url_prefix=url_prefix)
app.register_blueprint(model, url_prefix=url_prefix)


if __name__ == '__main__':
    print(app.url_map)
    app.run(debug=True)
