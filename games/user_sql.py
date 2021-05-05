import mysql.connector
from pytz import timezone
from datetime import datetime
import os


def db_connection():
    sql_host = os.environ["SQL_HOST"]
    sql_user = os.environ["SQL_USER"]
    sql_passwd = os.environ["SQL_PASSWD"]
    db_name = os.environ["DB_NAME"]
    db_config = {
        "host": sql_host,
        "user": sql_user,
        "password": sql_passwd,
        "database": db_name,
        "port": 3306,
    }
    return db_config


def signin(userid, username):

    """ Game Signin """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    now = datetime.now(timezone("Asia/Seoul")).strftime("%Y:%m:%d %H:%M:%S")
    sql = (
        "insert into discordapp(UserID, UserName, Level, Money, Exp, LostMoney, SigninDate)"
        f"values (%s, %s, %s, %s, %s, %s, '{now}') ;"
    )
    curs.execute(
        sql,
        (
            userid,
            username,
            1,
            10000,
            0,
            0,
        ),
    )
    con.commit()


def check_id(userid):

    """ Check ID """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    sql = "select exists(select * from discordapp where UserID = %s) ;"
    curs.execute(sql, (userid,))
    isDup = curs.fetchall()
    if isDup[0][0] == 1:
        # Exist
        return bool(False)
    else:
        return bool(True)


def get_user(userid):

    """ Get User Data """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    sql = "select * from discordapp where UserID = %s ;"
    curs.execute(sql, (userid,))
    rows = curs.fetchall()
    user_dic = {
        "username": rows[0][1],
        "level": rows[0][2],
        "money": rows[0][3],
        "exp": rows[0][4],
        "lost_money": rows[0][5],
        "signin_date": rows[0][6],
    }
    return user_dic
