import pymysql


def get_db_conn():
    conn = pymysql.connect(
            host="127.0.0.1",            # 数据库地址
            port=3306,         # 端口（配置文件传入的是字符串格式，所以这里取值的时候，用getint的方法 ）
            user="root",            # 账号
            passwd="admin123",    # 密码
            database='demo',    # 要操作的数据库名
            # database=('test_cloud_user','test_commodity','test_manager','test_order'),
            charset='utf8'
                           )  # 指定编码格式
    return conn


def query_db(_sql):
    conn = get_db_conn()  # 获取连接
    cur = conn.cursor()  # 建立游标
    cur.execute(_sql)  # 执行sql
    conn.commit()
    result = cur.fetchall()  # 获取所有查询结果
    # print('数据库查询结果', result)
    cur.close()  # 关闭游标
    conn.close()  # 关闭连接
    return result  # 返回结果


def change_db(_sql, data=None):
    conn = get_db_conn()  # 获取连接
    cur = conn.cursor()  # 建立游标
    # noinspection PyBroadException
    try:
        if data:
            cur.executemany(_sql, data)
        else:
            cur.execute(_sql)  # 执行sql
        conn.commit()  # 提交更改
        # print("修改数据库成功")
    except Exception as e:
        conn.rollback()  # 回滚
        print(e)
        return e
    finally:
        cur.close()  # 关闭游标
        conn.close()  # 关闭连接0


def db_json(table, where=None, *arg):
    str_arg = str(arg).replace("'", '')
    str_arg = str_arg.replace("(", '')
    str_arg = str_arg.replace(")", '')
    if where:
        _sql = "select %s from %s where %s" % (str_arg, table, where)
    else:
        _sql = "select %s from %s " % (str_arg, table)
    d_datas = query_db(_sql)
    res = []
    for d_data in d_datas:
        temp = {}
        i = 0
        for key in arg:
            if i > len(d_data): return
            temp[key] = d_data[i]
            i += 1
        res.append(temp)
    return res


if __name__ == '__main__':
    i_id = 1
    where = "i_id='%s';" % i_id
    res = db_json('params', where, 'id', 'name', 'case1', 'maxlength', 'minlength',
                      'required', 'options', 'i_id', 'updated')
    print(res)