# Scrapes following (followers + following) to a given depth starting at one user.
# Sores following data in form of ids

import tweepy
import time
import asyncio

auth = tweepy.OAuthHandler('jM02SFZT0CSvc3ovYQ64feJof', 'FaZobzNnyrY48xslNNB3VnGRoHvH8FJUUPTGSzYhOCROvBkMsp')
auth.set_access_token('2235275766-ryYMfgCqdClUnIXlKvGpgQgqOhHIITl7t5kmwJc', '7qGJcG2g9fmmNe9fMFedWfOloy01ORfq8G3SL6ZHp5y2U')

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

LEVELS = 2

# time started
start_time = time.time()

# Print in colors in terminal
def pr_red(skk): print("\033[91m {}\033[00m" .format(skk))
def pr_cyan(skk): print("\033[96m {}\033[00m" .format(skk))


def main():
    username = "levitannin"
    perform_scrape(username)
    print(time.time() - start_time)

def perform_scrape(username):
    # holds the complete set of all followings scraped
    all_users = {username}

    # Current level of users being scraped
    users_in_level = all_users

    # call scrape_level for each level
    for level in range(LEVELS):
        print("users in level", level, users_in_level, "\nLength", len(users_in_level))
        users_in_level = scrape_level(users_in_level)

# scrape a level of users
def scrape_level(users_ids):
    next_level = set()
    for user in users_ids:
        next_level.update(scrape_user(user))
    # prints length of following for the users of current level
    print("length of level", len(next_level))
    return next_level

# returns a list containing one user's following
def scrape_user(username):
    print("Scraping", username)

    # Holds all the usernames of the users followers and following
    usernames = []
    usernames = api.followers(username)
    time.sleep(15)
    print("followers", usernames)
    usernames.append(api.friends_ids(username))
    time.sleep(15)

    print(username, "has", len(usernames), "followers + following")
    return usernames

if __name__ == '__main__':
    main()