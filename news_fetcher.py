import requests

categories = ['business', 'entertainment', 'general',
              'health', 'science', 'sports', 'technology']


def fetch_news_for_category(category):
    url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'country': 'us',
        'category': category,
        'apiKey': 'd1feae6822754dd1aca9284adf71b7a2'
    }

    news_list = []  # List to store news articles for the category

    try:
        response = requests.get(url, params=params)
        # Raises an HTTPError if the response status code is 4XX or 5XX
        response.raise_for_status()
        news_data = response.json()

        if news_data.get('articles'):
            for article in news_data['articles']:
                news_item = {
                    'title': article.get('title'),
                    'url': article.get('url'),
                    'author': article.get('author'),
                    'description': article.get('description'),
                    'publishedAt': article.get('publishedAt'),
                    'category': category,
                    # Fix: Removed the comma after 'image_url'
                    'image_url': article.get('urlToImage') or ""
                }
                news_list.append(news_item)
    except requests.RequestException as e:
        print(f"Request failed: {e}")

    return news_list


def fetch_news():
    all_news = []
    for category in categories:
        category_news = fetch_news_for_category(category)
        all_news.extend(category_news)
    return all_news
