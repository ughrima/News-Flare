
# 🗞️ Satirical News Explorer

This project is a full pipeline to **extract**, **analyze**, and **present** the **most relevant and important global news**, enriched with satire. It scrapes high-quality articles, processes them using cutting-edge NLP, categorizes and clusters them by topic, and then adds humorous flair—finally displaying everything in a stylish interactive dashboard.

---

## 📁 Project Structure

```
├── main.ipynb               # News scraping, sentiment analysis, keyword extraction, entity & topic modeling
├── satire.ipynb             # Satirical headline and summary generation using FLAN-T5
├── topic.py                 # Dynamic keyword clustering and topic assignment
├── news_flare.py            # Streamlit dashboard for visualizing satirical news
```

---

## 📦 Dependencies

Install the required packages:

```bash
pip install spacy nltk vaderSentiment transformers beautifulsoup4 selenium webdriver-manager pandas wordcloud matplotlib streamlit gensim yake scikit-learn sentence-transformers
python -m nltk.downloader punkt stopwords
python -m spacy download en_core_web_sm
```

---

## 🔄 Detailed File Descriptions

### 1. `main.ipynb` – **News Gathering & Processing Pipeline**

**Purpose**: Fetches and processes high-quality news articles, then applies various NLP techniques including sentiment analysis, keyword extraction, entity recognition, and topic modeling.

#### ✅ News Fetching
- Uses **NewsAPI** with a well-defined query and explicit trusted sources.
- If fewer than 15 articles are returned, fallback expands to include `health` and `sports`.

#### 🧼 Preprocessing & Scraping
- `BeautifulSoup` and `Selenium` clean full article content, handling dynamic pages.

#### 📊 NLP Pipeline
- **Sentiment Analysis**: VADER (rule-based) → DistilBERT (transformer) fallback.
- **Keyword Extraction**: Initially `YAKE`, replaced by `KeyBERT` for contextual relevance.
- **Summarization**: `Sumy` LSA summarizer.
- **Entity Recognition**: `spaCy` identifies people, places, organizations.
- **Relation Extraction**: Extracts thematic connections between keywords and entities.

**Output**:
A cleaned dataset with text, keywords, sentiment, entities, summaries.

---

### 2. `topic.py` – **Dynamic Topic Categorization**

**Purpose**: Automatically assigns each article to a semantic topic based on clustered keywords.

#### 🧠 Method:
- Deduplicates similar articles.
- Extracts and filters keywords.
- Groups keywords into thematic buckets (e.g., Trade, Politics, Health).
- Assigns articles based on the best match using keyword overlap and content matching.

**Output**:
A CSV with added columns: `Dominant_Topic`, `Topic_Description`.

---

### 3. `satire.ipynb` – **Humor Layer: Satirical Enrichment**

**Purpose**: Generates humorous versions of each article using `google/flan-t5-base`.

#### ✍️ How It Works
- Prompts are crafted like: `"Make this headline funny: ..."` or `"Write a funny summary about: ..."`
- Uses sampling to ensure creative output:
  - `max_new_tokens`: 30 (headline), 60 (summary)
  - `temperature`: 0.95
  - `top_p`: 0.95
  - `do_sample=True`, `truncation=True`
- Outputs are post-processed to extract the actual funny text.

Adds:
- `Satirical_Headline`
- `Funny_Short_Summary` columns to the dataset.

---

### 4. `news_flare.py` – **Interactive Streamlit Dashboard**

**Purpose**: Displays processed articles with satirical content in a visually rich web UI.

#### 💡 Features:
- Sidebar filter by topic
- Color-coded **sentiment labels** with emojis
- **Keyword chips** with pastel colors
- **Funny headlines & summaries**
- Links to full articles
- Aesthetic **word cloud** visualization

---

## 🚀 To Run

After generating the final CSV:

```bash
streamlit run news_flare.py
```

---

## 🎯 Project Goal

This project **focuses on surfacing globally relevant and important news**, filtering out noise, and making it **engaging and accessible through humor and intelligent summarization**.
