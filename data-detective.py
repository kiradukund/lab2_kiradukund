import csv
import sys
import os

# lab 2 - kiradukund - analyzing twitter data for my python class
# i split everything into functions to keep things organized


def load_raw_data(filename):
    """
    reads the csv file and puts every row into a list as a dictionary
    i used DictReader because it lets me do row["Likes"] instead of row[2]
    which is way easier to read
    """
    if not os.path.exists(filename):
        print("Error: cant find " + filename)
        print("make sure the csv file is in the same folder as this script")
        sys.exit(1)

    tweet_list = []

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweet_list.append(row)

    print("\nloaded " + str(len(tweet_list)) + " tweets from " + filename)
    return tweet_list


def clean_data(tweet_list):
    """
    goes through every tweet and fixes the messy ones
    - no text = useless, throw it away
    - missing likes or retweets = set to 0 so we dont get errors later
    """
    processed_tweets = []
    rows_removed = 0
    fields_fixed = 0

    for tweet in tweet_list:
        text_value = tweet.get("Text", "").strip()

        # skip tweets with no text, nothing to analyze there
        if text_value == "":
            rows_removed += 1
            continue

        # if likes is blank i set it to "0" as a string
        # because everything in csv comes as a string anyway
        if tweet.get("Likes", "").strip() == "":
            tweet["Likes"] = "0"
            fields_fixed += 1

        if tweet.get("Retweets", "").strip() == "":
            tweet["Retweets"] = "0"
            fields_fixed += 1

        processed_tweets.append(tweet)

    print("\n---------------------------------------------")
    print("cleaning done:")
    print("  removed  : " + str(rows_removed) + " tweets (no text)")
    print("  fixed    : " + str(fields_fixed) + " empty fields")
    print("  kept     : " + str(len(processed_tweets)) + " tweets")

    return processed_tweets


def find_most_liked(tweet_list):
    """
    finds the tweet with the most likes
    i used a loop instead of max() because the assignment said no built-in functions
    basically i pretend the first tweet is the winner and replace it
    every time i find something better
    """
    if len(tweet_list) == 0:
        print("no tweets found")
        return

    most_liked_tweet = tweet_list[0]  # start with tweet 1 as our best guess

    for i in range(1, len(tweet_list)):
        # my lecturer warned us about this string comparison issue in class
        # because "90" > "200" in python string comparison which is wrong
        current_likes = int(tweet_list[i]["Likes"])
        best_so_far   = int(most_liked_tweet["Likes"])

        if current_likes > best_so_far:
            most_liked_tweet = tweet_list[i]

    print("\n---------------------------------------------")
    print("most viral tweet:")
    print("  user  : @" + most_liked_tweet.get("Username", "unknown"))
    print("  likes : " + most_liked_tweet.get("Likes", "0"))
    print("  text  : " + most_liked_tweet.get("Text", ""))


def sort_by_likes(tweet_list):
    """
    sorts tweets from highest to lowest likes using bubble sort
    no .sort() allowed so i wrote the algorithm myself
    bubble sort keeps swapping neighbours until everything is in order
    it is not the fastest but it works and i understand how it works
    """
    sorted_list = tweet_list[:]  # copy so i dont mess up the original
    n = len(sorted_list)

    for pass_num in range(n - 1):
        for i in range(n - 1 - pass_num):

            left  = int(sorted_list[i]["Likes"])
            right = int(sorted_list[i + 1]["Likes"])

            # swap if left is smaller because we want biggest first
            if left < right:
                sorted_list[i], sorted_list[i + 1] = sorted_list[i + 1], sorted_list[i]

    return sorted_list


def search_by_keyword(tweet_list, keyword):
    """
    searches all tweets for a keyword and returns the matching ones
    .lower() makes it case insensitive so "python" finds "Python" too
    """
    matching_tweets = []

    for tweet in tweet_list:
        tweet_text = tweet.get("Text", "")

        if keyword.lower() in tweet_text.lower():
            matching_tweets.append(tweet)

    return matching_tweets


def get_average_likes(tweet_list):
    # extra feature i added - just wanted to see what the average was
    if len(tweet_list) == 0:
        return 0

    total = 0
    for tweet in tweet_list:
        try:
            total += int(tweet["Likes"])
        except ValueError:
            pass  # skip if somehow the value is not a number

    return total // len(tweet_list)


def tweets_per_user(tweet_list):
    # another extra - counts how many tweets each person has in the dataset
    # i used a dictionary because it is easy to look up by username
    counts = {}

    for tweet in tweet_list:
        user = tweet.get("Username", "unknown")

        if user in counts:
            counts[user] += 1
        else:
            counts[user] = 1

    return counts


# ---------------------------------------------------
# runs when you do: python data-detective.py
# ---------------------------------------------------
if __name__ == "__main__":

    print("\n== Twitter Data Detective ==")

    tweet_list = load_raw_data("twitter_dataset.csv")

    processed_tweets = clean_data(tweet_list)

    find_most_liked(processed_tweets)

    sorted_tweets = sort_by_likes(processed_tweets)

    print("\n---------------------------------------------")
    print("top 10 by likes:")
    print("---------------------------------------------")
    for rank, tweet in enumerate(sorted_tweets[:10], start=1):
        print(str(rank) + ". @" + tweet.get("Username", "?") + " - " + tweet.get("Likes", "0") + " likes")
        print("   " + tweet.get("Text", "")[:60] + "...")

    # my extra features
    avg = get_average_likes(processed_tweets)
    print("\n---------------------------------------------")
    print("average likes across all tweets: " + str(avg))

    user_counts = tweets_per_user(processed_tweets)
    print("\ntweet count per user:")
    for user, count in user_counts.items():
        print("  @" + user + " posted " + str(count) + " tweet(s)")

    # search menu
    print("\n---------------------------------------------")
    print("what do you want to do?")
    print("1 - search by keyword")
    print("2 - see top 10 again")
    print("3 - quit")

    choice = input("\nchoice: ").strip()

    if choice == "1":
        keyword = input("enter keyword: ").strip()

        if keyword == "":
            print("no keyword entered, skipping")
        else:
            results = search_by_keyword(processed_tweets, keyword)
            print("\n" + str(len(results)) + " tweet(s) found for '" + keyword + "':\n")

            if len(results) == 0:
                print("nothing matched, try another word")
            else:
                for tweet in results:
                    print("@" + tweet.get("Username", "?") + " (" + tweet.get("Likes", "0") + " likes)")
                    print("  " + tweet.get("Text", ""))
                    print()

    elif choice == "2":
        print("\ntop 10 by likes:")
        print("---------------------------------------------")
        for rank, tweet in enumerate(sorted_tweets[:10], start=1):
            print(str(rank) + ". @" + tweet.get("Username", "?") + " - " + tweet.get("Likes", "0") + " likes")
            print("   " + tweet.get("Text", "")[:60] + "...")

    else:
        print("\ndone, bye!")
