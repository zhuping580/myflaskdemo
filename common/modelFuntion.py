import copy
from common.data_transform import length_transform


class CreateCase:
    def __init__(self, goodDate, title):
        self.goodDate = goodDate
        self.title = title
        self.keys = self.goodDate.keys()
        self.case = []
        self.firstCase = {}
        self.first_case()
        self.foreach_item()

    def first_case(self):
        firstCase = self.firstCase
        enter = {}
        for key in self.keys:
            enter[key] = self.goodDate[key]['case']
        firstCase['title'] = self.title + "冒烟测试用例"
        firstCase['enter'] = enter
        firstCase['out'] = {'response': {'code': 200, 'msg': 'success'}}
        self.case.append(firstCase)

    def max_length(self, key, value):
        if "maxlength" not in value.keys():
            return
        maxlength = value["maxlength"]
        if not maxlength:
            return
        _case = value["case"]
        case21 = copy.deepcopy(self.firstCase)
        case21['title'] = self.title + key + "最大长度校验"
        _case = _case * (maxlength // len(_case) + 1)
        case21['enter'][key] = _case[0:maxlength - 1]
        case21['out'] = {'response': {'code': 200, 'msg': 'success'}}
        self.case.append(case21)
        case22 = copy.deepcopy(self.firstCase)
        case22['title'] = self.title + key + "最大长度校验"
        # _case = _case * (maxlength // len(_case) + 1)
        case22['enter'][key] = _case[0:maxlength]
        case22['out'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
        self.case.append(case22)

    def min_length(self, key, value):
        if "minlength" not in value.keys():
            return
        minlength = value["minlength"]
        if not minlength:
            return
        _case = value["case"]
        case21 = copy.deepcopy(self.firstCase)
        case21['title'] = self.title + key + "最小长度校验"
        case21['enter'][key] = _case[0: minlength - 1]
        case21['out'] = {'response': {'code': 200, 'msg': 'success'}}
        self.case.append(case21)
        case22 = copy.deepcopy(self.firstCase)
        case22['title'] = self.title + key + "最小长度校验"
        case22['enter'][key] = _case[0:minlength - 2]
        case22['out'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
        self.case.append(case22)

    def check_length(self, key, value):
        if "length" not in value.keys():
            return
        length = value["length"]
        _case = value["case"]
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
                    case2['out'] = {'response': {'code': 200, 'msg': 'success'}}
                elif _key == 'invalid':
                    case2['out'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
                self.case.append(case2)

    def check_required(self, key, value):
        if "required" not in value.keys():
            return
        case3 = copy.deepcopy(self.firstCase)
        case3['title'] = self.title + key + "必填校验"
        if value["required"]:
            case3['enter'][key] = ''
            case3['out'] = {'response': {'code': 'P00001', 'msg': 'fail'}}
        else:
            case3['enter'][key] = ''
            case3['out'] = {'response': {'code': 200, 'msg': 'success'}}
        self.case.append(case3)

    def select_option(self, key, value):
        if "option" not in value.keys():
            return
        for i in value["option"]:
            case4 = copy.deepcopy(self.firstCase)
            case4['title'] = self.title + key + "选项校验"
            case4["enter"][key] = i
            case4['out'] = {'response': {'code': 200, 'msg': 'success'}}
            self.case.append(case4)

    def foreach_item(self):
        for key in self.keys:
            self.check_length(key, self.goodDate[key])
            self.max_length(key, self.goodDate[key])
            self.min_length(key, self.goodDate[key])
            self.check_required(key, self.goodDate[key])
            self.select_option(key, self.goodDate[key])

    def get_case(self):
        return self.case

