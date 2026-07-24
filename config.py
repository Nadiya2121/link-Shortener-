import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MovieLinkbd:MovieLinkbd@cluster0.cmx4zn5.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['neon_saas_db']

users_col = db['users']
urls_col = db['urls']
settings_col = db['settings']
analytics_col = db['analytics']
withdrawals_col = db['withdrawals']

# Telegram Bot Token (Set your token here)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8658306833:AAE6n9VyvnzYob2iSp1TpjmWwaU18FmiGCQ")

def get_settings():
    settings = settings_col.find_one({"_id": "global_settings"})
    if not settings:
        default_data = {
            "_id": "global_settings",
            "primaryDomain": "cloudlink.pro",
            "backupDomain": "cloudlink-backup.pro",
            "popunderCode": "",
            "directLinkUrl": "",
            "bannerTop": "",
            "bannerBottom": "",
            "nativeAd": "",
            "timerSeconds": 8,
            # CPM Rates per 1000 views in USD
            "cpmRates": {
                "US": 10.0, "UK": 8.0, "CA": 8.0, 
                "BD": 3.0, "IN": 2.5, "DEFAULT": 2.0
            }
        }
        settings_col.insert_one(default_data)
        return default_data
    return settings
