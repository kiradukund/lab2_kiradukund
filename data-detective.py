# coding: utf-8
import csv
import sys
import os

# This function opens the CSV file and reads every row into a list
# Each row becomes a dictionary like {"Username": "alice", "Likes": "120"}
def load_raw_data(filename):
    if not os.path.exists(filename):
        print("Error: The file " + filename + " was not found.")
        sys.exit(1)

    raw_tweets = []

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            raw_tweets.append(row)

    print("\nLoaded " + str(len(raw_tweets)) + " raw tweets from " + filename)
    return raw_tweets


# QUEST 1 - Clean the messy data before we do anything else
def clean_data(tweets):
    clean_tweets = []
    fixed = 0
    removed = 0

    for tweet in tweets:
        text_value = tweet.get("Text", "").strip()

        # If there is no text at all, skip this tweet
        if text_value == "":
            removed += 1
            continue

        # If Likes is empty, set it to 0
        if tweet.get("Likes", "").strip() == "":
            tweet["Likes"] = "0"
            fixed += 1

        # If Retweets is empty, set it to 0
        if tweet.get("Retweets", "").strip() == "":
            tweet["Retweets"] = "0"
            fixed += 1

        clean_tweets.append(tweet)

    print("\n" + "="*50)
    print("QUEST 1 - Data Auditor")
    print("="*50)
    print("Tweets removed (missing text) : " + str(removed))
    print("Fields repaired (set to 0)    : " + str(fixed))
    print("Clean tweets remaining        : " + str(len(clean_tweets)))

    return clean_tweets


# QUEST 2 - Find the tweet with the most likes WITHOUT using max()
def find_viral_tweet(tweets):
    if len(tweets) == 0:
        print("No tweets to search through.")
        return

    # Start by assuming the first tweet is the most liked
    viral = tweets[0]

    # Check every other tweet to see if it has more likes
    for i in range(1, len(tweets)):
        current_likes = int(tweets[i]["Likes"])
        best_likes = int(viral["Likes"])

        if current_likes > best_likes:
            viral = tweets[i]

    print("\n" + "="*50)
    print("QUEST 2 - The Viral Post")
    print("="*50)
    print("Username : " + viral.get("Username", "Unknown"))
    print("Likes    : " + viral.get("Likes", "0"))
    print("Text     : " + viral.get("Text", ""))


# QUEST 3 - Sort all tweets from most liked to least liked using Bubble Sort
def custom_sort_by_likes(tweets):
    sorted_tweets = tweets[:]
    n = len(sorted_tweets)

    # Bubble Sort - compare two neighbours and swap if needed
    for pass_number in range(n - 1):
        for i in range(n - 1 - pass_number):
            likes_left = int(sorted_tweets[i]["Likes"])
            likes_right = int(sorted_tweets[i + 1]["Likes"])

            # We want highest first so swap if left is smaller
            if likes_left < likes_right:
                sorted_tweets[i], sorted_tweets[i + 1] = sorted_tweets[i + 1], sorted_tweets[i]

    return sorted_tweets


# QUEST 4 - Let the user search for a keyword
def search_tweets(tweets, keyword):
    matches = []

    for tweet in tweets:
        tweet_text = tweet.get("Text", "")

        # .lower() makes search case-insensitive
        if keyword.lower() in tweet_text.lower():
            matches.append(tweet)

    return matches


# This block runs when you execute the file directly
if __name__ == "__main__":

    # Step 1 - Load the raw data
    dataset = load_raw_data("twitter_dataset.csv")

    # Step 2 - Quest 1: Clean the data
    clean_dataset = clean_data(dataset)

    # Step 3 - Quest 2: Find the most liked tweet
    find_viral_tweet(clean_dataset)

    # Step 4 - Quest 3: Sort and show Top 10
    sorted_tweets = custom_sort_by_likes(clean_dataset)
    print("\n" + "="*50)
    print("QUEST 3 - Top 10 Most Liked Tweets")
    print("="*50)
    for rank, tweet in enumerate(sorted_tweets[:10], start=1):
        print(str(rank) + ". @" + tweet.get("Username","?") + " | Likes: " + tweet.get("Likes","0"))
        print("   " + tweet.get("Text","")[:50] + "...")

    # Step 5 - Quest 4: Keyword search
    keyword = input("\nEnter a keyword to search tweets (e.g. Python): ").strip()

    if keyword == "":
        print("No keyword entered. Skipping search.")
    else:
        results = search_tweets(clean_dataset, keyword)
        print("\n" + "="*50)
        print("QUEST 4 - Keyword Search: '" + keyword + "'")
        print("="*50)
        print("Total tweets matching '" + keyword + "': " + str(len(results)))
        print()

        if len(results) == 0:
            print("No matches found. Try a different keyword.")
        else:
            for tweet in results:
                print("@" + tweet.get("Username","?") + " (Likes: " + tweet.get("Likes","0") + ")")
                print("  " + tweet.get("Text",""))
                print()
