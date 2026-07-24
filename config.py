import os
from pymongo import MongoClient

# MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MovieLinkbd:MovieLinkbd@cluster0.cmx4zn5.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['neon_shortener']

# MongoDB Collections
urls_col = db['urls']
settings_col = db['settings']
analytics_col = db['analytics']

# Default Ad Settings Get Helper
def get_settings():
    settings = settings_col.find_one({"_id": "global_settings"})
    if not settings:
        default_data = {
            "_id": "global_settings",
            "popunderCode": "",
            "directLinkUrl": "",
            "bannerTop": "",
            "bannerBottom": "",
            "nativeAd": "",
            "timerSeconds": 10
        }
        settings_col.insert_one(default_data)
        return default_data
    return settings
