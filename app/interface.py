import json
from datetime import datetime

from flask import Blueprint, request, jsonify

from common.token_method import login_required, verify_token
from common import db

# 创建蓝图

interface = Blueprint('interface', __name__)


@interface.route('/interface/update', methods=['POST'])
@login_required
def update_interface():
    userid = verify_token()
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    name = json_data['name']
    methods = json_data['methods']
    url = json_data['url']
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from interface where id='{}'".format(_id)):
            _sql = "update interface set name='%s',methods='%s',url='%s',updated_by=%d where id='%d'" % \
                   (name, methods, url, userid, _id)
            e = db.change_db(_sql)
            if e:
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    # 新增
    ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _sql = '''insert into interface (name, methods, url, created, created_by) value ('%s', '%s', '%s', '%s', '%d')'''\
           % (name, methods, url, ctime, userid)
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@interface.route('/interface/list', methods=['GET'])
@login_required
def interface_list():
    """获取模型数据"""
    # print('userid:', userid)
    print(request.args)
    pageSize = int(request.args.get("pageSize"))
    pageNum = int(request.args.get("currentPage"))
    data = []
    totals = db.query_db("select count(*) from interface")
    database = db.query_db("select id,name,methods,url from interface limit %d,%d;"
                           % (pageSize*(pageNum-1), pageSize))
    for i in database:
        temp = {}
        temp['id'] = i[0]
        temp['name'] = i[1]
        temp['methods'] = i[2]
        temp['url'] = i[3]
        _data = db.query_db(
            "select name from params where i_id={}".format(i[0])
        )
        array = []
        for j in _data:
            for k in j:
                array.append(k)
        temp['params'] = array
        data.append(temp)

    return jsonify(code=0, message=u"success", totals=totals[0][0], data=data)


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


