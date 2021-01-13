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
    friends: tp.List[tp.Dict[str, tp.Any]] = get_friends(
        user_id, fields=["bdate"]
    ).items  # type:ignore
    today = dt.date.today()
    ages = []
    user: tp.Dict[str, tp.Any]
    for user in friends:
        try:
            date = dt.date(
                int(user["bdate"].split(".")[2]),
                int(user["bdate"].split(".")[1]),
                int(user["bdate"].split(".")[0]),
            )
        except (KeyError, IndexError):
            continue
        ages.append(relativedelta(today, date).years)
    if ages:
        return statistics.median(ages)
    else:
        return None
