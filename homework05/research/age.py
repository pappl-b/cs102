import datetime as dt
import statistics
import typing as tp

from dateutil.relativedelta import relativedelta

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    age_list = []
    friends_list = get_friends(user_id, fields=["bdate"])
    for friend in friends_list.items:
        try:
            bdate = dt.datetime.strptime(friend["bdate"], "%d.%m.%Y")
            age_list.append(relativedelta(dt.datetime.now(), bdate).years)
        except (KeyError, ValueError):
            continue
    if len(age_list) == 0:
        return None
    else:
        return statistics.median(age_list)
