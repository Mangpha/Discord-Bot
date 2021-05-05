import pymysql
from pytz import timezone
from datetime import datetime
import os

sql_host = os.environ["SQL_HOST"]
sql_user = os.environ["SQL_USER"]
sql_passwd = os.environ["SQL_PASSWD"]
db_name = os.environ["DB_NAME"]
con = pymysql.connect(
    host=sql_host,
    user=sql_user,
    password=sql_passwd,
    charset="utf8",
    db=db_name,
    port=3306,
)


def join(userid, username):

    now = datetime.now(timezone("Asia/Seoul")).strftime("%Y:%m:%d %H:%M:%S")

    try:
        curs = con.cursor()
        sql = (
            "insert into discordapp(UserID, UserName, Level, Money, Exp, LostMoney, SigninDate)"
            f"values (%s, %s, %s, %s, %s, %s, '{now}');"
        )
        curs.execute(sql, (userid, username, 1, 10000, 0, 0))
        con.commit()

    finally:
        con.close()


def check_id(userid):
    try:
        curs = con.cursor()
        sql = "select * from discordapp where UserID=%s;"
        curs.execute(sql, userid)
        con.commit()
        rows = curs.fetchall()
        for row in rows:
            if row[0] is not None:
                check_bool = True
            else:
                check_bool = False
        user_dic = {
            "username": rows[0][1],
            "level": rows[0][2],
            "money": rows[0][3],
            "exp": rows[0][4],
            "lost_money": rows[0][5],
            "signin_date": rows[0][6],
        }
        return check_bool, user_dic

    finally:
        con.close()
