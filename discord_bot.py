import discord
from discord.ext import commands
import random
import requests
import json
import os

token = os.environ["DISCORD_TOKEN"]

game = discord.Game("!!help")
bot = commands.Bot(command_prefix="!!")

user_db = {}


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
    embed = discord.Embed(title=kwargs, description=ans, color=0xF3BB76)
    await ctx.send(embed=embed)


@bot.command(help="Play Game")
async def signin(ctx):
    UserName = ctx.author.name
    UserId = ctx.author.id
    if UserId not in user_db:
        dic = {UserId: {"username": UserName, "level": 1, "money": 10000, "exp": 0}}
        user_db.update(dic)
        embed = discord.Embed(title="User Detail", description=user_db[UserId])
        embed.add_field(name="Level", value=user_db[UserId]["level"], inline=True)
        embed.add_field(name="Money", value=user_db[UserId]["money"], inline=True)
        embed.add_field(name="Exp", value=user_db[UserId]["exp"], inline=True)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Failed", description="User Valid")
        await ctx.send(embed=embed)


bot.run(token)
