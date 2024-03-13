from datetime import datetime
from fastapi_utilities import repeat_every
from fastapi import APIRouter
from models.news import News
from config.database import news_collection
from gnews import GNews
from transformers import pipeline


from news_fetcher import fetch_news

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


router = APIRouter()

google_news = GNews(language='en', country='US', period='1d')


@router.on_event('startup')
@repeat_every(seconds=43200)
async def curate_news():
    try:
        res = fetch_news()
        for data in res:
            existing_news_item = news_collection.find_one(
                {"title": data["title"]})
            if existing_news_item is None and data['url'] is not None:
                content = google_news.get_full_article(data['url'])
                if content is not None and data['author'] is not None:
                    news_item = News(
                        title=data["title"],
                        description=data["description"] if data.get(
                            "description") else "",
                        published_date=datetime.fromisoformat(
                            data['publishedAt'].rstrip('Z')),
                        url=data["url"],
                        category=data['category'],
                        summary="",
                        content=content.text,
                        image_url=data['image_url'],
                        summarized=False,
                        author=data['author'],
                    )
                    news_collection.insert_one(dict(news_item))
    except Exception as e:
        print(e)


@router.on_event('startup')
# Consider adjusting the frequency based on your needs
@repeat_every(seconds=300)
async def summarize():
    try:
        news = news_collection.find({'summarized': False})

        for data in news:
            summary = summarizer(
                data['content'].strip(), max_length=120, truncation=True)
            data['summary'] = summary[0]['summary_text']
            data['summarized'] = True
            print(data)
            updated_news = news_collection.update({'_id': data['_id']}, data)
            print(updated_news)
            print("Done")
    except Exception as e:
        print(e)
