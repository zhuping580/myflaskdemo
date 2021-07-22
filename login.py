import json
from flask import Blueprint, request, jsonify, redirect, session
import db
from common import token_method

# 创建蓝图
logins = Blueprint('login', __name__)


@logins.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        """登录"""
        data = request.get_data()
        json_data = json.loads(data)
        username = json_data['username']
        password = json_data['password']
        sql0 = "select password from users where name='%s'" % username
        db_password = db.query_db(sql0)

        # ""  0  [] () {} None 在逻辑判断时都是假
        if not all([username, password]):
            # 表示name或password中有一个为空或者都为空
            return jsonify(code=1, message=u"参数不完整")

        if db_password:
            if db_password[0][0] == password:
                db_id = db.query_db("select id from users where name='%s'" % username)
                token = token_method.create_token(db_id)
                return jsonify(code=0, data={"user": username, "message": u"success", "token": token})
            else:
                return jsonify(code=2, message=u"用户名或密码错误")
        else:
            return jsonify(code=3, message=u"用户未注册")
    else:
        return 'show_the_login_form()'





