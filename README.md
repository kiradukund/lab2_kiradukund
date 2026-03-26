# Lab 2 – Social Media Data Detective

## What This Project Does
This project reads a large Twitter dataset CSV file, cleans it, and runs four data analysis tasks using Python. A Bash script is also included to find the most active users straight from the terminal.

---

## Files Included

| File | Description |
|------|-------------|
| `data-dective.py` | Main Python script – runs all 4 quests |
| `feed-analyzer.sh` | Bash script – finds Top 5 most active users |
| `twitter_dataset.csv` | The dataset (download from Kaggle) |
| `README.md` | This file |

---

## How to Run the Python Script

### Step 1 – Make sure Python is installed
Open your terminal and type:
```
python --version
```
You should see something like `Python 3.x.x`.

### Step 2 – Place your dataset in the same folder
Make sure `twitter_dataset.csv` is in the **same folder** as `data-dective.py`.

### Step 3 – Run the script
```
python data-dective.py
```

### What happens next
The script will automatically:
1. Load and clean the data
2. Find the most liked tweet
3. Sort all tweets and show the Top 10
4. Ask you to type a keyword to search for

---

## How to Run the Bash Script

### Step 1 – Make sure `twitter_dataset.csv` is in the same folder

### Step 2 – Give the script permission to run
```
chmod +x feed-analyzer.sh
```

### Step 3 – Run it
```
./feed-analyzer.sh
```

This will print the **Top 5 most active users** and how many tweets each one posted.

---

## How the Sorting Algorithm Works

The script uses **Bubble Sort** to order tweets from most liked to least liked. It works by going through the list repeatedly and swapping two neighbours whenever the one on the left has fewer likes than the one on the right. After each full pass through the list, the tweet with the fewest likes moves closer to the end — just like a bubble rising to the surface — until everything is in the correct order.
