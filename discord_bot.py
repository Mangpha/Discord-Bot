import discord
from discord.ext import commands
import random
import requests
import json
import os
from games import join as sql_join

token = os.environ["DISCORD_TOKEN"]

game = discord.Game("!!help")
bot = commands.Bot(command_prefix="!!")


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
    sql_join.join(UserId, UserName)
    boolean = sql_join.check_id(UserId)[0]
    if boolean is False:
        embed = discord.Embed(title="가입완료", description=UserName, color=0xC08282)
        embed.add_field(name="레벨", value=":one:", inline=True)
        embed.add_field(name="보유 금액", value=":moneybag: 10000", inline=True)
        embed.add_field(name="경험치", value="0", inline=False)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="가입 실패", description="이미 가입된 유저입니다.")
        await ctx.send(embed=embed)


@bot.command(help="게임 내 정보확인")
async def 내정보(ctx):
    UserId = ctx.author.id
    storage = sql_join.check_id(UserId)
    boolean = storage[0]
    user_info = storage[1]
    if boolean is False:
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
