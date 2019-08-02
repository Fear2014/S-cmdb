from django.http import JsonResponse
import pymysql

def inception_tools(data):
    sql = '/* --user=%s;--password=%s;--host=%s;--port=%s;--enable-check; */\
    inception_magic_start; \
    use %s;  \
    %s \
    inception_magic_commit;'% \
    (data.get('user'), data.get('password'), data.get('host'), data.get('port'), data.get('db_name'), data.get('sql_conent'))
    try:
        conn = pymysql.connect(host='127.0.0.1', user='', passwd='', db='', port=6669, use_unicode=True,
                               charset="utf8")  # inception的地址、端口等
        cur = conn.cursor()
        ret = cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        for res in result:
            if res[4] != 'None':
                result = res[4]
                status = 1
                return status, result
    except pymysql.Error as e:
        print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
    status = 0
    return status, result





