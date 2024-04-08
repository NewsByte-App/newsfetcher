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


# @router.on_event('startup')
# @repeat_every(seconds=100000)
# async def download_model():
#     model_name = "facebook/bart-large-cnn"
#     tokenizer = BartTokenizer.from_pretrained(model_name)
#     model = BartForConditionalGeneration.from_pretrained(model_name)

#     model.save_pretrained('./model_data/bart-large-cnn')
#     tokenizer.save_pretrained('./model_data/bart-large-cnn')


@router.on_event('startup')
@repeat_every(seconds=10)
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
                        summary=summarizer(
                            content.text.strip(), max_length=120, truncation=True)[0]['summary_text'],
                        content=content.text,
                        image_url=data['image_url'],
                        summarized=True,
                        author=data['author'],
                    )
                    news_collection.insert_one(dict(news_item))
                    print("Fetched")

    except Exception as e:
        print(e)


# @router.on_event('startup')
# # Consider adjusting the frequency based on your needs
# @repeat_every(seconds=300)
# async def summarize():
#     try:
#         news = news_collection.find({'summarized': False})

#         for data in news:
#             summary = summarizer(
#                 data['content'].strip(), max_length=120, truncation=True)
#             data['summary'] = summary[0]['summary_text']
#             data['summarized'] = True
#             news_collection.update({'_id': data['_id']}, data)
#             print("Summarized")
#     except Exception as e:
#         print(e)
