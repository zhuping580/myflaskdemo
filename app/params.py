import json

from flask import Blueprint, request, jsonify

from common.token_method import login_required
from common import db

# 创建蓝图

params = Blueprint('params', __name__)


@params.route('/params/update', methods=['POST'])
@login_required
def update_params():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    i_id = json_data['i_id']
    name = json_data['name']
    case = json_data['case']
    maxlenght = json_data['maxlenght']
    minlenght = json_data['minlenght']
    required = json_data['required']
    option = json_data['option']
    url = json_data['url']
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from params where id='{}'".format(_id)):
            _sql = "update params set name='%s',case='%s',maxlenght='%d',minlenght='%d',required='%s',option='%s' " \
                   "where id='%d'" \
                   % (name, case, maxlenght, minlenght, required, option, _id)
            e = db.change_db(_sql)
            if e:
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    _sql = '''insert into params (name,case,maxlenght,minlenght,required,option,i_id) value ('%s', '%s', '%s')'''\
           % (name, case, maxlenght, minlenght, required, option, i_id)
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@params.route('/params/list', methods=['GET'])
@login_required
def params_list():
    """获取模型数据"""
    data = []
    database = db.query_db('''select id,name,case,maxlenght,minlenght,required,option,i_id from params''')
    for i in database:
        temp = {}
        temp['id'] = i[0]
        temp['name'] = i[1]
        temp['case'] = i[2]
        temp['maxlenght'] = i[3]
        temp['minlenght'] = i[4]
        temp['required'] = i[5]
        temp['option'] = i[6]
        temp['i_id'] = i[7]
        data.append(temp)

    return jsonify(code=0, message=u"success", data=data)


@params.route('/params/delete', methods=['POST'])
@login_required
def delete_params():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    _id = json_data['id']
    _sql = "delete from params where id='%d'" % _id
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")

