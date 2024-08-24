import nltk
from newspaper import Article
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from heapq import nlargest

def fetch_article(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

def summarize(text, num_sentences=5):
    sentences = sent_tokenize(text)
    words = [word.lower() for sentence in sentences for word in sentence.split() if word.lower() not in stopwords.words('english')]
    
    freq = FreqDist(words)
    
    ranking = {}
    
    for i, sentence in enumerate(sentences):
        for word in sentence.split():
            if word.lower() in freq:
                if i in ranking:
                    ranking[i] += freq[word.lower()]
                else:
                    ranking[i] = freq[word.lower()]
    
    indexes = nlargest(num_sentences, ranking, key=ranking.get)
    final_sentences = [sentences[j] for j in sorted(indexes)]
    return ' '.join(final_sentences)

def summarize_news(url):
    article_text = fetch_article(url)
    summary = summarize(article_text)
    return summary

def main():
    urls = []
    while True:
        url = input("Enter a news article URL (or press Enter to finish): ")
        if url == "":
            break
        urls.append(url)
    
    for i, url in enumerate(urls, 1):
        try:
            print(f"\nProcessing article {i}:")
            article_text = fetch_article(url)
            summary = summarize(article_text)
            print(f"Summary of {url}:")
            print(summary)
            print("-" * 50)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    #main()