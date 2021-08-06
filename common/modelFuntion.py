import copy
from common.data_transform import length_transform


class CreateCase:
    def __init__(self, goodDate, title):
        self.goodDate = goodDate
        self.title = title
        self.keys = self.goodDate
        self.case = []
        self.firstCase = {}

    def first_case(self):
        firstCase = self.firstCase
        enter = {}
        for good in self.goodDate:
            key = good['name']
            enter[key] = good['case1']
        firstCase['title'] = self.title + "冒烟测试用例"
        firstCase['enter'] = enter
        firstCase['outs'] = {'response': {'code': 200, 'msg': 'success'}}
        firstCase['priority'] = "P0"
        self.case.append(firstCase)

    def check_token(self, good):
        if "login_required" not in good.keys():
            return
        if good["login_required"]:
            case11 = copy.deepcopy(self.firstCase)
            case11['title'] = self.title + "登录校验"
            case11['outs'] = {'response': {'code': 401}}

    def max_length(self, good):
        if "maxlength" not in good.keys():
            return
        maxlength = good["maxlength"]
        if not maxlength:
            return
        _case = good["case1"]
        key = good["name"]
        case21 = copy.deepcopy(self.firstCase)
        case21['title'] = self.title + key + "最大长度校验"
        _case = _case * (maxlength // len(_case) + 1)
        case21['enter'][key] = _case[0:maxlength - 1]
        case21['outs'] = {'response': {'code': 200, 'msg': 'success'}}
        case21['priority'] = "P1"
        self.case.append(case21)
        case22 = copy.deepcopy(self.firstCase)
        case22['title'] = self.title + key + "最大长度校验"
        # _case = _case * (maxlength // len(_case) + 1)
        case22['enter'][key] = _case[0:maxlength]
        case22['outs'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
        case22['priority'] = "P2"
        self.case.append(case22)

    def min_length(self, good):
        if "minlength" not in good.keys():
            return
        minlength = good["minlength"]
        if not minlength:
            return
        _case = good["case1"]
        key = good["name"]
        case21 = copy.deepcopy(self.firstCase)
        case21['title'] = self.title + key + "最小长度校验"
        case21['enter'][key] = _case[0: minlength - 1]
        case21['outs'] = {'response': {'code': 200, 'msg': 'success'}}
        case21['priority'] = "P1"
        self.case.append(case21)
        case22 = copy.deepcopy(self.firstCase)
        case22['title'] = self.title + key + "最小长度校验"
        case22['enter'][key] = _case[0:minlength - 2]
        case22['outs'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
        case22['priority'] = "P2"
        self.case.append(case22)

    def check_length(self, good):
        if "length" not in good.keys():
            return
        length = good["length"]
        _case = good["case1"]
        key = good["name"]
        length_data = length_transform(length)
        for _key in length_data.keys():
            for i in length_data[_key]:
                case2 = copy.deepcopy(self.firstCase)
                case2['title'] = self.title + key + "长度校验"
                if len(_case) >= i:
                    if i == 0:
                        case2['enter'][key] = ''
                    else:
                        case2['enter'][key] = _case[0:i - 1]
                else:
                    _case = _case * (i // len(_case) + 1)
                    case2['enter'][key] = _case[0:i - 1]
                if _key == 'valid':
                    case2['outs'] = {'response': {'code': 200, 'msg': 'success'}}
                elif _key == 'invalid':
                    case2['outs'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
                self.case.append(case2)

    def check_required(self, good):
        if "required" not in good.keys():
            return
        case3 = copy.deepcopy(self.firstCase)
        key = good["name"]
        case3['title'] = self.title + key + "必填校验"
        if good["required"]:
            case3['enter'][key] = ''
            case3['outs'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
            case3['priority'] = "P1"
        else:
            case3['enter'][key] = ''
            case3['outs'] = {'response': {'code': 200, 'msg': 'success'}}
            case3['priority'] = "P1"
        self.case.append(case3)

    def select_option(self, good):
        if "option" not in good.keys():
            return
        key = good["name"]
        for i in good["option"]:
            case4 = copy.deepcopy(self.firstCase)
            case4['title'] = self.title + key + "选项校验"
            case4["enter"][key] = i
            case4['outs'] = {'response': {'code': 200, 'msg': 'success'}}
            case4['priority'] = "P3"
            self.case.append(case4)

    def foreach_item(self):
        for good in self.goodDate:
            self.check_length(good)
            self.max_length(good)
            self.min_length(good)
            self.check_required(good)
            self.select_option(good)

    def get_case(self):
        self.first_case()
        self.foreach_item()
        return self.case

