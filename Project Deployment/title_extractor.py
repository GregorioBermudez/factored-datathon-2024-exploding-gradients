from newspaper import Article

def extract_article_text(url):
    article = Article(url)
    article.download()
    try:
        article.parse()
    except:
        pass
    return article.title