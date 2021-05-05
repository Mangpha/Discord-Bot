import discord
from discord.ext import commands
import random
import requests
import json
import os
import pymysql
from pytz import timezone
from datetime import datetime

token = os.environ["DISCORD_TOKEN"]

game = discord.Game("!!help")
bot = commands.Bot(command_prefix="!!")

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
curs = con.cursor()


def signin(userid, username):

    """ Game Signin """

    now = datetime.now(timezone("Asia/Seoul")).strftime("%Y:%m:%d %H:%M:%S")
    sql = (
        "insert into discordapp(UserID, UserName, Level, Money, Exp, LostMoney, SigninDate)"
        f"values (%s, %s, %s, %s, %s, %s, '{now}');"
    )
    curs.execute(sql, (userid, username, 1, 10000, 0, 0))
    con.commit()


def check_id(userid):

    """ Check ID , Get User Data """

    check_bool = True
    sql = "select * from discordapp where UserID=%s;"
    curs.execute(sql, userid)
    con.commit()
    rows = curs.fetchall()
    if not (rows):
        check_bool = True
        user_dic = {}
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


@bot.event
async def on_ready():
    print(bot.user.name)
    await bot.change_presence(status=discord.Status.online, activity=game)


@bot.command(help="데스티니 활동 랜덤 추천")
async def 추천좀(ctx):
    ran_list = [
        "레이드",
        "예언",
        "선각자",
        "예지",
        "이단의 구덩이",
        "조각난 왕관",
        "갬빗",
        "시련의 장",
        "전장",
        "선봉대 공격전",
        "황혼전: 시련",
        "종료",
        "슬픔의 제단",
        "업적작",
        "탑 공굴리기 & 용암도전",
    ]
    em = discord.Embed(title="데스티니 가디언즈 활동 추천", description="", color=0xF3BB76)
    em.add_field(name="추천 결과", value=random.choice(ran_list))
    await ctx.send(embed=em)


@bot.command(help="한강 수온 체크")
async def 한강물온도(ctx):
    hangang_api = "https://api.hangang.msub.kr/"
    embed = discord.Embed(title="한강 물 온도 체크", description="", color=0xF3BB76)
    res = requests.get(hangang_api)
    res_json = json.loads(res.text)
    temp = res_json["temp"]
    time = res_json["time"]
    embed.add_field(name="시간", value=time, inline=True)
    embed.add_field(name="온도", value=temp, inline=True)
    await ctx.send(embed=embed)


@bot.command(help="소라고동")
async def 소라고동님(ctx, *, kwargs):
    ans = random.choice(["Yes", "No"])
    emj_list = [
        ":laughing:",
        ":blush:",
        ":smile:",
        ":sweat_smile:",
        ":upside_down:",
        ":yum:",
        ":stuck_out_tongue_closed_eyes:",
        ":zany_face:",
        ":pensive:",
        ":frowning2:",
        ":thinking:",
    ]
    emoji = random.choice(emj_list)
    embed = discord.Embed(
        title=kwargs, description=f"{emoji} {ans} {emoji}", color=0xF3BB76
    )
    await ctx.send(embed=embed)


@bot.command(help="게임 가입")
async def 가입(ctx):
    UserName = ctx.author.name
    UserId = ctx.author.id
    boolean = check_id(UserId)[0]
    if boolean is True:
        signin(UserId, UserName)
        embed = discord.Embed(title="가입완료", description=UserName, color=0xC08282)
        embed.add_field(name="레벨", value="1", inline=True)
        embed.add_field(name="보유 금액", value=":moneybag: 10000", inline=True)
        embed.add_field(name="경험치", value="0", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="가입 실패", description="이미 가입된 유저입니다.")
        await ctx.send(embed=embed)


@bot.command(help="게임 내 정보확인")
async def 내정보(ctx):
    UserId = ctx.author.id
    storage = check_id(UserId)
    boolean = storage[0]
    if boolean is False:
        user_info = storage[1]
        username = user_info["username"]
        level = user_info["level"]
        money = user_info["money"]
        exp = user_info["exp"]
        lost_money = user_info["lost_money"]
        signin_date = user_info["signin_date"]
        embed = discord.Embed(title="유저 정보", description=username, color=0xC08282)
        embed.add_field(name="레벨", value=level, inline=True)
        embed.add_field(name="보유 금액", value=money, inline=True)
        embed.add_field(name="경험치", value=exp, inline=True)
        embed.add_field(name="잃은 돈", value=lost_money, inline=True)
        embed.add_field(name="가입 시간", value=signin_date, inline=True)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="오류", description="가입되지 않은 유저입니다.")
        await ctx.send(embed=embed)


bot.run(token)
