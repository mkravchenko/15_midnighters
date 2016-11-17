import requests
from pytz import timezone, utc
import datetime as d
from datetime import datetime


DEV_URL = 'http://devman.org/api/challenges/solution_attempts/'


def load_attempts():
    pages = get_number_of_pages()
    for page in range(1, pages + 1):
        payload = {"page": page}
        response = requests.get(DEV_URL, params=payload).json()
        for records in response['records']:
            user_name = records['username']
            timestamp = records['timestamp']
            time_zone = records['timezone']
            if timestamp and time_zone:
                commit_time = utc.localize(datetime.utcfromtimestamp(timestamp)).astimezone(timezone(time_zone)).time()
                is_midnighter = is_midnighter_current_user(commit_time)
                if is_midnighter:
                    yield {
                        'username': user_name,
                        'timestamp': commit_time,
                        'timezone': time_zone,
                    }


def is_midnighter_current_user(time_z):
    t1 = d.time(0, 0, 0)
    t2 = d.time(6, 0, 0)
    return True if t1 < time_z < t2 else False


def get_number_of_pages():
    response = requests.get(DEV_URL).json()
    number_of_pages = response["number_of_pages"]
    if not number_of_pages or number_of_pages is None:
        exit("Number of pages can't be {}".format(number_of_pages))
    return int(number_of_pages)


def print_midnighters():
    attempt = load_attempts()
    print("Midnight users are:\n{0} \t\t{1} \t\t{2}".format('Username', 'Timestamp', 'Timezone'))
    for params in attempt:
        print("{0} \t\t{1} \t\t{2}".format(params['username'], params['timestamp'], params['timezone']))


if __name__ == '__main__':
    print_midnighters()
