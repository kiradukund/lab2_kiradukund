#!/bin/bash

# feed-analyzer.sh
# Reads twitter_dataset.csv and prints the Top 5 most active users

# Check that the CSV file exists before doing anything
if [ ! -f "twitter_dataset.csv" ]; then
    echo "Error: twitter_dataset.csv not found in this folder."
    exit 1
fi

echo "======================================="
echo "  Top 5 Most Active Twitter Users"
echo "======================================="
echo ""

# How this pipeline works step by step:
#
# cut -d',' -f2 twitter_dataset.csv
#     Gets only column 2 (Username) from the CSV file
#
# | tail -n +2
#     Skips the first line (the header row "Username")
#
# | sort
#     Sorts all usernames alphabetically so duplicates sit next to each other
#
# | uniq -c
#     Counts how many times each username appears in a row
#
# | sort -rn
#     Sorts by count from highest to lowest
#
# | head -5
#     Shows only the top 5 results

cut -d',' -f2 twitter_dataset.csv | tail -n +2 | sort | uniq -c | sort -rn | head -5

echo ""
echo "Done."
