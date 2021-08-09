import json
from datetime import datetime

from flask import Blueprint, request, jsonify

from common.token_method import login_required, verify_token
from common import db

# 创建蓝图

params = Blueprint('params', __name__)


@params.route('/params/update', methods=['POST'])
@login_required
def update_params():
    userid = verify_token()
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    i_id = json_data['i_id']
    name = json_data['name']
    case = json_data['case']
    maxlength = json_data['maxlength'] or 'null'
    minlength = json_data['minlength'] or 'null'
    required = json_data['required']
    # if required:
    #     required = 1
    # else:
    #     required = 0
    option = json_data['option'] or 'null'
    # url = json_data['url']
    # 修改
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from params where id='{}'".format(_id)):
            _sql = "update params " \
                   "set name='{}',case1='{}',maxlength={},minlength={},required={},options={},updated_by={} " \
                   "where id={}".format(name, case, maxlength, minlength, required, option, userid, _id)
            e = db.change_db(_sql)
            if e:
                print(e)
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    # 新增
    ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _sql = '''insert into params 
            (name,case1,maxlength,minlength,required,options,i_id,created,created_by) 
            value ('%s','%s','%d','%d','%d','%s','%d','%s','%d')'''\
            % (name, case, maxlength, minlength, required, option, i_id, ctime, userid)
    e = db.change_db(_sql)
    if e:
        print(e)
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@params.route('/params/list', methods=['GET'])
@login_required
def params_list():
    """获取模型数据"""
    i_id = request.args.get("i_id")
    # json_data = json.loads(data)
    print(request)
    # i_id = json_data['i_id']
    where = "i_id=%s;" % i_id
    data = db.db_json('params', where, 'id', 'name', 'case1', 'maxlength', 'minlength',
                      'required', 'options', 'i_id', 'updated')
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

