import json
from flask import Blueprint, request, jsonify
from common.token_method import login_required, verify_token
from common import db
# 创建蓝图，第一个参数指定了蓝图的名字。
users = Blueprint('user', __name__)


@users.route('/user/info', methods=['GET'])
@login_required
def user_info():
    # token = request.headers["token"]
    # 拿到token，去换取用户信息
    user_id = verify_token()
    _sql = "select * from users where id=" + str(user_id)
    user = db.query_db(_sql)
    data = {
        "id": user[0][0],
        "name": user[0][1],
        "password": user[0][2]
    }

    return jsonify(code=0, msg="成功", data=data)


@users.route('/user/addUser', methods=['POST'])
@login_required
def add_user():
    data = request.get_data()
    json_data = json.loads(data)
    name = json_data['name']
    password = json_data['password']
    if not all([name.strip(), password.strip()]):
        # 表示name或password中有一个为空或者都为空
        return jsonify(code=1, message=u"参数不完整")
    sql0 = """select * from users where name='%s'""" % name
    if db.query_db(sql0):
        return jsonify(code=2, message=u"用户已存在")
    _sql = """insert into users (name, password) values ('%s','%s')""" % (name, password)
    db.change_db(_sql)
    return jsonify(code=0, message=u"添加用户成功")


@users.route('/user/deleteUser', methods=['POST'])
@login_required
def delete_user():
    token = request.headers["token"]
    # 拿到token，去换取用户信息
    user_id = verify_token(token)
    if user_id != 1:
        return jsonify(code=1, message=u"用户权限不够")
    data = request.get_data()
    json_data = json.loads(data)
    _id = json_data['id']
    if _id == 1:
        return jsonify(code=2, message=u"管理员不能删除")
    _sql = "delete from users where id=" + str(_id)
    db.query_db(_sql)
    return jsonify(code=0, message=u"删除用户成功")


@users.route('/user/list', methods=['GET'])
@login_required
def user_list():
    _sql = "select * from users"
    data = db.query_db(_sql)
    ret = []
    for i in data:
        tmp = {'id': i[0], 'name': i[1], 'password': i[2]}
        ret.append(tmp)
    return jsonify(code=0, message=u"查询成功", data=ret)


@users.route('/user/findUser', methods=['GET'])
@login_required
def user_find():
    name = request.args.get("name")
    _sql = "select id,name from users where name like '{}'".format(name)
    data = db.query_db(_sql)
    ret = []
    for i in data:
        tmp = {'id': i[0], 'name': i[1]}
        ret.append(tmp)
    return jsonify(code=0, message=u"查询成功", data=ret)
