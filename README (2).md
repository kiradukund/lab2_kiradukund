# Lab 2 – Social Media Data Detective

## What This Project Does

This project reads a Twitter dataset CSV file, cleans the data, and runs four data analysis tasks using Python. A Bash script is also included to find the Top 5 most active users directly from the terminal.

---

## Files Included

| File | Description |
|------|-------------|
| `data-detective.py` | Main Python script – runs all 4 quests |
| `feed-analyzer.sh` | Bash script – finds Top 5 most active users |
| `twitter_dataset.csv` | The dataset used for testing |
| `README.md` | This file |

---

## How to Run the Python Script

**Step 1 – Make sure Python is installed**
```bash
python --version
```

**Step 2 – Place `twitter_dataset.csv` in the same folder as `data-detective.py`**

**Step 3 – Run the script**
```bash
python data-detective.py
```

The script will automatically:
1. Load the raw CSV data
2. Clean the data and report any fixes (Quest 1)
3. Find and display the most liked tweet (Quest 2)
4. Sort all tweets by likes using Bubble Sort and show the Top 10 (Quest 3)
5. Ask you to type a keyword and search for matching tweets (Quest 4)

---

## How to Run the Bash Script

**Step 1 – Give the script permission to run**
```bash
chmod +x feed-analyzer.sh
```

**Step 2 – Run it**
```bash
./feed-analyzer.sh
```

This will print the **Top 5 most active users** and how many tweets each one posted.

---

## How the Sorting Algorithm Works

The script uses **Bubble Sort** to order tweets from most liked to least liked. It works by repeatedly comparing two neighbouring tweets and swapping them whenever the left tweet has fewer likes than the right one. After enough passes through the list, all tweets end up sorted from highest to lowest likes.
