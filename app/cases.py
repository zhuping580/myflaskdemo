import json
from datetime import datetime

from flask import Blueprint, request, jsonify
import requests

from common.token_method import login_required, verify_token
from common import db
from common.modelFuntion import CreateCase

# 创建蓝图

cases = Blueprint('cases', __name__)


@cases.route('/cases/update', methods=['POST'])
@login_required
def update_cases():
    userid = verify_token()
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    priority = json_data['priority']
    title = json_data['title']
    enter = json_data['enter']
    outs = json_data['outs']
    updated_by = json_data['updated_by']
    if 'id' in json_data.keys():
        _id = json_data['id']
        if db.query_db("select * from cases where id='{}'".format(_id)) is not None:
            _sql = "update cases set priority='%s',title='%s',enter='%s',outs='%s',updated_by=%d where id='%d'" % \
                   (priority, title, enter, outs, updated_by, userid)
            e = db.change_db(_sql)
            if e:
                return jsonify(code=-1, message=u"操作失败")
            return jsonify(code=0, message=u"修改成功")
    # 新增
    ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    _sql = '''insert into cases (priority,title,enter,outs,created,created_by) value ('%s', '%s', '%s', '%s', '%d')'''\
           % (priority, title, enter, outs, ctime, userid)
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@cases.route('/cases/list', methods=['GET'])
@login_required
def cases_list():
    """获取模型数据"""
    # print('userid:', userid)
    print(request.args)
    i_id = int(request.args.get("i_id"))
    # pageSize = int(request.args.get("pageSize"))
    # pageNum = int(request.args.get("currentPage"))
    data = []
    database = db.query_db("select id,priority,title,enter,outs,result from cases where i_id=%d;" % i_id)
    for i in database:
        temp = {}
        temp['id'] = i[0]
        temp['priority'] = i[1]
        temp['title'] = i[2]
        temp['enter'] = i[3]
        temp['outs'] = i[4]
        temp['result'] = i[5]
        data.append(temp)

    return jsonify(code=0, message=u"success", data=data)


@cases.route('/cases/delete', methods=['POST'])
@login_required
def delete_cases():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)

    _id = json_data['id']
    _sql = "delete from cases where id=%d" % _id
    e = db.change_db(_sql)
    if e:
        return jsonify(code=-1, message=u"操作失败")
    return jsonify(code=0, message=u"success")


@cases.route('/cases/create', methods=['POST'])
@login_required
def create_case():
    userid = verify_token()
    data = request.get_data()
    json_data = json.loads(data)
    i_ids = json_data['i_id']
    print(i_ids)
    for i_id in i_ids:
        db_data = db.query_db(
            "select name,case1,maxlength,minlength,required,options from params where i_id=%d" % i_id
        )
        title = db.query_db("select name from interface where id=%d" % i_id)[0][0]
        module_data = []
        for i in db_data:
            temp = {}
            temp['name'] = i[0]
            temp['case1'] = i[1]
            temp['maxlength'] = i[2]
            temp['minlength'] = i[3]
            temp['required'] = i[4]
            temp['options'] = i[5]
            module_data.append(temp)
        cases_data = CreateCase(module_data, title).get_case()
        db.change_db("delete from cases where i_id=%d" % i_id)
        ctime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        insert_datas = []
        for k in cases_data:
            # print('用例', k)
            insert_data = []
            insert_data.append(i_id)
            for g in k:
                insert_data.append(str(k[g]))
            insert_data.append(ctime)
            insert_data.append(userid)
            insert_data.append('auto')
            insert_data = tuple(insert_data)
            insert_datas.append(insert_data)
        insert_datas = tuple(insert_datas)
        print('————————', insert_datas)
        _sql = "insert into cases (i_id,title,enter,outs,priority,created,created_by,type) " \
               "value (%s,%s,%s,%s,%s,%s,%s,%s)"
        e = db.change_db(_sql, insert_datas)
        print('e', e)

    return jsonify(code=0, message=u"success")


@cases.route('/cases/execute', methods=['POST'])
@login_required
def execute_cases():
    data = request.get_data()
    json_data = json.loads(data)
    print(json_data)
    if 'id' in json_data.keys:
        _id = json_data['id']
        cases = db.db_json('cases', 'id='+str(_id), 'title', 'enter', 'outs', 'i_id')
        i_id = cases[0]['i_id']
    elif 'i_id' in json_data.keys:
        i_id = json_data['i_id']
        cases = db.db_json('cases', 'id='+str(i_id), 'title', 'enter', 'outs', 'i_id')
    else:
        return jsonify(code=-1, message=u"参数错误")

    interface = db.db_json('interface', 'id='+str(i_id), 'methods', 'url', 'login_required')
    interface = interface[0]

    systems = db.db_json('systems', None, 's_key', 'val', 'type')
    url = ''
    headers = {}
    for i in systems:
        if i['s_key'] == 'url':
            url = i['val']
        elif i['s_key'] == 'token':
            headers['token'] = i['val']
        elif i['s_key'] == 'Cookie':
            headers['Cookie'] = i['val']

    for case in cases:
        if interface['methods'] == 'post':
            _result = requests.post(url=url+interface['url'], json=json.loads(case["enter"].replace("'", '"')), headers=headers)
        elif interface['methods'] == 'get':
            _result = requests.get(url=url+interface['url'], params=json.loads(case['enter'].replace("'", '"')), headers=headers)
        else:
            return jsonify(code=0, message=u"'不支持' + i_data['methods'] + '请求方式'")
        sql3 = "update cases set result ='%s' where id=%d" % (_result.text, _id)
        db.change_db(sql3)

    return jsonify(code=0, message=u"success")


def login():
    url = "http://192.168.3.66:9001/user/login/password"
    data = {
        "mobile": "18111111111",
        "password": "Sulongfei@123456",
        "mobileAraeCode": "+86",
        "regType": 0,
        "email": ""
    }
    response = requests.post(url=url, json=data)
    # print('请求头', response.request.headers)
    # print('请求体', response.request.body)
    # print('响应头', response.headers)
    cookie = response.headers['Set-Cookie']
    cookie = cookie.split(';', 1)[0]
    token = response.json()['data']['token']
    _sql = "update systems set val='%s' where s_key='Cookie'" % cookie
    db.change_db(_sql)
    _sql0 = "update systems set val='%s' where s_key='token'" % token
    db.change_db(_sql0)


if __name__ == '__main__':
    login()
