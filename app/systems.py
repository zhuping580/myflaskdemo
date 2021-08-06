import json
from datetime import datetime

from flask import Blueprint, request, jsonify

from common.token_method import login_required, verify_token
from common import db

# 创建蓝图

systems = Blueprint('systems', __name__)


@systems.route('/systems/update', methods=['POST'])
@login_required
def update_systems():
    userid = verify_token()
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    key = json_data['key']
    val = json_data['val']
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from systems where id='{}'".format(_id)):
            _sql = "update systems set s_key='%s',val='%s',updated_by=%d where id='%d'" % \
                   (key, val, userid, _id)
            e = db.change_db(_sql)
            if e:
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    # 新增
    ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _sql = '''insert into systems (s_key, val, created, created_by) value ('%s', '%s', '%s', '%d')'''\
           % (key, val, ctime, userid)
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@systems.route('/systems/list', methods=['GET'])
@login_required
def systems_list():
    """获取模型数据"""
    # print('userid:', userid)
    print(request.args)
    pageSize = int(request.args.get("pageSize") or 10)
    pageNum = int(request.args.get("currentPage") or 1)
    data = []
    totals = db.query_db("select count(*) from systems")
    database = db.query_db("select id,s_key,val from systems limit %d,%d;"
                           % (pageSize*(pageNum-1), pageSize))
    for i in database:
        temp = {}
        temp['id'] = i[0]
        temp['key'] = i[1]
        temp['val'] = i[2]
        data.append(temp)

    return jsonify(code=0, message=u"success", totals=totals[0][0], data=data)


@systems.route('/systems/delete', methods=['POST'])
@login_required
def delete_systems():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    _id = json_data['id']
    _sql = "delete from systems where id='%d'" % _id
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


