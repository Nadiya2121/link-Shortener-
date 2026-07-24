import os
from pymongo import MongoClient

# Your original MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://MovieLinkbd:MovieLinkbd@cluster0.cmx4zn5.mongodb.net/?appName=Cluster0")
client = MongoClient(MONGO_URI)
db = client['neon_saas_db']

users_col = db['users']
urls_col = db['urls']
settings_col = db['settings']
analytics_col = db['analytics']
withdrawals_col = db['withdrawals']

# Your original Telegram Bot Token
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
            "phaseCount": 2,
            "cpmRate": 1.0,        # ডিফল্ট $১.০০ ডলার প্রতি ১০০০ ভিউতে
            "minWithdraw": 2.0,    # ডিফল্ট $২.০০ ডলার মিনিমাম উইথড্র
            "cpmRates": {
                "US": 10.0, "UK": 8.0, "CA": 8.0, 
                "BD": 3.0, "IN": 2.5, "DEFAULT": 1.0
            }
        }
        settings_col.insert_one(default_data)
        return default_data
    
    # অটো-আপডেট: আগের ডাটাবেসে এই ফিল্ডগুলো না থাকলে যুক্ত হয়ে যাবে
    if "cpmRate" not in settings:
        settings_col.update_one({"_id": "global_settings"}, {"$set": {"cpmRate": 1.0, "minWithdraw": 2.0}})
        settings = settings_col.find_one({"_id": "global_settings"})
        
    return settings
