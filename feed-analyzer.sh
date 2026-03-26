#!/bin/bash

# feed-analyzer.sh
# This script reads twitter_dataset.csv and finds the Top 5 most active users
# It uses command-line tools chained together with the pipe | symbol

# First, check that the CSV file actually exists before we do anything
if [ ! -f "twitter_dataset.csv" ]; then
    echo "Error: twitter_dataset.csv not found in this folder."
    exit 1
fi

echo "=== Top 5 Most Active Twitter Users ==="
echo ""

# Here is how the pipeline works, step by step:
#
# cut -d',' -f2 twitter_dataset.csv
#   --> cuts out only column 2 (the Username column) from the CSV
#       -d',' means the separator between columns is a comma
#       -f2 means we want field number 2
#
# | tail -n +2
#   --> skips the first line (the header row that says "Username")
#       without this, "Username" would be counted as an actual user
#
# | sort
#   --> sorts all usernames alphabetically so identical names are next to each other
#       uniq -c only works properly when duplicates are side by side
#
# | uniq -c
#   --> counts how many times each username appears in a row
#       the -c flag adds the count number at the start of each line
#
# | sort -rn
#   --> sorts the results numerically (-n) in reverse (-r)
#       so the user with the MOST tweets comes first
#
# | head -5
#   --> only shows the first 5 lines (our Top 5)

cut -d',' -f2 twitter_dataset.csv | tail -n +2 | sort | uniq -c | sort -rn | head -5

echo ""
echo "Done."
