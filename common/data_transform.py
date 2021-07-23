from common.response import ResMsg

def length_transform(length):
    valid = []
    invalid = []
    a1, a2 = length.split(',')
    if '[' in a1:
        int_a1 = int(a1.replace('[', ''))
        valid.append(int_a1)
        if int_a1 != 0:
            invalid.append(int_a1 - 1)
    elif '(' in a1:
        int_a1 = int(a1.replace('(', ''))
        valid.append(int_a1 + 1)
        invalid.append(int_a1)
    if ']' in a2:
        int_a2 = int(a2.replace(']', ''))
        valid.append(int_a2)
        invalid.append(int_a2 + 1)
    elif ')' in a2:
        int_a2 = int(a2.replace(')', ''))
        valid.append(int_a2 - 1)
        invalid.append(int_a2)
    dict1 = {'valid': valid, 'invalid': invalid}
    return dict1


class RequestParser:
    def __init__(self, jsonData: dict):
        self.data = jsonData

    def check_param(self, name, datatype=str, required=False, info=None):
        res = ResMsg()
        value = ''
        if name not in self.data.keys():
            res.update(code=-1, msg="缺少" + name + "参数")
            return res.data
        value = self.data[name]
        if not value and required:
            res.update(code=-1, msg=name + "参数必填")
        print(type(value), datatype)
        print(type(value) == str)
        # print(isinstance(value, datatype))
        # elif type(value) != datatype:
        #     res.update(code=-1, msg=name + "参数类型不是" + datatype)
        # return res.data


if __name__ == '__main__':
    a = length_transform("[0,2000]")
    print(a)