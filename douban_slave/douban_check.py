import redis
import pymysql

redis_client = redis.StrictRedis(host='localhost', port=6379, db=1)
mysql_client = pymysql.connect(host='localhost', user='root', password='Dominic233', db='python_project', charset='utf8')
cursor = mysql_client.cursor()

while redis_client.scard('test'):
    data = redis_client.spop('test').decode('utf8')
    sql = "select id from books where id='%s'" % data
    cursor.execute(sql)
    if not cursor.fetchone():
        redis_client.lpush('bookspider:start_urls', 'https://book.douban.com/subject/'+data+'/')
