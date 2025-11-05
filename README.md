# 📚 Flipzy

A powerful spaced repetition system built with Python, Poetry, and Streamlit to help you learn English vocabulary and phrases efficiently.

## 🎯 Features

- **Spaced Repetition Algorithm**: Uses the SM-2 algorithm to optimize your learning schedule
- **Vocabulary & Phrases**: Add words, phrases, idioms, phrasal verbs, and more
- **Smart Scheduling**: Cards are automatically scheduled based on how well you remember them
- **Progress Tracking**: Monitor your learning statistics and progress
- **Easy Management**: Search, edit, and delete cards as needed
- **Beautiful UI**: Clean and intuitive interface built with Streamlit

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Poetry (for dependency management)

### Installation

1. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install dependencies**:
   ```bash
   poetry install
   ```

3. **Run the app**:
   ```bash
   poetry run streamlit run app.py
   ```

   Or activate the virtual environment first:
   ```bash
   poetry shell
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Add Vocabulary
- Go to the "Add Vocabulary" page
- Enter a word or phrase (e.g., "Break the ice")
- Add the definition/translation
- Optionally add an example sentence
- Choose a category (vocabulary, phrase, idiom, etc.)
- Click "Add Card"

### 2. Review Cards
- Go to the "Review" page
- Cards due for review will be shown
- Try to recall the definition
- Click "Show Answer" when ready
- Rate how well you remembered (0-5):
  - **0**: Complete blackout
  - **1**: Incorrect, but remembered with difficulty
  - **2**: Incorrect, but correct after hesitation
  - **3**: Correct, but with difficulty
  - **4**: Correct after some hesitation
  - **5**: Perfect immediate recall

### 3. Track Progress
- View statistics on the "Statistics" page
- See how many cards you've mastered
- Monitor your learning activity

### 4. Manage Cards
- Search for specific cards
- Delete cards you no longer need
- View all your cards organized by category

## 🧠 How Spaced Repetition Works

The app uses the **SM-2 algorithm** (SuperMemo 2), which:

1. **Adjusts intervals** based on your performance
   - Cards you remember easily appear less frequently
   - Cards you struggle with appear more often

2. **Calculates ease factors** for each card
   - Higher ease factor = easier card for you
   - Lower ease factor = more difficult card

3. **Optimizes review schedule**
   - New cards appear frequently
   - Well-mastered cards appear after longer intervals
   - Ensures efficient learning without forgetting

## 💡 Tips for Best Results

1. **Review daily**: Consistency is key to language learning
2. **Be honest**: Rate your recall accurately for optimal scheduling
3. **Add context**: Include example sentences to better understand usage
4. **Categorize**: Use categories to organize different types of vocabulary
5. **Review regularly**: Don't skip reviews - the algorithm works best with consistent use

## 📁 Project Structure

```
learning-english/
├── app.py                    # Main Streamlit application
├── spaced_repetition.py      # SM-2 algorithm implementation
├── storage.py                # Data persistence layer
├── pyproject.toml            # Poetry configuration
├── vocabulary_cards.json      # Data storage (created automatically)
└── README.md                 # This file
```

## 🔧 Technical Details

- **Framework**: Streamlit
- **Algorithm**: SM-2 (SuperMemo 2)
- **Storage**: JSON file (vocabulary_cards.json)
- **Python Version**: 3.8+

## 📝 License

This project is open source and available for personal use.

## 🎓 Your 3-Month Journey

To become fluent in 3 months:

1. **Week 1-2**: Add 20-30 new words/phrases daily
2. **Week 3-8**: Maintain daily reviews, add 10-15 new items daily
3. **Week 9-12**: Focus on reviewing mastered cards, add challenging phrases

**Goal**: Aim for 500-1000 vocabulary items mastered by the end of 3 months!

---

Happy learning! 🚀

