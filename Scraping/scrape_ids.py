# Scrapes following (followers + following) to a given depth starting at one user.
# Sores following data in form of ids

import tweepy
import time
import pandas as pd
import asyncio

# Tweepy authentication
auth = tweepy.OAuthHandler('jM02SFZT0CSvc3ovYQ64feJof', 'FaZobzNnyrY48xslNNB3VnGRoHvH8FJUUPTGSzYhOCROvBkMsp')
auth.set_access_token('2235275766-ryYMfgCqdClUnIXlKvGpgQgqOhHIITl7t5kmwJc', '7qGJcG2g9fmmNe9fMFedWfOloy01ORfq8G3SL6ZHp5y2U')
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# number of levels to be scraped
LEVELS = 2
current_level = 0

user_data = []

# time started
start_time = time.time()

# Print in colors in terminal
def pr_red(skk): print("\033[91m {}\033[00m" .format(skk))
def pr_cyan(skk): print("\033[96m {}\033[00m" .format(skk))


def main():
    user = api.get_user("levitannin")
    perform_scrape(user)
    print(time.time() - start_time)

def perform_scrape(user):
    user_id = user.id
    # holds the complete set of all followings scraped
    all_users = {user_id}

    # Current level of users being scraped
    users_in_level = all_users

    # call scrape_level for each level
    for level in range(LEVELS):
        current_level = level
        # print("users in level", level, users_in_level, "\nLength", len(users_in_level))
        users_in_level = scrape_level(users_in_level)
        all_users.update(users_in_level)
    create_df()

# scrape a level of users
def scrape_level(users_ids):
    next_level = set()
    for user in users_ids:
        next_level.update(scrape_user(user))
    # prints length of following for the users of current level
    print("length of level", len(next_level))
    return next_level

# returns a list containing one user's following
def scrape_user(user_id):
    # get screen name from id
    screen_name = api.get_user(user_id).screen_name
    print("Scraping", screen_name)

    # ids will hold all ids of a user's following
    ids = set()
    followers = []
    following = []

    try:
        followers = api.followers_ids(user_id)
        ids.update(followers)
        time.sleep(5)

        following = api.friends_ids(user_id)
        ids.update(following)
        time.sleep(5)

    except tweepy.TweepError as ex:
        if ex == "Not authorized": pr_red("Not authorized exception, skipping user")
        else: print("Other exception", ex)

    print(api.get_user(user_id).screen_name, "has", len(ids), "followers + following")
    save_data(screen_name, user_id, followers, following)
    return ids

def create_df():
    df = pd.DataFrame(user_data)
    print(df)

def save_data(screen_name, user_id, followers, following):
    data = {"Level": current_level,
            "Screen Name": screen_name,
            "ID": user_id,
            "Followers": followers,
            "Following": following}
    user_data.append(data)


if __name__ == '__main__':
    main()