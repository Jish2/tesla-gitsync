from bs4 import BeautifulSoup
import requests
from subprocess import Popen, PIPE
import yaml
from datetime import datetime, timedelta

GITHUB_URL = "https://github.com/Jish2"
# GITHUB_URL = "https://github.tesla.com/jgoon"

GIT_LOG_FORMAT = '--pretty=format:"%h %as"'


def main():

    global current_store
    current_store = get_git_logs()  # from commit log
    updated_store = get_contributions_map("page.html")  # from github profile
    diff_store = diff_contribution_maps(current_store, updated_store)

    with open("store.yaml", "w") as writer:
        msg = yaml.dump(
            diff_store,
            default_flow_style=False,
        )
        msg2 = yaml.dump(current_store, default_flow_style=False)
        msg3 = yaml.dump(updated_store, default_flow_style=False)
        writer.write(msg + "\n" + msg2 + "\n" + msg3)

    for date in diff_store:
        count = diff_store[date] - current_store.get(date, 0)

        for num in range(count):
            contribute(date, num)

    pass


def diff_contribution_maps(original, updated):
    """
    given two contribution maps, returns as dictionary of the difference in the two
    """
    result = {}

    for date in updated:
        result[date] = updated.get(date) - original.get(date, 0)

    return result


def add_page(url: str):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
    }

    try:
        response = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        print(e)
        exit()

    with open("page.html", "w") as writer:
        writer.write(response.text)


def run(commands):
    Popen(commands).wait()


def contribute(date, num):

    parsed_date = datetime.strptime(date, "%Y-%m-%d")
    updated_date = parsed_date + timedelta(minutes=num)
    date_str = datetime.strftime(updated_date, "%Y-%m-%d %H:%M:%S")

    updated_count = current_store.get(date, 0) + 1
    current_store[date] = updated_count
    date_message = f"Contribution #{updated_count}: {date_str}"

    with open("store.yaml", "w") as writer:
        store_yaml = yaml.dump(
            current_store,
            default_flow_style=False,
        )
        writer.write(store_yaml)

    run(["git", "add", "."])
    run(["git", "commit", "-m", '"%s"' % date_message, "--date", date_str])


def get_contributions_map(filename: str):
    """
    takes file and from contribution graph, returns as dictionary of date: occurences
    """

    with open(filename) as fp:
        soup = BeautifulSoup(fp, features="html.parser")

    target_class = "ContributionCalendar-day"

    parsed_store = {}

    elements = soup.find_all(
        lambda tag: tag.get("class") == [target_class]
        and tag.has_attr("data-date")
        and tag.has_attr("data-level")
    )

    for element in elements:
        date = element["data-date"]
        count = int(element["data-level"])

        if count != 0:
            parsed_store[date] = count

    return parsed_store


def get_git_logs():
    """
    returns git logs of current repo as dictionary of date: occurences
    """
    process = Popen(["git", "log", GIT_LOG_FORMAT], stdout=PIPE, stderr=PIPE, text=True)

    output, error = process.communicate()

    if error != "":
        exit

    log = output[1:-1].split('"\n"')

    dates = {}  # [date: str in YYYY-MM-DD]: occurences: int

    for entry in log:
        hash, timestamp = entry.split(" ")
        dates[timestamp] = dates.get(timestamp, 0) + 1

    return dates


if __name__ == "__main__":
    main()

# checks if profile.html exists
# true -> pass
# false -> run the scraper

# parse html and create date commit map

# get the git log, and repopulate the yaml
# (we use git log as source of truth)

# diff the date commit map and git log
# write commits for the new git log

###### unused flow ######

# the source of truth will be the yaml, and commits will be made to the yaml.

# run the scraper to get profile.html

# parse html and create date commit map

# parse the yaml, store in mem.

# diff the date commit map and the yaml
# make commits resolving differences
