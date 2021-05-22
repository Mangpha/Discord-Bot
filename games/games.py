import random


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
