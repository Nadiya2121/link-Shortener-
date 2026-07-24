আপনার প্রজেক্টের জন্য একটি সম্পূর্ণ প্রফেশনাল, দৃষ্টিনন্দন এবং বিস্তারিত **`README.md`** ফাইল তৈরি করে দেওয়া হলো। 

যেকোনো নতুন ডেভেলপার বা আপনি নিজে ভবিষ্যতে এই ফাইলটি পড়লে ১ মিনিটে বুঝে যাবেন প্রজেক্টটি কীভবে তৈরি করা হয়েছে, কোডের কোথায় কী আছে এবং কীভাবে এটি রেন্ডারে হোস্ট করতে হয়।

---

### 📜 `README.md` (কপি-পেস্ট করার জন্য প্রস্তুত)

```markdown
# ⚡ CloudLink Pro - High-Yield URL Shortener & Monetization SaaS

**CloudLink Pro** হলো একটি সম্পূর্ণ প্রফেশনাল, হাই-পারফর্ম্যান্স এবং মাল্টি-ফিচার সম্বলিত **URL Shortener & Publisher Monetization Platform**। এতে রয়েছে অ্যাডস্টাররা (AdSterra) বিজ্ঞাপন নেটওয়ার্ক ইন্টিগ্রেশন, অটোমেটেড টেলিগ্রাম বোট, বিকাশ/নগদ/রকেট পেমেন্ট উইথড্রয়াল সিস্টেম, কাস্টম স্লাগ, পাসওয়ার্ড সিকিউরিটি এবং ডার্ক নিয়ন থিম (Cyberpunk Glowing UI)।

---

## 🚀 প্রধান ফিচারসমূহ (Core Features)

### 👤 ১. ইউজার অথেনটিকেশন ও সিকিউরিটি (User Auth & Privacy)
- **রেজিস্ট্রেশন ও লগইন:** ইউজার নাম, ইমেইল ও পাসওয়ার্ড দিয়ে একাউন্ট খোলার সুবিধা (`/register`, `/login`)।
- **ইউজার প্রাইভেসী:** প্রতিটি ইউজার কেবল তার নিজের তৈরি করা লিংক এবং আয়ের তথ্য দেখতে পারে।
- **পাসওয়ার্ড রিকভারি:** কোনো ইউজার পাসওয়ার্ড ভুলে গেলে এডমিন প্যানেল থেকে ১-ক্লিকে পাসওয়ার্ড রিসেট করে দেওয়ার অপশন।
- **User Block/Unblock System:** স্প্যামার বা বোট ইউজারদের এডমিন প্যানেল থেকে ব্লক করার সুবিধা।

### 💰 ২. পাবলিশার আয় ও উইথড্রয়াল (Publisher Earnings & Withdrawals)
- **Dynamic CPM Rates:** এডমিন প্যানেল থেকে প্রতি ১,০০০ ক্লিকে ইউজারদের কত টাকা দেওয়া হবে (যেমন: $1.00/1000 views) তা সেট করার সুবিধা।
- **লোকাল পেমেন্ট গেটওয়ে:** বিকাশ (bKash), নগদ (Nagad) এবং রকেট (Rocket)-এর মাধ্যমে টাকা উইথড্র করার সুবিধা।
- **উইথড্রয়াল স্ট্যাটাস:** ইউজারদের জন্য `Pending`, `Approved` এবং `Rejected & Refunded` স্ট্যাটাস ট্র্যাকিং।
- **স্মার্ট রিফান্ড সিস্টেম:** ভুল অ্যাকাউন্ট নম্বর দিলে এডমিন ১ ক্লিকে রিজেক্ট করলে টাকা ইউজারের ওয়ালেটে ফেরত চলে যায়।

### 🔀 ৩. স্মার্ট রিডাইরেকশন ও অ্যাড কন্ট্রোল (Multi-Phase & AdSterra Control)
- **Dynamic Phase System:** এডমিন প্যানেল থেকে ১-ফেজ, ২-ফেজ বা ৩-ফেজ রিডাইরেকশন অন/অফ করার সুবিধা।
- **AdSterra Management:** কোড পরিবর্তন না করে এডমিন প্যানেল থেকে Popunder, Direct Link, Banner Top, Banner Bottom এবং Native Ads বসানোর অপশন।
- **Domain Rotator & Anti-Block:** ফেসবুক বা হোয়াটসঅ্যাপে লিংক ব্লক হওয়া ঠেকানোর জন্য ক্লাউডফ্লেয়ার ও টেক আর্টিকেলের ছদ্মবেশ (Masking Content)।

### 🤖 ৪. অটোমেটেড টেলিগ্রাম বোট (Telegram Bot Engine)
- **Background Threading:** ওয়েব সার্ভারের ভেতরেই ব্যাকগ্রাউন্ড থ্রেডে বোট স্বয়ংক্রিয়ভাবে চালু থাকে।
- **ইনস্ট্যান্ট শর্টনার:** টেলিগ্রাম বোটে যেকোনো বড় লিংক পাঠালেই ১ সেকেন্ডে শর্ট লিংক তৈরি করে দেয়।
- **১-ক্লিক কপি টেক্সট:** টেলিগ্রাম থেকে শর্ট লিংকে ট্যাপ করলেই কপি হয়ে যায়।

---

## 📂 ফাইল আর্কিটেকচার (Flat Structure)

প্রজেক্টটি কোনো জটিল ফোল্ডার ছাড়া একদম সহজ **৪টি মূল ফাইল** দিয়ে তৈরি করা হয়েছে:

```text
cloudlink-pro/
├── config.py         # ডাটাবেস কানেকশন, মঙ্গোডিবি কালেকশন ও পরিবেশ ভেরিয়েবল
├── admin.py          # এডমিন ড্যাশবোর্ড, অ্যাড কন্ট্রোল, ইউজার ব্লক ও উইথড্রয়াল ম্যানেজমেন্ট
├── main.py           # মূল ওয়েব সার্ভার, সাইনআপ/লগইন, ইউজার ড্যাশবোর্ড, ফেজ পেজ ও টেলিগ্রাম বোট
└── requirements.txt  # প্রজেক্টের প্রয়োজনীয় সব পাইথন প্যাকেজ তালিকা
```

---

## 🛠️ টেকনোলজি স্ট্যাক (Tech Stack)

- **Backend:** Python 3.x, Flask Framework
- **Database:** MongoDB Atlas (PyMongo Engine)
- **Bot Engine:** PyTelegramBotAPI (`telebot`)
- **Frontend & Design:** HTML5, Tailwind CSS (CDN), FontAwesome Icons
- **WSGI / Deployment:** Gunicorn (Render Web Service Ready)

---

## ⚙️ এনভারনমেন্ট ভেরিয়েবলসমূহ (Environment Variables)

সাইটটি চালানোর জন্য নিচের ভেরিয়েবলগুলো প্রজেক্টের `.env` ফাইলে অথবা **Render Environment Settings** এ দিতে হবে:

| Variable Name | Description | Example Value |
| :--- | :--- | :--- |
| `MONGO_URI` | MongoDB Atlas Connection String | `mongodb+srv://user:pass@cluster.mongodb.net/...` |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot API Token from @BotFather | `8658306833:AAE6n9Vyvnz...` |
| `PORT` | Web Server Port (Auto handled by Render) | `5000` |

---

## 🌐 রাউটিং ম্যাপ (All Routes Overview)

### 🟢 Public / User Routes (`main.py`):
- `GET /` -> ইউজার লগইন থাকলে ড্যাশবোর্ড দেখাবে, না থাকলে `/login` এ রিডাইরেক্ট করবে।
- `GET /login` & `POST /login` -> ইউজার লগইন পেজ।
- `GET /register` & `POST /register` -> নতুন পাবলিশার একাউন্ট খোলার পেজ।
- `GET /logout` -> ইউজার সেশন রিমুভ করে লগআউট করবে।
- `POST /shorten` -> কাস্টম এলিয়াস ও পাসওয়ার্ড সহ লিংক শর্ট করবে।
- `POST /withdraw` -> বিকাশ/নগদ/রকেটে পেমেন্ট রিকোয়েস্ট পাঠাবে।
- `GET /go/<code>` -> রিডাইরেকশনের Phase 1 এ পাঠাবে।
- `GET /go/<code>/phase/<phase_num>` -> মাল্টি-ফেজ টাইমার ও বিজ্ঞাপনের পেজ।
- `GET /final/<code>` -> ক্লিক কাউন্ট হিসাব করে মূল লিংকে নিয়ে যাবে।

### 🔴 Admin Routes (`admin.py`):
- `GET /admin` -> মাস্টার এডমিন ড্যাশবোর্ড।
- `POST /admin/save` -> অ্যাড কোড, টাইমার, CPM Rate ও মিনিমাম উইথড্র সেটিংস সেভ করা।
- `POST /admin/reset_user_password` -> যেকোনো ইউজারের পাসওয়ার্ড বদলে দেওয়া।
- `GET /admin/toggle_block_user/<username>` -> ইউজার ব্লক বা আনব্লক করা।
- `GET /admin/approve_withdrawal/<id>` -> পেমেন্ট এপ্রুভ ও Paid করা।
- `GET /admin/reject_withdrawal/<id>` -> পেমেন্ট রিজেক্ট করে ইউজারের ব্যালেন্স রিফান্ড করা।

---

## 🚀 লোকাল পিসিতে সেটআপ নির্দেশিকা (Local Setup)

১. প্রজেক্টের ফাইলগুলো একটি ফোল্ডারে নামিয়ে টার্মিনাল ওপেন করুন:
```bash
git clone https://github.com/your-username/cloudlink-pro.git
cd cloudlink-pro
```

২. প্রয়োজনীয় ডিপেন্ডেন্সি ইন্সটল করুন:
```bash
pip install -r requirements.txt
```

৩. অ্যাপ্লিকেশন রান করুন:
```bash
python main.py
```
এখন ব্রাউজারে `http://127.0.0.1:5000` এ ঢুকলেই প্রজেক্ট লাইভ দেখতে পাবেন!

---

## ☁️ Render.com হোস্টিং নির্দেশিকা (Deployment)

১. এই কোডগুলো আপনার **GitHub Repository**-তে Push করুন।
2. **Render.com** এ গিয়ে **New Web Service** সিলেক্ট করুন।
3. আপনার GitHub রিপোজিটরি টি সিলেক্ট করুন।
4. **Environment:** `Python 3` সিলেক্ট করুন।
5. **Start Command:**
   ```bash
   gunicorn main:app
   ```
6. **Environment Variables** এ গিয়ে `MONGO_URI` এবং `TELEGRAM_BOT_TOKEN` যোগ করে Deploy বাটনে ক্লিক করুন!

---

© 2026 **CloudLink Pro SaaS Engine**. All Rights Reserved.
```
