import datetime
import json
import random
import time

from script.users import username

NOW = datetime.date(year=2023, month=1, day=1)
NUM_USERS = 2000
random.seed(123)

def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d %H:%M', prop)

def user():
    payment = random.choice(["23.99", "29.99", "33.99", "85.00", "88.00", "99.99"])
    return dict(
        username=username(),
        status=random.choice(["active", "inactive", "suspended"]),
        created=random_date("2010-1-1 00:00", "2023-1-1 00:00", random.random()),
        orders=[
            dict(
                date=(NOW - datetime.timedelta(weeks=i)).isoformat(),
                cost=payment,
                status=random.choices(["ERROR", "FAILED", "SUCCESS", "PENDING"], weights=[1, 10, 100, 20])[0]
            )
            for i in range(random.randint(0,15))
        ],
    )


if __name__ == "__main__":
    users = (user() for _ in range(NUM_USERS))
    print(json.dumps(list(users), indent=2))
