# 🧠 Sentiment Analysis using AFINN and WordNet

> A Python desktop app that fetches live tweets for any search query and analyses their sentiment using two different NLP algorithms — **AFINN** and **WordNet (SentiWordNet)** — with results displayed as a pie chart.

---

## What it does

1. Enter a **search query** (e.g. `climate change`, `iPhone`, `elections`)
2. Enter how many **tweets** to analyse
3. Choose an algorithm — **AFINN** or **WordNet**
4. App fetches live tweets via Twitter API, preprocesses them, runs sentiment scoring, and displays a **pie chart** of Positive / Negative / Neutral breakdown

---

## Demo

▶️ **[Watch demo on YouTube](https://www.youtube.com/watch?v=N8VjJi-udO4&t=10s)**

> *Old demo video — the app works, the narration is... enthusiastic. Bear with it.*

---

## How it works

```
User Input (query + tweet count)
          │
          ▼
  Twitter API (Tweepy)
  → Fetch tweets
          │
          ▼
  Text Preprocessing
  → Remove @mentions, RTs, URLs, hashtags, special chars
          │
          ├──────────────────┬──────────────────┐
          ▼                  ▼
      AFINN               WordNet
   Lexicon Score        SentiWordNet
   (word scoring)    (POS tag → sentiment score)
          │                  │
          └──────────────────┘
                    │
                    ▼
          Pie Chart (Matplotlib)
       Positive / Negative / Neutral %
```

---

## Algorithms

### AFINN
- Uses the AFINN lexicon — a list of ~3,300 English words each assigned a sentiment score from -5 (very negative) to +5 (very positive)
- Scores each tweet and classifies as Positive / Negative / Neutral

### WordNet (SentiWordNet)
- Uses NLTK's **SentiWordNet** corpus
- Tokenises tweets → removes stopwords → POS tagging (Noun, Verb, Adj, Adv)
- Looks up each word's **positive score** and **negative score** in SentiWordNet
- Falls back to **lemmatization** then **stemming** if the word isn't found directly
- Aggregates scores per tweet to determine overall sentiment

---

## Tech Stack

| Component | Library |
|---|---|
| GUI | Tkinter |
| Twitter API | Tweepy |
| Sentiment (1) | AFINN |
| Sentiment (2) | NLTK — SentiWordNet, POS tagger, Lemmatizer, PorterStemmer |
| Data handling | Pandas |
| Visualisation | Matplotlib |
| Text cleaning | Regex |

---

## Setup

### 1. Install dependencies

```bash
pip install tweepy afinn nltk pandas matplotlib
```

```python
import nltk
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('sentiwordnet')
nltk.download('wordnet')
nltk.download('universal_tagset')
```

### 2. Add your Twitter API credentials

In `datapreprocessing.py`, replace the placeholder keys with your own from the [Twitter Developer Portal](https://developer.twitter.com):

```python
consumer_key        = "YOUR_CONSUMER_KEY"
consumer_secret     = "YOUR_CONSUMER_SECRET"
access_token        = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"
```

### 3. Run

```bash
python main.py
```

---

## Project Structure

```
├── main.py                         # Tkinter GUI — search input + algorithm buttons
├── datapreprocessing.py            # Tweet fetch, text cleaning, AFINN & WordNet logic
├── image.png                       # Background image for the GUI
└── Final code and application/     # Compiled .exe for Windows
```

---

## Output

The app plots a **pie chart** showing:
- % Positive tweets
- % Negative tweets  
- % Neutral tweets
- Total tweet count and breakdown in the legend

---

*Mini project — NLP sentiment analysis comparing lexicon-based (AFINN) vs corpus-based (WordNet) approaches on live Twitter data.*
