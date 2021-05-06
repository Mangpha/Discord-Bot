import mysql.connector
from pytz import timezone
from datetime import datetime
import os
import pyupbit


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


def get_user_info(userid, column):

    """ Get User's Info (Money, Coin, Etc) """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    sql = f"select {column} from discordapp where UserID = %s ;"
    curs.execute(
        sql,
        (userid,),
    )
    rows = curs.fetchall()
    return rows[0][0]


def get_coin_doge():
    return pyupbit.get_current_price("KRW-DOGE")


def get_coin_btt():
    return pyupbit.get_current_price("KRW-BTT")


def buy_coin(userid, coin_type, b_coin):

    """ Buy Coin : input Coin Type """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    now_money = float(get_user_info(userid, "money"))
    now_coin = int(get_user_info(userid, coin_type))

    if coin_type == "doge":
        coin_price = float(get_coin_doge())
    if coin_type == "btt":
        coin_price = float(get_coin_btt())

    if now_money < coin_price * b_coin:
        return False
    else:
        sql = "update discordapp set money=%s-(%s*%s) where (UserID=%s) ;"
        curs.execute(
            sql,
            (now_money, coin_price, b_coin, userid),
        )
        con.commit()
        sql = f"update discordapp set {coin_type}=%s+%s where (UserID=%s);"
        curs.execute(
            sql,
            (
                now_coin,
                b_coin,
                userid,
            ),
        )
        con.commit()
        return True


def sell_coin(userid, coin_type, b_coin):

    """ Sell Coin: Input Coin Type """

    con = mysql.connector.connect(**db_connection())
    curs = con.cursor()
    now_money = float(get_user_info(userid, "money"))
    now_coin = int(get_user_info(userid, coin_type))

    if coin_type == "doge":
        coin_price = float(get_coin_doge())
    if coin_type == "btt":
        coin_price = float(get_coin_btt())

    if now_coin < b_coin:
        return False

    else:
        sql = "update discordapp set money=%s+(%s*%s) where (UserID=%s);"
        curs.execute(
            sql,
            (
                now_money,
                coin_price,
                b_coin,
                userid,
            ),
        )
        con.commit()
        sql = f"update discordapp set {coin_type}=%s-%s where (UserID=%s);"
        curs.execute(
            sql,
            (
                now_coin,
                b_coin,
                userid,
            ),
        )
        con.commit()
        return True
