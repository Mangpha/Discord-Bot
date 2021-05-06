import discord
from discord.ext import commands
import random
import requests
import json
import os
from games.user_sql import (
    signin,
    check_id,
    get_user,
    get_user_info,
    get_coin_price,
    buy_coin,
    sell_coin,
)

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
    UserName = ctx.message.author.name
    UserId = ctx.message.author.id
    boolean = check_id(UserId)
    if boolean is False:
        embed = discord.Embed(title="가입 실패", description="이미 가입된 유저입니다.")
        await ctx.send(embed=embed)
    else:
        signin(UserId, UserName)
        embed = discord.Embed(title="가입완료", description=UserName, color=0xC08282)
        embed.add_field(name="레벨", value="1", inline=True)
        embed.add_field(name="보유 금액", value=":moneybag: 10000", inline=True)
        embed.add_field(name="경험치", value="0", inline=False)
        await ctx.send(embed=embed)


@bot.command(help="게임 내 정보확인")
async def 내정보(ctx):
    UserId = ctx.message.author.id
    boolean = check_id(UserId)
    if boolean is False:
        user_info = get_user(UserId)
        username = user_info["username"]
        level = user_info["level"]
        money = user_info["money"]
        exp = user_info["exp"]
        lost_money = user_info["lost_money"]
        signin_date = user_info["signin_date"]
        embed = discord.Embed(title="유저 정보", description=username, color=0xC08282)
        embed.add_field(name="레벨", value=level, inline=True)
        embed.add_field(name="보유 금액", value=f":moneybag: {money}", inline=True)
        embed.add_field(name="경험치", value=exp, inline=True)
        embed.add_field(name="잃은 돈(코인 제외)", value=lost_money, inline=True)
        embed.add_field(name="가입 시간", value=signin_date, inline=True)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="오류", description="가입되지 않은 유저입니다.")
        await ctx.send(embed=embed)


@bot.command(help="도지 코인 조회, 매수, 매도")
async def 도지(ctx, option="도움", *, coin=0):
    userid = ctx.message.author.id
    coin_price = get_coin_price()
    coin_type = "doge"
    boolean = check_id(userid)
    if boolean is False:
        if option == "조회":
            embed = discord.Embed(title="조회", description="도지 코인", color=0xC08282)
            embed.add_field(name="가격", value=f":coin: {coin_price}")
            await ctx.send(embed=embed)

        if option == "매수":
            if coin == 0:
                embed = discord.Embed(
                    title="매수", description="매수량을 입력해주세요", color=0xC08282
                )
                embed.add_field(name="현재가", value=f":coin: {coin_price}")
                await ctx.send(embed=embed)

            if coin != 0 and type(coin) is int:
                result = buy_coin(userid, coin_type, coin)
                if result is False:
                    embed = discord.Embed(
                        title="매수", description="현재 보유 금액 부족", color=0xC08282
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title="매수", description="도지 코인", color=0xC08282
                    )
                    embed.add_field(name="현재가", value=f":coin: {coin_price}")
                    embed.add_field(name="매수 완료", value=f":coin: {coin} DOGE 구매완료")
                    await ctx.send(embed=embed)

        if option == "매도":
            if coin == 0:
                embed = discord.Embed(
                    title="매도", description="매도량을 입력해주세요", color=0xC08282
                )
                embed.add_field(name="현재가", value=f":coin: {coin_price}")
                await ctx.send(embed=embed)

            if coin != 0 and type(coin) is int:
                result = sell_coin(userid, coin_type, coin)
                if result is False:
                    embed = discord.Embed(
                        title="매도",
                        description="매도하려는 수량이 보유 수량보다 적거나 없습니다",
                        color=0xC08282,
                    )
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        title="매도", description="도지 코인", color=0xC08282
                    )
                    embed.add_field(name="현재가", value=f":coin: {coin_price}")
                    embed.add_field(name="매도 완료", value=f":coin: {coin} DOGE 판매완료")
                    await ctx.send(embed=embed)

        if option == "내코인":
            now_coin = get_user_info(userid, "doge")
            embed = discord.Embed(title="내 코인", description="도지 코인", color=0xC08282)
            embed.add_field(name="보유 수량", value=f":coin: {now_coin} DOGE 보유중")
            await ctx.send(embed=embed)

        if option == "도움":
            embed = discord.Embed(title="도지 코인", description="도움말")
            embed.add_field(name="조회", value="현재 도지 코인의 가격을 조회합니다")
            embed.add_field(
                name="매수",
                value=f"현재가 :coin: {coin_price}에 매수합니다 (변동 가능성 있음)",
                inline=False,
            )
            embed.add_field(
                name="매도",
                value=f"현재가 :coin: {coin_price}에 매도합니다 (변동 가능성 있음)",
                inline=False,
            )
            embed.add_field(name="내코인", value="현재 보유중인 코인을 조회합니다", inline=False)
            await ctx.send(embed=embed)

    else:
        embed = discord.Embed(
            title="가입 필요", description="가입 후에 이용가능합니다", color=0xC08282
        )
        await ctx.send(embed=embed)


bot.run(token)
