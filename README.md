# News-Flare

---

# News Article Analysis with Satirical Content Generation

This project processes news articles, assigns them to thematic categories based on keywords, and generates satirical headlines and summaries for each article. The goal is to create a fun and humorous interpretation of news articles through machine learning.

## Features

- **Data Preprocessing:** Clean the dataset by excluding articles with missing or empty content, and remove duplicate articles based on content similarity.
- **Keyword-Based Categorization:** Classify articles into broad thematic categories such as "Politics," "Trade," "Social Issues," and more, based on the keywords present in each article.
- **Satirical Content Generation:** Generate funny and sarcastic headlines and short summaries for each article using a pre-trained text-to-text model.
- **Output:** Save the processed articles with their respective categories, satirical headlines, and funny summaries into a new CSV file.

## Requirements

- **Python 3.8+**
- **Libraries:**  
  - `pandas`
  - `nltk`
  - `transformers` (for text generation)
  - `re`
  - `string`
  - `difflib`
  - `collections`

To install the necessary libraries, run the following:

```bash
pip install pandas nltk transformers
```

## Setup

1. **Download the NLTK Data:**
   - The script uses NLTK's `punkt` and `stopwords`. You need to download these before running the script.

2. **Prepare Your Data:**
   - Ensure your CSV file has at least two columns: `Title`, `Summary`, and `Keywords` for each article.
   - The column `Scraped_Content` should contain the article's main text.

3. **Run the Script:**
   - Once your data is ready, you can run the `main.py` script with the following command:

   ```bash
   python main.py
   ```

   The script will preprocess the CSV, deduplicate articles, categorize them, generate satirical content, and save the updated DataFrame to a new CSV file.

## Script Breakdown

1. **`load_and_preprocess_csv(file_path)`**  
   This function loads the CSV, removes rows with missing content, and resets the index.

2. **`deduplicate_articles(df, similarity_threshold=0.95)`**  
   This function deduplicates articles by calculating the similarity between article contents. If the similarity score is above the threshold, the second article is considered a duplicate and removed.

3. **`extract_keywords(keywords_str)`**  
   This function processes the `Keywords` column by extracting keywords from each article, cleaning them, and converting them into a list of lowercase keywords.

4. **`group_keywords_into_categories(df)`**  
   This function groups keywords into predefined thematic categories (e.g., "Trade," "Politics") and assigns them to articles.

5. **`assign_articles_to_categories(df, category_keywords)`**  
   This function assigns each article to a category based on the presence of matching keywords.

6. **`generate_satirical_content(df)`**  
   Using the `transformers` library, this function generates satirical headlines and funny summaries for each article.

7. **Output:**  
   After processing, the script saves the results in a new CSV file: `news_with_satirical_content.csv`. The new CSV includes:
   - `Dominant_Topic`: The assigned category for the article.
   - `Topic_Description`: A description of the category and keyword matches.
   - `Satirical_Headline`: A generated funny headline.
   - `Funny_Short_Summary`: A sarcastic, funny summary of the article.

## Example Output

```csv
Title,Summary,Keywords,Satirical_Headline,Funny_Short_Summary,Dominant_Topic,Topic_Description
"Trade War Heats Up", "US and China increase tariffs", "tariff, trade, economy", "When Your Favorite Trade War Becomes a Family Feud", "US and China’s tariff game reaches new levels of absurdity.", "Trade", "Topic: Trade (Matches: 2, Keywords: tariff, trade)"
...
```

## Notes

- The script uses the **Flan-T5 model** from Google's pre-trained models for generating the satirical content. The model is fine-tuned to generate text-to-text responses.
- The category assignment process is dynamic, and the prioritization of certain themes (e.g., prioritizing "Trade" over "Politics" for trade-related keywords) can be customized based on the use case.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

You can copy and paste this into your `README.md` file. Let me know if you want any changes or additions!
