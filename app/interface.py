import json

from flask import Blueprint, request, jsonify

from common.token_method import login_required
from common import db

# 创建蓝图

interface = Blueprint('interface', __name__)


@interface.route('/interface/update', methods=['POST'])
@login_required
def update_interface():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    name = json_data['name']
    methods = json_data['methods']
    url = json_data['url']
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from interface where id='{}'".format(_id)):
            _sql = "update interface set name='%s',methods='%s',url='%s' where id='%d'" % (name, methods, url, _id)
            e = db.change_db(_sql)
            if e:
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    _sql = '''insert into interface (name, methods, url) value ('%s', '%s', '%s')'''\
           % (name, methods, url)
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@interface.route('/interface/list', methods=['GET'])
@login_required
def interface_list():
    """获取模型数据"""
    data = []
    database = db.query_db('''select id,name,methods,url from interface''')
    for i in database:
        temp = {}
        temp['id'] = i[0]
        temp['name'] = i[1]
        temp['methods'] = i[2]
        temp['url'] = i[3]
        data.append(temp)

    return jsonify(code=0, message=u"success", data=data)


@interface.route('/interface/delete', methods=['POST'])
@login_required
def delete_interface():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    _id = json_data['id']
    _sql = "delete from interface where id='%d'" % _id
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")

