import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import string
import re
from difflib import SequenceMatcher
from collections import Counter

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Step 1: Load and preprocess the CSV
def load_and_preprocess_csv(file_path):
    df = pd.read_csv(file_path)
    df = df[df['Scraped_Content'].notna() & (df['Scraped_Content'] != '')]
    df = df.reset_index(drop=True)
    print(f"After excluding failed scrapes: {len(df)} articles remain.")
    return df

# Step 2: Deduplicate articles
def deduplicate_articles(df, similarity_threshold=0.95):
    to_drop = []
    for i in range(len(df)):
        if i in to_drop:
            continue
        for j in range(i + 1, len(df)):
            if j in to_drop:
                continue
            content_i = str(df.loc[i, 'Scraped_Content'])
            content_j = str(df.loc[j, 'Scraped_Content'])
            similarity = SequenceMatcher(None, content_i, content_j).ratio()
            if similarity >= similarity_threshold:
                to_drop.append(j)
                print(f"Duplicate found: Article {i+1} and Article {j+1} (similarity: {similarity:.2f})")
    df = df.drop(to_drop).reset_index(drop=True)
    print(f"After deduplication: {len(df)} articles remain.")
    return df

# Step 3: Extract keywords from the Keywords column
def extract_keywords(keywords_str):
    if not isinstance(keywords_str, str):
        return []
    keywords = [kw.split(' (')[0].strip().lower() for kw in keywords_str.split(',')]
    return keywords

# Step 4: Preprocess text for keyword matching
def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    text = re.sub(r'\[\+\d+ chars\]', '', str(text))
    text = re.sub(r'\b(mon|tues|wednes|thurs|fri|satur|sun)day\b', '', text, flags=re.IGNORECASE)
    tokens = word_tokenize(text.lower())
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [token for token in tokens if len(token) > 3 and token.isalpha()]
    return ' '.join(tokens)

# Step 5: Define broad thematic categories with expanded seed words
THEMATIC_CATEGORIES = {
    "Trade": ["tariff", "trade", "export", "import", "economy", "market", "china", "us", "business", "industry", "musk", "cnn business"],
    "International Relations": ["ukraine", "russia", "south", "diplomatic", "government", "foreign", "war", "conflict", "republic", "africa", "california", "israeli", "minister"],
    "Religion": ["pope", "christian", "gaza", "religious", "faith", "prayer", "hope", "community", "church", "catholic"],
    "Aviation": ["boeing", "plane", "aviation", "industry", "ortberg", "kelly", "bessent"],
    "Social Issues": ["health", "pollution", "transgender", "social", "protest", "lawsuit", "fertility", "measles", "women", "rate", "particle", "birth", "air", "west"],
    "Legal and Corporate": ["tesla", "court", "judge", "corporate", "contract", "pentagon", "brand", "vehicle", "electric", "byd", "kff"],
    "Politics": ["trump", "president", "government", "policy", "administration", "republican", "politics", "governor", "defense", "secretary", "zelensky"]
}

# Step 6: Dynamically group keywords into thematic categories with prioritization
def group_keywords_into_categories(df):
    # Aggregate all keywords
    all_keywords = []
    for keywords_str in df['Keywords']:
        keywords = extract_keywords(keywords_str)
        all_keywords.extend(keywords)
    
    # Filter out generic keywords
    generic_keywords = ["white house", "white house press", "united states", "cnn", "told", "states"]
    all_keywords = [kw for kw in all_keywords if kw not in generic_keywords]
    
    # Count keyword frequencies
    keyword_counts = Counter(all_keywords)
    print("Top 20 Most Frequent Keywords (after filtering generics):")
    for kw, count in keyword_counts.most_common(20):
        print(f"{kw}: {count}")
    
    # Group keywords into categories based on seed words
    category_keywords = {category: [] for category in THEMATIC_CATEGORIES}
    unmatched_keywords = []
    
    for keyword in set(all_keywords):
        assigned = False
        category_scores = {}
        
        # Score each category based on seed word matches
        for category, seed_words in THEMATIC_CATEGORIES.items():
            score = sum(1 for seed_word in seed_words if seed_word in keyword)
            if score > 0:
                category_scores[category] = score
        
        if category_scores:
            # Prioritize categories
            prioritized_categories = sorted(category_scores, key=category_scores.get, reverse=True)
            dominant_category = prioritized_categories[0]
            
            # Prioritize Trade over Politics for trade-related keywords
            if "Trade" in category_scores and "Politics" in category_scores:
                trade_related = any(word in keyword for word in ["tariff", "trade", "export", "import", "economy", "market", "business"])
                if trade_related:
                    dominant_category = "Trade"
            
            # Prioritize Legal and Corporate over International Relations for legal-related keywords
            if "Legal and Corporate" in category_scores and "International Relations" in category_scores:
                legal_related = any(word in keyword for word in ["court", "judge", "lawsuit", "corporate", "brand", "vehicle"])
                if legal_related:
                    dominant_category = "Legal and Corporate"
            
            category_keywords[dominant_category].append(keyword)
            assigned = True
        
        if not assigned:
            unmatched_keywords.append(keyword)
    
    # Add unmatched keywords to "Other"
    category_keywords["Other"] = unmatched_keywords
    
    # Print the grouped keywords for debugging
    print("\nGrouped Keywords by Category:")
    for category, keywords in category_keywords.items():
        print(f"{category}: {keywords}")
    
    return category_keywords

# Step 7: Assign articles to categories based on keyword matches
def assign_articles_to_categories(df, category_keywords):
    topic_assignments = []
    topic_descriptions = []
    
    for i, row in df.iterrows():
        keywords = extract_keywords(row['Keywords'])
        processed_content = preprocess_text(row['Scraped_Content'])
        combined_text = ' '.join(keywords) + ' ' + processed_content
        
        # Score each category based on keyword matches
        category_scores = {}
        matched_keywords = {}
        for category, keywords in category_keywords.items():
            matches = [kw for kw in keywords if kw in combined_text]
            category_scores[category] = len(matches)
            matched_keywords[category] = matches
        
        # Assign the category with the most keyword matches
        if category_scores:
            dominant_category = max(category_scores, key=category_scores.get)
            score = category_scores[dominant_category]
            if score == 0:
                dominant_category = "Other"
                description = "Topic: Other (No matching keywords)"
            else:
                description = f"Topic: {dominant_category} (Matches: {score}, Keywords: {', '.join(matched_keywords[dominant_category])})"
        else:
            dominant_category = "Other"
            description = "Topic: Other (No matching keywords)"
        
        topic_assignments.append(dominant_category)
        topic_descriptions.append(description)
        
        # Debug: Print matches for Article 1
        if i == 0:
            print("\nArticle 1 Keyword Matches:")
            for category, matches in matched_keywords.items():
                print(f"{category}: {matches}")
    
    return topic_assignments, topic_descriptions

# Main function to process the CSV and assign topics
def main(file_path):
    # Load and preprocess CSV
    df = load_and_preprocess_csv(file_path)
    
    # Deduplicate articles
    df = deduplicate_articles(df)
    
    # Group keywords into categories
    category_keywords = group_keywords_into_categories(df)
    
    # Assign articles to categories
    topic_assignments, topic_descriptions = assign_articles_to_categories(df, category_keywords)
    
    # Add topic assignments to DataFrame
    df['Dominant_Topic'] = topic_assignments
    df['Topic_Description'] = topic_descriptions
    
    # Save the updated DataFrame
    df.to_csv("processed_articles_with_dynamic_topics.csv", index=False)
    
    # Print topic assignments
    print("\nTopic Assignments:")
    for i, (topic, desc) in enumerate(zip(topic_assignments, topic_descriptions)):
        print(f"Article {i+1}: {desc}")
    
    return df

# Example usage
if __name__ == "__main__":
    file_path = "news_analysis_2025-04-23.csv"
    processed_df = main(file_path)

