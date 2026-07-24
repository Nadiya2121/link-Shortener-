import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MovieLinkbd:MovieLinkbd@cluster0.cmx4zn5.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['neon_shortener_pro']

urls_col = db['urls']
settings_col = db['settings']
analytics_col = db['analytics']

def get_settings():
    settings = settings_col.find_one({"_id": "global_settings"})
    if not settings:
        default_data = {
            "_id": "global_settings",
            "phaseCount": 2,  # 1, 2, or 3 Phase Redirect
            "popunderCode": "",
            "directLinkUrl": "",
            "bannerTop": "",
            "bannerBottom": "",
            "nativeAd": "",
            "timerSeconds": 8
        }
        settings_col.insert_one(default_data)
        return default_data
    return settings
