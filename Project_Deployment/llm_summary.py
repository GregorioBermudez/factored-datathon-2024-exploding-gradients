import openai
from openai import OpenAI
import os
from newspaper import Article

# Set up your OpenAI API key
openai.api_key = 'sk-j_eK-pwlGxm1oyhPmahFCvdxdNeAfOPaKAiOqu1MhJT3BlbkFJsyfcey3XM89ptnxwyuSXtbszrA7r4SinH54dNXjBYA'

client = OpenAI(
    # This is the default and can be omitted
    api_key= openai.api_key
)
def extract_article_content(url):
    """Extracts the main content of the article from the URL using newspaper3k."""
    article = Article(url)
    article.download()
    try:
        article.parse()
    except:
        pass
    return article.text

def summarize_text_with_gpt4(text):
    if text == '':
        return None, None
    
    """Summarizes the provided text using GPT-4 Mini."""
    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": f'''"Please summarize the following news article in a 
            concise paragraph. After summarizing, classify the article into one of the following 3
            categories: Economical, Social or Political. Note: Don't put '**' in the text or the categories
             Input:
             "[{text}]"
             Output:
             Summary: [Generated summary of the article in plain text]
             Category: [Economical, Social or Political]",
            '''
        }
    ],
    model="gpt-4o-mini",
)
    output_text = response.choices[0].message.content
    # Extract the summary
    summary = None
    if "Summary:" in output_text:
        summary = output_text.split("Summary:")[1].split("Category:")[0].strip()

    # Extract the category
    category = None
    if "Category:" in output_text:
        category = output_text.split("Category:")[1].strip().split()[0]
        return summary, category

def summarize_news_article(url):
    """Main function to summarize a news article from a URL."""
    article_content = extract_article_content(url)
    summary, category = summarize_text_with_gpt4(article_content)
    return summary, category