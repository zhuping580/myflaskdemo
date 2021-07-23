

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


if __name__ == '__main__':
    a = length_transform("[0,2000]")
    print(a)