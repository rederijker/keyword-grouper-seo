import streamlit as st
import pandas as pd
from collections import Counter
import itertools
import re
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Keyword Grouper SEO App-Cristiano Caggiula",
    page_icon="🔑",
    layout="wide"
)

# Function to determine keyword groups based on term frequency
def group_keywords(df, stop_words, min_group_size, ngram_size, keyword_column):
    # Count the frequency of all words in keywords
    all_words = list(itertools.chain(*df[keyword_column].str.lower().str.split()))
    word_freq = Counter(all_words)
    # Select only words that are common but not too common (exclude stop words and words that are too short)
    common_terms = {word for word, freq in word_freq.items() if freq > 1 and word not in stop_words and len(word) > 2}

    # Create a list of DataFrames for the groups
    grouped_dfs = []

    # Associate each keyword with the most common term it contains
    for keyword in df[keyword_column]:
        words = re.findall(r'\b\w+\b', keyword.lower())  # Extract complete words from the keyword
        if len(words) >= ngram_size:
            ngrams = [tuple(words[i:i + ngram_size]) for i in range(len(words) - ngram_size + 1)]
            groups = set()
            for ngram in ngrams:
                if all(term in common_terms or term.isdigit() for term in ngram):  # Also consider numbers
                    groups.add(" ".join(ngram))
            if groups:
                grouped_dfs.extend([pd.DataFrame({'Group': [group], 'Keywords': [keyword]}) for group in groups])

    # Concatenate the DataFrames in the list into a single DataFrame
    grouped_keywords_df = pd.concat(grouped_dfs, ignore_index=True)

    # Filter groups with a minimum size
    filtered_groups = grouped_keywords_df.groupby('Group').filter(lambda x: len(x) >= min_group_size)

    return filtered_groups

# Function to calculate the total clicks for each group
def calculate_click_totals(df, grouped_df, keyword_column, clicks_column):
    click_totals = {}
    for group in grouped_df['Group'].unique():
        keywords_in_group = grouped_df[grouped_df['Group'] == group]['Keywords'].tolist()
        click_total = df[df[keyword_column].isin(keywords_in_group)][clicks_column].sum()
        click_totals[group] = click_total
    return click_totals

# Streamlit user interface
st.title("Keyword Grouper SEO App")
st.markdown("made in Streamlit 🎈 by [Cristiano Caggiula](https://www.linkedin.com/in/cristiano-caggiula/)")
st.write("The app cluster keywords extracted from Google Search Console and more. The app groups the keywords and, for each group, it is possible to see the total number of clicks, to identify the most profitable groups in terms of traffic.")
st.divider()
# Allow the user to choose the language (English or Italian) and modify the stop words dictionary

col1, col2 = st.columns(2)
with col1:    
    st.subheader ("💬 Select language")
    language = st.selectbox("", ["English", "Italian"])

    if language == "English":
        st.write("")
        default_stop_words = [
            'and', 'but', 'is', 'the', 'to', 'in', 'for', 'on', 'with', 'as', 'by', 'at', 'from',
            'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only',
            'own', 'same', 'so', 'than', 'too', ' very', 's', 't', 'can', 'will', 'just', 'don', 
            'should', 'now'
        ]
    else:
        st.write("")
        default_stop_words = [
            'a', 'adesso', 'ai', 'al', 'alla', 'allo', 'allora', 'altre',
            'altri', 'altro', 'anche', 'ancora', 'avere', 'aveva', 'avevano',
            'ben', 'buono', 'che', 'chi', 'cinque', 'comprare', 'con',
            'consecutivi', 'consecutivo', 'cosa', 'cui', 'da', 'del', 'della',
            'dello', 'dentro', 'deve', 'devo', 'di', 'doppio', 'due', 'e',
            'ecco', 'fare', 'fine', 'fino', 'fra', 'gente', 'giu', 'ha', 'hai',
            'hanno', 'ho', 'il', 'indietro', 'invece', 'io', 'la', 'lavoro',
            'le', 'lei', 'lo', 'loro', 'lui', 'lungo', 'ma', 'me', 'meglio',
            'molta', 'molti', 'molto', 'nei', 'nella', 'no', 'noi', 'nome',
            'nostro', 'più', 'se', 'o', 'per', 'un', 'una'
        ]

# Text area for custom stop words
    with st.expander("Customize Stop Words"):
        custom_stop_words = st.text_area("One per line", "\n".join(default_stop_words))
        stop_words = [word.strip() for word in custom_stop_words.split('\n') if word.strip()]
with col2:
    st.text("")
st.divider()
st.subheader("⬆️ Upload Keyword CSV")
tab1, tab2 = st.tabs(["Keywords and Clicks", "Keywords only"]) # File upload widget for keywords with clicks
with tab1:
    uploaded_file = st.file_uploader("CSV with Keywords and Clicks", type=["csv"])
with tab2:
    uploaded_file_without_clicks = st.file_uploader("Upload your CSV with Keywords only (no Clicks)", type=["csv"])

# Control for minimum group size and tuple length
min_group_size, ngram_size = st.columns(2)
with min_group_size:
    min_group_size = st.slider("Minimum Group Size",
                               min_value=1,
                               max_value=50,
                               value=2,
                               help="The minimum group size is the minimum number of keywords required in a group for it to be displayed in the results. Increase this value to show only larger keyword groups."
                              )

with ngram_size:
    ngram_size = st.slider(
    "Length of the keyword", 
    min_value=1, 
    max_value=5, 
    value=2, 
    help="Drag the slider to choose the n-gram size for the keyword. An n-gram size of 1 means a single word, whereas 5 means a phrase of up to 5 words."
)

# Column mapping for keywords with clicks
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    columns = data.columns
    
    st.write("Map CSV columns to the required fields 👇")
    
    keyword_column = st.selectbox(" Keyword Column is:", columns)
    clicks_column = st.selectbox("Clicks Column is:", columns)
    
    if st.button("Group Keywords with Clicks ✨"):
        with st.spinner("Grouping..."):
            if keyword_column in data.columns and clicks_column in data.columns:
                # Group keywords with clicks, passing the list of stop words, the minimum size, and the tuple length as arguments
                grouped_keywords_df = group_keywords(data, stop_words, min_group_size, ngram_size, keyword_column=keyword_column)
                
                # Calculate the total clicks for each group
                click_totals = calculate_click_totals(data, grouped_keywords_df, keyword_column=keyword_column, clicks_column=clicks_column)
                
                # Sort groups by total clicks in descending order
                sorted_groups = sorted(click_totals.items(), key=lambda x: x[1], reverse=True)
                top_groups = sorted_groups[:5]
                tab1, tab2 = st.columns([2, 2])
                # Expand each group to show keywords and clicks
                with tab1:
                    st.subheader("🔑 Groups")
                    for group, total_clicks in sorted_groups:
                        with st.expander(f"{group} - Total Clicks: {total_clicks}"):
                            keywords_list = grouped_keywords_df[grouped_keywords_df['Group'] == group]['Keywords'].tolist()
                            keyword_clicks_df = data[data[keyword_column].isin(keywords_list)][[keyword_column, clicks_column]]
                            st.write(keyword_clicks_df)
                with tab2:                   
                    # Plot histogram for the top 5 groups by clicks
                    top_groups_clicks = [click for group, click in top_groups]
                    top_group_names = [group for group, click in top_groups]

                    if len(top_groups) > 0:
                        fig, ax = plt.subplots()
                        ax.barh(top_group_names, top_groups_clicks)
                        ax.set_xlabel('Total Clicks')
                        ax.set_ylabel('Group Name')
                        ax.set_title('Top 5 Groups by Clicks')
                        st.pyplot(fig)

# Column mapping for keywords without clicks from uploaded file
if uploaded_file_without_clicks is not None:
    data_without_clicks = pd.read_csv(uploaded_file_without_clicks)
    columns_without_clicks = data_without_clicks.columns
    
    st.write("Map the CSV columns to the required fields for Keywords without Clicks from Uploaded File:")
    
    keyword_column_without_clicks = st.selectbox("Keyword Column is:", columns_without_clicks)
    
    if st.button("Group Keywords without Clicks from Uploaded File ✨"):
        with st.spinner("Grouping..."):
            if keyword_column_without_clicks in data_without_clicks.columns:
                # Group keywords without clicks from the uploaded CSV
                grouped_keywords_without_clicks_df = group_keywords(data_without_clicks, stop_words, min_group_size, ngram_size, keyword_column=keyword_column_without_clicks)
                tab4, tab5 = st.columns([2, 2])
                # Expand each group to show keywords in an expander
                with tab4:
                    st.subheader("🔑 Groups")
                    for group in grouped_keywords_without_clicks_df['Group'].unique():
                        keywords_list = grouped_keywords_without_clicks_df[grouped_keywords_without_clicks_df['Group'] == group]['Keywords'].tolist()
                        if len(keywords_list) >= min_group_size:
                            with st.expander(f"{group}"):
                                keyword_group_df = pd.DataFrame({'Keywords': keywords_list})
                                st.table(keyword_group_df)
            else:
                st.error(f"Column '{keyword_column_without_clicks}' not found in the uploaded CSV for Keywords without Clicks from Uploaded File.")
