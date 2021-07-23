import json
import os

from flask import Blueprint, request, jsonify
from common.readYaml import ReadYaml
from common.modelFuntion import CreateCase
from common.token_method import login_required

# 创建蓝图
from configs.common import project_path

model = Blueprint('model', __name__)


@model.route('/model/update', methods=['POST'])
@login_required
def update_model():
    """新增模型"""
    data = request.get_data()
    json_data = json.loads(data)
    modelName = json_data['modelName']
    rule = json_data['rules']
    ReadYaml(r"\\model\\"+modelName+"数据原型.yml").writer_yaml(rule)
    return jsonify(code=0, message=u"success")


@model.route('/model/list', methods=['GET'])
@login_required
def model_list():
    """获取模型数据"""
    data = []
    dirs = os.listdir(project_path + r"\\yaml\\model")
    for _dir in dirs:
        temp = ReadYaml(r"\\model\\" + _dir).get_yaml_data()
        data.append(temp)
    return jsonify(code=0, message=u"success", data=data)


@model.route('/model/creat_api_case', methods=['POST'])
@login_required
def creat_api_case():
    """生成接口测试用例"""
    data = request.get_data()
    json_data = json.loads(data)
    modelName = json_data['modelName']
    temp = ReadYaml(r"\\model\\" + modelName + "数据原型.yml").get_yaml_data()
    title = modelName
    case_data = CreateCase(temp, title).get_case()
    ReadYaml(r"api_case\\"+modelName+"接口测试用例.yml").writer_yaml(case_data)
    return jsonify(code=0, message=u"success")

