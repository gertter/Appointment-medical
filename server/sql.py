import pymysql
from hospital.settings import DATABASES
def Sql(time_sure,clinic,date):
    conn = pymysql.connect(host=DATABASES['default']['HOST'],user=DATABASES['default']['USER'],passwd=DATABASES['default']['PASSWORD'],port=3306,db=DATABASES['default']['NAME'],charset="utf8")
    cur=conn.cursor()
    cur.execute("update server_time set %s='Unavailable',`key`='yes' Where Radio='%s' and date='%s'"%(time_sure,clinic,date))
    conn.commit()
    conn.close()
    cur.close()
def Sql_pro(key,name):
    if key=='':
        pass
    else:
        conn=pymysql.connect(host=DATABASES['default']['HOST'],user=DATABASES['default']['USER'],passwd=DATABASES['default']['PASSWORD'],port=3306,db=DATABASES['default']['NAME'],charset="utf8")
        cur=conn.cursor()
        cur.execute("update server_clinic_info set %s='1' Where name='%s'"%(key,name))
        conn.commit()
        conn.close()
        cur.close()
def Sql_No(key,name):
    conn = pymysql.connect(host=DATABASES['default']['HOST'],user=DATABASES['default']['USER'],passwd=DATABASES['default']['PASSWORD'],port=3306,db=DATABASES['default']['NAME'],charset="utf8")
    cur=conn.cursor()
    cur.execute("update server_clinic_info set %s='0' Where name='%s'"%(key,name))
    conn.commit()
    conn.close()
    cur.close()