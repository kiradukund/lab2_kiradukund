import csv
import os
import sys

# ─────────────────────────────────────────────
#  LOAD DATA
#  Reads the CSV file and returns a list of
#  dictionaries (one dictionary per tweet).
# ─────────────────────────────────────────────
def load_raw_data(filename):
    # Check the file actually exists before we try to open it
    if not os.path.exists(filename):
        print("Error: The file '" + filename + "' was not found.")
        print("Make sure twitter_dataset.csv is in the same folder as this script.")
        sys.exit(1)

    raw_tweets = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                raw_tweets.append(row)
    except Exception as e:
        print("Something went wrong while reading the file: " + str(e))
        sys.exit(1)

    return raw_tweets


# ─────────────────────────────────────────────
#  QUEST 1 - THE DATA AUDITOR
#  Clean the messy data:
#    - Remove tweets that have no Text
#    - Replace empty Likes or Retweets with 0
# ─────────────────────────────────────────────
def clean_data(tweets):
    clean_tweets = []   # This will hold all the good tweets
    removed_count = 0   # Count how many tweets we throw away
    fixed_count = 0     # Count how many fields we repair

    for tweet in tweets:
        # If the Text field is empty or missing, skip this tweet entirely
        if not tweet.get('Text') or tweet['Text'].strip() == '':
            removed_count = removed_count + 1
            continue   # Jump to the next tweet

        # If Likes is empty, replace it with the string '0'
        if not tweet.get('Likes') or tweet['Likes'].strip() == '':
            tweet['Likes'] = '0'
            fixed_count = fixed_count + 1

        # If Retweets is empty, replace it with the string '0'
        if not tweet.get('Retweets') or tweet['Retweets'].strip() == '':
            tweet['Retweets'] = '0'
            fixed_count = fixed_count + 1

        # This tweet passed all checks, so add it to our clean list
        clean_tweets.append(tweet)

    print("=" * 50)
    print("QUEST 1 - Data Auditor")
    print("=" * 50)
    print("Tweets removed (missing text) : " + str(removed_count))
    print("Fields repaired (set to 0)    : " + str(fixed_count))
    print("Clean tweets remaining        : " + str(len(clean_tweets)))
    print()

    return clean_tweets


# ─────────────────────────────────────────────
#  QUEST 2 - THE VIRAL POST
#  Find the single tweet with the most Likes.
#  We are NOT allowed to use max() so we
#  loop through the list ourselves.
# ─────────────────────────────────────────────
def find_viral_tweet(tweets):
    # Safety check - make sure the list is not empty
    if len(tweets) == 0:
        print("No tweets available to search.")
        return None

    # Start by assuming the very first tweet is the most liked
    viral = tweets[0]

    # Now check every other tweet in the list
    for tweet in tweets:
        # Convert Likes from text to a whole number before comparing
        # Without int(), "90" would look bigger than "200" alphabetically
        if int(tweet['Likes']) > int(viral['Likes']):
            viral = tweet   # Found a new winner, update our variable

    print("=" * 50)
    print("QUEST 2 - The Viral Post")
    print("=" * 50)
    print("Username : " + viral['Username'])
    print("Likes    : " + viral['Likes'])
    print("Text     : " + viral['Text'])
    print()

    return viral


# ─────────────────────────────────────────────
#  QUEST 3 - THE ALGORITHM BUILDER
#  Sort all tweets from most liked to least
#  liked using Bubble Sort.
#  We are NOT allowed to use .sort() or sorted().
#
#  How Bubble Sort works:
#  We go through the list many times. Each time
#  we compare two neighbours. If the left one has
#  fewer likes than the right one we swap them.
#  We keep doing this until everything is in order.
# ─────────────────────────────────────────────
def custom_sort_by_likes(tweets):
    # Make a copy so we do not change the original list
    sorted_tweets = tweets[:]
    n = len(sorted_tweets)

    # Outer loop - we need up to n passes through the list
    for i in range(n):
        # Inner loop - compare each pair of neighbours
        for j in range(0, n - i - 1):
            left_likes  = int(sorted_tweets[j]['Likes'])
            right_likes = int(sorted_tweets[j + 1]['Likes'])

            # If the left tweet has FEWER likes, swap them
            # We want highest likes on the left = descending order
            if left_likes < right_likes:
                sorted_tweets[j], sorted_tweets[j + 1] = sorted_tweets[j + 1], sorted_tweets[j]

    # Slice the first 10 tweets for the Top 10
    top_10 = sorted_tweets[:10]

    print("=" * 50)
    print("QUEST 3 - Top 10 Most Liked Tweets")
    print("=" * 50)

    for i in range(len(top_10)):
        tweet = top_10[i]
        short_text = tweet['Text'][:55] + '...' if len(tweet['Text']) > 55 else tweet['Text']
        print(str(i + 1) + ". @" + tweet['Username'] + " | Likes: " + tweet['Likes'])
        print("   " + short_text)

    print()
    return sorted_tweets


# ─────────────────────────────────────────────
#  QUEST 4 - THE CONTENT FILTER
#  Ask the user for a keyword then search
#  through every tweet and collect matches
#  into a brand new list.
# ─────────────────────────────────────────────
def search_tweets(tweets, keyword):
    results = []   # Start with an empty list for matches

    # Loop through every tweet and check if the keyword appears in the Text
    for tweet in tweets:
        # .lower() makes the search case-insensitive
        # so "Python" and "python" both match
        if keyword.lower() in tweet['Text'].lower():
            results.append(tweet)   # Add this tweet to our results list

    print("=" * 50)
    print("QUEST 4 - Keyword Search: '" + keyword + "'")
    print("=" * 50)
    print("Total tweets matching '" + keyword + "': " + str(len(results)))
    print()

    if len(results) == 0:
        print("No tweets found containing that keyword.")
    else:
        for tweet in results:
            print("@" + tweet['Username'] + " (Likes: " + tweet['Likes'] + ")")
            print("  " + tweet['Text'])

    print()
    return results


# ─────────────────────────────────────────────
#  MAIN - This runs when you execute the script
# ─────────────────────────────────────────────
if __name__ == "__main__":

    # Step 1 - Load the raw data from the CSV file
    dataset = load_raw_data("twitter_dataset.csv")
    print("\nLoaded " + str(len(dataset)) + " raw tweets from twitter_dataset.csv\n")

    # Step 2 - Quest 1: Clean the data
    clean_dataset = clean_data(dataset)

    # Step 3 - Quest 2: Find the most viral tweet
    viral = find_viral_tweet(clean_dataset)

    # Step 4 - Quest 3: Sort by likes and show Top 10
    sorted_dataset = custom_sort_by_likes(clean_dataset)

    # Step 5 - Quest 4: Ask user for a keyword and search
    keyword = input("Enter a keyword to search tweets (e.g. Python): ").strip()

    if keyword == '':
        print("No keyword entered. Skipping search.")
    else:
        search_tweets(clean_dataset, keyword)
