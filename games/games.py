import random
from . import user_sql


def make_lotto():
    lotto_list = []
    for i in range(0, 6):
        lotto_num = random.randint(1, 46)
        while lotto_num in lotto_list:
            lotto_num = random.randint(1, 46)
        lotto_list.append(lotto_num)
    return sorted(lotto_list)


def users_lotto(args):
    try:
        # Type Error
        user_lotto = sorted(list(set(args)))

        if len(user_lotto) > 6:
            return False

        if len(user_lotto) != 6:
            for i in range(0, 6 - len(user_lotto)):
                user_lotto_num = random.randint(1, 46)
                while user_lotto_num in user_lotto:
                    user_lotto_num = random.randint(1, 46)
                user_lotto.append(user_lotto_num)

        return sorted(user_lotto)

    except TypeError:
        return False


def check_lotto(user, bots, userid):
    check = 0
    for i in range(0, len(bots)):
        if user[i] in bots:
            check += 1

    # apply n times to return value
    if check == 2:
        return 1

    if check == 3:
        return 2

    if check == 4:
        return 5

    if check == 5:
        return 10

    if check == 6:
        return 100

    else:
        user_sql.set_data(userid, "LostMoney", 500)
        return 0
