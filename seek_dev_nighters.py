import requests
from pytz import timezone, utc
import datetime as d
from datetime import datetime


DEV_URL = 'http://devman.org/api/challenges/solution_attempts/'


def load_attempts(pages):
    for page in range(1, pages + 1):
        response = get_json_response_by_page_number(page)
        for records in response['records']:
            timestamp = records['timestamp']
            time_zone = records['timezone']
            commit_time = get_commit_time(timestamp, time_zone)
            is_midnighter = is_midnighter_current_user(commit_time)
            if is_midnighter:
                yield {
                    'username': records['username'],
                    'timestamp': commit_time,
                    'timezone': time_zone,
                }


def get_json_response_by_page_number(page):
    payload = {"page": page}
    return requests.get(DEV_URL, params=payload).json()


def get_commit_time(timestamp, time_zone):
    if timestamp and time_zone:
        return utc.localize(datetime.utcfromtimestamp(timestamp)).astimezone(timezone(time_zone)).time()
    return None


def is_midnighter_current_user(time_z):
    if time_z:
        time_of_night_start = d.time(0, 0, 0)
        time_of_night_finish = d.time(6, 0, 0)
        return bool(time_of_night_start < time_z < time_of_night_finish)
    return False


def get_number_of_pages():
    response = requests.get(DEV_URL).json()
    number_of_pages = response["number_of_pages"]
    if not number_of_pages or number_of_pages is None:
        exit("Number of pages can't be {}".format(number_of_pages))
    return int(number_of_pages)


def print_midnighters(attempts_l):
    print("Midnight users are:\n{0} \t\t{1} \t\t{2}".format('Username', 'Timestamp', 'Timezone'))
    for params in attempts_l:
        print("{0} \t\t{1} \t\t{2}".format(params['username'], params['timestamp'], params['timezone']))


if __name__ == '__main__':
    number_of_pages = get_number_of_pages()
    attempts = load_attempts(number_of_pages)
    print_midnighters(attempts)
