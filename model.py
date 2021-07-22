import json
from flask import Blueprint, request, jsonify, redirect, session
from common.readYaml import ReadYaml

# 创建蓝图
model = Blueprint('model', __name__)


@model.route('/model/update', methods=['POST'])
def update_model():
    """新增模型"""
    data = request.get_data()
    json_data = json.loads(data)
    modelName = json_data['modelName']
    rule = json_data['rules']
    ReadYaml(modelName+"数据原型.yml").writer_yaml(rule)
    return jsonify(code=0, message=u"success")






