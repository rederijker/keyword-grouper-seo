# Keyword Grouper SEO App

## Introduction
The Keyword Grouper SEO App is a Streamlit-based tool designed for digital marketers, SEO professionals, and content creators to optimize their keyword strategy. It clusters semantically related search terms to uncover patterns and opportunities within search data, typically sourced from tools like Google Search Console.

By grouping similar keywords, the app facilitates the identification of high-impact areas for SEO and content creation, allowing users to focus their efforts on search queries that drive traffic and conversions.

## What is a Keyword Grouper?
A keyword grouper is an analytical tool that organizes keywords into related groups based on common terms and phrases. It provides an aggregated view of search queries, revealing how users are searching for topics related to your content or business.

## Why is it Useful for SEO?
- **User Intent Understanding**: It helps you understand the intent behind search queries, which can inform content creation and website structure decisions.
- **SEO Focus**: By spotting high-performing keyword groups, you can focus your SEO efforts on optimizing for the most profitable clusters.
- **Content Gap Identification**: Identifying clusters with lower performance might highlight opportunities for content that can address those gaps.
- **Improves Ad Relevance**: For PPC campaigns, keyword clusters enable you to create ad groups with high relevance, potentially reducing cost-per-click and improving ad performance.

## Key App Features
- **Algorithm-Driven Grouping**: The app utilizes a tailored algorithm for clustering keywords based on term frequency, n-gram size, and a configurable list of stop words, leading to meaningful keyword groupings.
- **Custom Stop Words**: Modify the app's stop word list to better fit your keyword data and improve the relevance of your keyword groups.
- **Click Data Analysis**: If click data is provided, it calculates the total clicks for each keyword group, a metric indicative of traffic potential.
- **Bilingual Functionality**: Capable of handling both English and Italian datasets, broadening the app's usability to multiple markets.
- **Visual Results**: Offers a visualization component, such as a bar chart for comparing the top keyword groups based on clicks, enhancing the interpretation of clustering results.

## Using the App

### Before You Start
- **Language Selection**: Choose between English and Italian for the app's stop word list and interface language.
- **Stop Words Customization**: Input a list of words you wish to exclude from being used to form keyword groups.

### Uploading Data
- **File Upload**: Drag and drop a CSV file containing your keyword data into the upload area.
- **CSV Configuration**: Align the CSV columns with the app's fields to analyze the keyword and (optional) click data correctly.

### Analyzing Keywords
- **Parameter Settings**: Adjust the minimum group size and the n-gram size to fine-tune the grouping granularities.
- **Processing**: Use the "Group Keywords" button to start the clustering algorithm.
- **Viewing Results**: Explore the tabulated keyword groups and see the top groups displayed in a chart.
- **Outcome**: Review and use the insights from the keyword clusters to optimize your SEO strategy and content plans.

## Algorithm Details
The detailed steps of the keyword grouping algorithm are as follows:

- **Term Frequency Calculation**: Starting with the inputted keyword list, the algorithm computes the frequency of each term, excluding default and custom stop words and terms that are below a minimum character threshold.
  
- **Group Identification**: Using word frequency data, it forms keyword groups by associating keywords with common terms, ensuring each keyword group contains terms that exceed the set frequency threshold.

- **Group Refinement**: It further refines the groups based on user-defined settings, such as minimum group size and n-gram size, to ensure relevance and specificity.

- **Click Data Aggregation**: For keyword groups, if click data is available, the algorithm aggregates the total clicks for each group, providing a performance metric for each cluster.

- **Result Display and Visualization**: The algorithm presents sorted keyword groups and visualizations of their performance in an interactive and user-friendly interface.

## App Demo
Experience the app live and start optimizing your keyword strategy: [Keyword Grouper App Demo](https://keyword-grouper.streamlit.app/).

## Conclusion
Maximize the potential of your keyword data with the Keyword Grouper SEO App. It's more than just a tool; it's an essential asset in your SEO and content marketing arsenal, enabling you to make data-driven decisions for better search visibility and engagement. Your feedback and suggestions are always welcome to improve future versions of the app. Happy keyword grouping!
