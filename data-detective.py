import csv
import sys
import os

# This is my main project file for the data detective lab
# I read through the twitter dataset and run 4 analysis tasks on it
# Each function below handles one part of the work


def load_raw_data(filename):
    """
    Opens the CSV file and loads every row into a list.
    Each row becomes a dictionary so I can access fields by name.
    Returns the full list of tweets exactly as they are in the file.
    """
    # Before opening the file, check it actually exists
    # If not, we print a clear message and stop the program
    if not os.path.exists(filename):
        print("Error: Could not find the file called " + filename)
        print("Make sure twitter_dataset.csv is in the same folder as this script.")
        sys.exit(1)

    tweet_list = []

    # Open the file and read it row by row using DictReader
    # DictReader is useful because it turns each row into a dictionary
    # so instead of row[0] I can write row["Username"] which is clearer
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            tweet_list.append(row)

    print("\nSuccessfully loaded " + str(len(tweet_list)) + " tweets from " + filename)
    return tweet_list


def clean_data(tweet_list):
    """
    Cleans the dataset before any analysis.
    - Removes tweets that have no text at all
    - Replaces empty Likes or Retweets fields with 0
    Returns a clean list ready to work with.
    """
    processed_tweets = []
    rows_removed = 0
    fields_fixed = 0

    for tweet in tweet_list:
        text_value = tweet.get("Text", "").strip()

        # If a tweet has no text there is nothing useful about it
        # so I skip it and count it as removed
        if text_value == "":
            rows_removed += 1
            continue

        # Some tweets are missing their Likes count
        # I replace the empty value with "0" so the rest of the code
        # does not crash when it tries to convert it to a number
        if tweet.get("Likes", "").strip() == "":
            tweet["Likes"] = "0"
            fields_fixed += 1

        # Same fix for Retweets
        if tweet.get("Retweets", "").strip() == "":
            tweet["Retweets"] = "0"
            fields_fixed += 1

        processed_tweets.append(tweet)

    print("\n" + "-" * 45)
    print("Data Cleaning Summary")
    print("-" * 45)
    print("Tweets removed (no text found) : " + str(rows_removed))
    print("Empty fields fixed (set to 0)  : " + str(fields_fixed))
    print("Tweets ready for analysis      : " + str(len(processed_tweets)))

    return processed_tweets


def find_most_liked(tweet_list):
    """
    Finds the single tweet with the highest number of Likes.
    I used a loop here instead of max() to follow the assignment rule.
    The idea is simple: assume the first tweet is the best,
    then keep replacing it whenever I find something better.
    """
    if len(tweet_list) == 0:
        print("No tweets to check.")
        return

    # Start by assuming tweet number 1 is the most liked
    most_liked_tweet = tweet_list[0]

    # Go through every other tweet starting from index 1
    for i in range(1, len(tweet_list)):
        # CSV files store everything as text so "200" is not a number yet
        # I have to convert to int before comparing otherwise "90" > "200"
        current_likes = int(tweet_list[i]["Likes"])
        current_best  = int(most_liked_tweet["Likes"])

        # If this tweet has more likes, it becomes our new best
        if current_likes > current_best:
            most_liked_tweet = tweet_list[i]

    print("\n" + "-" * 45)
    print("Most Viral Tweet")
    print("-" * 45)
    print("Username : @" + most_liked_tweet.get("Username", "unknown"))
    print("Likes    : " + most_liked_tweet.get("Likes", "0"))
    print("Text     : " + most_liked_tweet.get("Text", ""))


def sort_by_likes(tweet_list):
    """
    Sorts all tweets from highest likes to lowest using Bubble Sort.
    I wrote this sorting algorithm myself without using .sort() or sorted().
    Bubble Sort works by comparing two tweets next to each other
    and swapping them if they are in the wrong order.
    After enough passes, the whole list ends up sorted.
    """
    # I copy the list first so the original stays unchanged
    sorted_list = tweet_list[:]
    total = len(sorted_list)

    # Outer loop controls how many passes we make through the list
    for pass_num in range(total - 1):

        # Inner loop does the actual comparisons in each pass
        # Each pass the last item is already in place so we check one less
        for i in range(total - 1 - pass_num):
            likes_left  = int(sorted_list[i]["Likes"])
            likes_right = int(sorted_list[i + 1]["Likes"])

            # We want highest first so if the left is SMALLER we swap them
            if likes_left < likes_right:
                sorted_list[i], sorted_list[i + 1] = sorted_list[i + 1], sorted_list[i]

    return sorted_list


def search_by_keyword(tweet_list, keyword):
    """
    Goes through all tweets and collects ones that contain the keyword.
    The search is case-insensitive so Python matches PYTHON matches python.
    Returns a new list of only the matching tweets.
    """
    matching_tweets = []

    for tweet in tweet_list:
        tweet_text = tweet.get("Text", "")

        # .lower() on both sides means the search ignores uppercase/lowercase
        if keyword.lower() in tweet_text.lower():
            matching_tweets.append(tweet)

    return matching_tweets


def average_likes(tweet_list):
    """
    Calculates the average number of likes across all tweets.
    I added this as an extra feature to show more about the dataset.
    """
    if len(tweet_list) == 0:
        return 0

    total_likes = 0

    # Add up every tweet's likes one by one
    for tweet in tweet_list:
        try:
            total_likes += int(tweet["Likes"])
        except ValueError:
            # If a likes value is somehow not a number, just skip it
            pass

    return total_likes // len(tweet_list)


def count_tweets_per_user(tweet_list):
    """
    Counts how many tweets each user has in the dataset.
    I store the counts in a dictionary where the key is the username.
    This is my own extra feature added on top of the required quests.
    """
    user_counts = {}

    for tweet in tweet_list:
        username = tweet.get("Username", "unknown")

        # If we have seen this user before, add 1 to their count
        # If this is their first tweet, start their count at 1
        if username in user_counts:
            user_counts[username] += 1
        else:
            user_counts[username] = 1

    return user_counts


# ---------------------------------------------------------------
# Main program starts here - this runs when you execute the file
# ---------------------------------------------------------------
if __name__ == "__main__":

    print("\nWelcome to Twitter Data Detective")
    print("===================================")

    # Step 1 - Load the raw data from the CSV file
    tweet_list = load_raw_data("twitter_dataset.csv")

    # Step 2 - Clean the data before doing any analysis
    processed_tweets = clean_data(tweet_list)

    # Step 3 - Find the most liked tweet using my manual loop
    find_most_liked(processed_tweets)

    # Step 4 - Sort all tweets by likes and show the Top 10
    sorted_tweets = sort_by_likes(processed_tweets)

    print("\n" + "-" * 45)
    print("Top 10 Tweets by Likes")
    print("-" * 45)
    for rank, tweet in enumerate(sorted_tweets[:10], start=1):
        print(str(rank) + ". @" + tweet.get("Username", "?") +
              " | Likes: " + tweet.get("Likes", "0"))
        print("   " + tweet.get("Text", "")[:55] + "...")

    # Step 5 - Show average likes across all tweets (my extra feature)
    avg = average_likes(processed_tweets)
    print("\n" + "-" * 45)
    print("Extra Stats")
    print("-" * 45)
    print("Average likes per tweet : " + str(avg))

    # Step 6 - Show tweet count per user (my second extra feature)
    user_counts = count_tweets_per_user(processed_tweets)
    print("\nTweets per user:")
    for user, count in user_counts.items():
        print("  @" + user + " : " + str(count) + " tweet(s)")

    # Step 7 - Let the user search for a keyword
    print("\n" + "-" * 45)
    print("What would you like to do next?")
    print("-" * 45)
    print("1 - Search tweets by keyword")
    print("2 - View Top 10 again")
    print("3 - Exit")

    choice = input("\nEnter your choice (1/2/3): ").strip()

    if choice == "1":
        keyword = input("Enter a keyword to search for: ").strip()

        if keyword == "":
            print("You did not enter a keyword. Skipping search.")
        else:
            results = search_by_keyword(processed_tweets, keyword)
            print("\nFound " + str(len(results)) + " tweet(s) containing '" + keyword + "':\n")

            if len(results) == 0:
                print("No matches found. Try a different word.")
            else:
                for tweet in results:
                    print("@" + tweet.get("Username", "?") +
                          " (Likes: " + tweet.get("Likes", "0") + ")")
                    print("  " + tweet.get("Text", ""))
                    print()

    elif choice == "2":
        print("\nTop 10 Tweets by Likes")
        print("-" * 45)
        for rank, tweet in enumerate(sorted_tweets[:10], start=1):
            print(str(rank) + ". @" + tweet.get("Username", "?") +
                  " | Likes: " + tweet.get("Likes", "0"))
            print("   " + tweet.get("Text", "")[:55] + "...")

    else:
        print("\nGoodbye! Hope the analysis was useful.")
