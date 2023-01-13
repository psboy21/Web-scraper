from flask import Flask
from flask_pymongo import pymongo
# from scrapy import app

client = pymongo.MongoClient("mongodb+srv://psboy:7275108566@priyanshu.ztikbux.mongodb.net/?retryWrites=true&w=majority")
#db = client.test
dba = client.get_database('flask_mongodb_atlas')
collection = pymongo.collection.Collection(dba, 'amazon_data')
collection_daily = pymongo.collection.Collection(dba, 'daily_price_update')