from pymongo import MongoClient


client = MongoClient(
    "mongodb+srv://nanawarepranav:8veWVWADqWV16IUU@cluster0.ne7bqwg.mongodb.net/?retryWrites=true&w=majority")


db = client.NEWS_BITE


news_collection = db['news']
