# import streamlit as st
# import pandas as pd
# import ast
# from datetime import date
# from streamlit_agraph import agraph, Node, Edge, Config
# from wordcloud import WordCloud
# import matplotlib.pyplot as plt
# import numpy as np
# import random
# import re

# # ——————————————————————————————————————————
# # 1) PAGE SETUP
# # ——————————————————————————————————————————
# st.set_page_config(layout="wide")
# st.title("🗓️ Satirical News Explorer")

# # Fixed date
# fixed_date = date(2025, 4, 23)
# st.markdown(f"### News for: {fixed_date.strftime('%B %d, %Y')}")

# # ——————————————————————————————————————————
# # 2) LOAD & PREPARE DATA
# # ——————————————————————————————————————————
# df = pd.read_csv("/home/agrima/Desktop/curr-projects/News-Flare/news_with_satirical_content.csv")

# def parse_list(x):
#     if isinstance(x, str) and x.startswith("["):
#         return ast.literal_eval(x)
#     elif isinstance(x, str):
#         return [s.strip() for s in x.split(",") if s.strip()]
#     else:
#         return []
# df["Keywords"] = df["Keywords"].apply(parse_list)

# # ——————————————————————————————————————————
# # 3) SENTIMENT LABEL
# # ——————————————————————————————————————————
# def sentiment_label(compound_score):
#     try:
#         match = re.search(r"Compound: (-?\d+\.\d+)", compound_score)
#         if match:
#             compound_score = float(match.group(1))
#         else:
#             return "Invalid Sentiment"
#     except ValueError:
#         return "Invalid Sentiment"
    
#     if compound_score >= 0.05:
#         return "😊 Positive"
#     elif compound_score > -0.05:
#         return "😐 Neutral"
#     else:
#         return "😡 Negative"
    
# # ——————————————————————————————————————————
# # 4) MIND MAP OF KEYWORDS (UPDATED DESIGN)
# # ——————————————————————————————————————————
# st.subheader("🧠 Keyword Cluster")

# # Prepare the text from keywords
# text = " ".join([", ".join(keywords) for keywords in df["Keywords"]])

# # Create a more aesthetic WordCloud
# wordcloud = WordCloud(
#     width=600,
#     height=200,
#     background_color='#0e1117',  # dark background
#     max_words=50,
#     colormap="Set2",                  # nice soft colors
#     contour_color='white',             # optional white contour
#     contour_width=2,
#     min_font_size=15
# ).generate(text)

# # Display the WordCloud cleanly
# fig, ax = plt.subplots(figsize=(10, 5))
# ax.imshow(wordcloud, interpolation="bilinear")
# ax.axis("off")
# fig.patch.set_facecolor('#0e1117')  # match background behind wordcloud
# st.pyplot(fig)

# # ——————————————————————————————————————————
# # 5) TOPIC SELECTION & ARTICLE DISPLAY
# # ——————————————————————————————————————————
# st.sidebar.header("🔍 Browse by Topic")
# selected = st.sidebar.selectbox("Choose a topic", df["Dominant_Topic"].unique())

# results = df[df["Dominant_Topic"] == selected]
# st.subheader(f"Articles under “{selected}” ({len(results)})")

# for _, row in results.iterrows():
#     st.markdown(f"### 🤡 {row['Satirical_Headline']}")
#     st.write(row["Funny_Short_Summary"])
#     st.markdown(f"**Original Title:** {row['Title']}")
    
#     # Sentiment
#     sentiment = sentiment_label(row['Sentiment'])
#     st.markdown(f"**Sentiment:**")
#     sentiment_colors = {
#         "😊 Positive": "#66ff99",
#         "😐 Neutral": "#ffff66",
#         "😡 Negative": "#ff6666"
#     }
#     st.markdown(
#         f'<span style="background-color: {sentiment_colors.get(sentiment, "#999")}; '
#         f'padding: 8px 15px; border-radius: 12px; font-weight: bold; font-size: 16px">'
#         f'{sentiment}</span>', 
#         unsafe_allow_html=True
#     )
    
#     # Keywords
#     def clean_keyword(keyword):
#         return re.sub(r'[0-9.]', '', keyword)  # remove digits and dots
    
#     def pastel_color():
#         r = random.randint(180, 255)
#         g = random.randint(180, 255)
#         b = random.randint(180, 255)
#         return f"rgb({r}, {g}, {b})"

#     keywords = [clean_keyword(kw) for kw in row['Keywords']] 
#     keywords_html = "".join([
#         f'<li style="display: inline-block; background-color: {pastel_color()}; '
#         f'color: black; padding: 8px 15px; margin: 5px 5px; border-radius: 20px; '
#         f'font-size: 14px; font-weight: bold">{kw}</li>'
#         for kw in keywords
#     ])
#     st.markdown(f"<ul style='list-style-type: none; padding: 0;'>{keywords_html}</ul>", unsafe_allow_html=True)
    
#     # Article URL
#     st.markdown(f"[🔗 Read Full Article]({row['URL']})")
#     st.markdown("---")


import streamlit as st
import pandas as pd
import ast
from datetime import date
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import random
import re

# ——————————————————————————————————————————
# 1) PAGE SETUP
# ——————————————————————————————————————————
st.set_page_config(layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #0e1117;
            color: #f0f2f6;
        }
        .card {
            background-color: #1c1f26;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.6);
            margin-bottom: 25px;
        }
        .headline {
            font-size: 26px;
            font-weight: bold;
            color: #ffe599;
        }
        .summary {
            font-size: 20px;
            margin: 15px 0;
            color: #d0d0d0;
        }
        .original-title {
            font-size: 16px;
            font-style: italic;
            color: #b0b0b0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🗓️ Satirical News Explorer")

# Fixed date
fixed_date = date(2025, 4, 23)
st.markdown(f"### News for: {fixed_date.strftime('%B %d, %Y')}")

# ——————————————————————————————————————————
# 2) LOAD & PREPARE DATA
# ——————————————————————————————————————————
df = pd.read_csv("/home/agrima/Desktop/curr-projects/News-Flare/news_with_satirical_content.csv")

def parse_list(x):
    if isinstance(x, str) and x.startswith("["):
        return ast.literal_eval(x)
    elif isinstance(x, str):
        return [s.strip() for s in x.split(",") if s.strip()]
    else:
        return []
df["Keywords"] = df["Keywords"].apply(parse_list)

# ——————————————————————————————————————————
# 3) SENTIMENT LABEL
# ——————————————————————————————————————————
def sentiment_label(compound_score):
    try:
        match = re.search(r"Compound: (-?\d+\.\d+)", compound_score)
        if match:
            compound_score = float(match.group(1))
        else:
            return "Invalid Sentiment"
    except ValueError:
        return "Invalid Sentiment"
    
    if compound_score >= 0.05:
        return "😊 Positive"
    elif compound_score > -0.05:
        return "😐 Neutral"
    else:
        return "😡 Negative"
    
# ——————————————————————————————————————————
# 4) MIND MAP OF KEYWORDS
# ——————————————————————————————————————————
st.subheader("🧠 Keyword Cluster")

# Prepare text from keywords
text = " ".join([", ".join(keywords) for keywords in df["Keywords"]])

wordcloud = WordCloud(
    width=600,
    height=200,
    background_color='#0e1117',
    max_words=50,
    colormap="Set2",
    contour_color='white',
    contour_width=2,
    min_font_size=15
).generate(text)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
fig.patch.set_facecolor('#0e1117')
st.pyplot(fig)

# ——————————————————————————————————————————
# 5) TOPIC SELECTION & ARTICLE DISPLAY
# ——————————————————————————————————————————
st.sidebar.header("🔍 Browse by Topic")
selected = st.sidebar.selectbox("Choose a topic", df["Dominant_Topic"].unique())

results = df[df["Dominant_Topic"] == selected]

st.markdown(f"<h2 style='color: #f0f2f6; margin-top: 30px;'>📰 Articles under “{selected}” ({len(results)})</h2>", unsafe_allow_html=True)

for _, row in results.iterrows():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    
    # Headline
    st.markdown(f"<div class='headline'>🤡 {row['Satirical_Headline']}</div>", unsafe_allow_html=True)
    
    # Summary
    st.markdown(f"<div class='summary'>{row['Funny_Short_Summary']}</div>", unsafe_allow_html=True)
    
    # Original Title
    st.markdown(f"<div class='original-title'>Original Title: {row['Title']}</div>", unsafe_allow_html=True)
    
    # Sentiment
    sentiment = sentiment_label(row['Sentiment'])
    sentiment_colors = {
        "😊 Positive": "#66ff99",
        "😐 Neutral": "#ffff66",
        "😡 Negative": "#ff6666"
    }
    st.markdown(
        f'<div style="background-color: {sentiment_colors.get(sentiment, "#999")}; '
        f'padding: 8px 15px; border-radius: 12px; display: inline-block; '
        f'font-weight: bold; font-size: 16px; margin: 10px 0;">'
        f'{sentiment}</div>', 
        unsafe_allow_html=True
    )
    
    # Keywords
    def clean_keyword(keyword):
        return re.sub(r'[0-9.]', '', keyword)
    
    def pastel_color():
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        return f"rgb({r}, {g}, {b})"

    keywords = [clean_keyword(kw) for kw in row['Keywords']] 
    keywords_html = "".join([
        f'<li style="display: inline-block; background-color: {pastel_color()}; '
        f'color: black; padding: 8px 15px; margin: 5px 5px; border-radius: 20px; '
        f'font-size: 14px; font-weight: bold">{kw}</li>'
        for kw in keywords
    ])
    st.markdown(f"<ul style='list-style-type: none; padding: 0; margin-top: 15px;'>{keywords_html}</ul>", unsafe_allow_html=True)
    
    # Article URL
    st.markdown(f"<div style='margin-top: 20px'><a href='{row['URL']}' target='_blank' style='color: #4da6ff; font-weight: bold;'>🔗 Read Full Article</a></div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
