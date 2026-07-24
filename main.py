import random, string, datetime, threading, uuid
from flask import Flask, request, redirect, render_template_string, session, url_for
from user_agents import parse
import telebot
from config import urls_col, analytics_col, users_col, withdrawals_col, get_settings, TELEGRAM_BOT_TOKEN
from admin import admin_bp

app = Flask(__name__)
app.secret_key = "super_secret_saas_key_998877"
app.register_blueprint(admin_bp)

def generate_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# ==========================================
# 🤖 TELEGRAM BOT ENGINE (CONFLICT FREE THREAD)
# ==========================================
def start_telegram_bot():
    if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        try:
            bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

            # ১. আগের জটলা ও পুরানো পন্ডিং রিকোয়েস্ট ডিলিট করা
            try:
                bot.remove_webhook(drop_pending_updates=True)
            except Exception:
                pass

            # /start and /help Command Response
            @bot.message_handler(commands=['start', 'help'])
            def send_welcome(message):
                welcome_text = (
                    "⚡ *Welcome to CloudLink Pro Bot!*\n\n"
                    "I am your automated URL Shortener Bot. Send me any long link, and I will convert it into a short, protected link in 1 second!\n\n"
                    "📌 *How to Use Me?*\n"
                    "1️⃣ Copy any long URL (must start with `http://` or `https://`)\n"
                    "2️⃣ Paste and send the link in this chat\n"
                    "3️⃣ Receive your shortened link instantly!\n\n"
                    "🚀 *Send your first link now!*"
                )
                bot.reply_to(message, welcome_text, parse_mode='Markdown')

            # Handle incoming long URLs
            @bot.message_handler(func=lambda message: True)
            def process_url(message):
                long_url = message.text.strip()
                if long_url.startswith("http://") or long_url.startswith("https://"):
                    code = generate_code()
                    urls_col.insert_one({
                        "code": code,
                        "url": long_url,
                        "owner": f"tg_{message.from_user.id}",
                        "clicks": 0
                    })
                    
                    short_url = f"https://link-shortener-4obu.onrender.com/go/{code}"
                    success_text = (
                        "✅ *Link Shortened Successfully!*\n\n"
                        f"🔗 *Your Short Link:*\n`{short_url}`\n\n"
                        "💡 _Tap on the link above to copy it instantly!_"
                    )
                    bot.reply_to(message, success_text, parse_mode='Markdown')
                else:
                    bot.reply_to(message, "⚠️ *Invalid Link Format!*\nPlease send a valid link starting with `http://` or `https://`", parse_mode='Markdown')

            print("🤖 Telegram Bot Engine Running Cleanly!")
            # skip_pending=True ব্যবহারে কনফ্লিক্ট এরর আসবে না
            bot.infinity_polling(none_stop=True, skip_pending=True)
        except Exception as e:
            print(f"❌ Telegram Bot Thread Handled: {e}")

threading.Thread(target=start_telegram_bot, daemon=True).start()


# ==========================================
# 🌐 FIXED USER DASHBOARD (PRIVACY & COPY FIX)
# ==========================================
USER_DASHBOARD = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publisher Dashboard - CloudLink Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-white min-h-screen p-4 md:p-8 font-sans">
    <div class="max-w-5xl mx-auto space-y-6">
        
        <!-- Header & Balance -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center bg-slate-900 p-6 rounded-2xl border border-slate-800 gap-4">
            <div>
                <h1 class="text-xl font-bold text-cyan-400 flex items-center gap-2">
                    <i class="fa-solid fa-user-shield"></i> {{ user.username }}
                </h1>
                <p class="text-xs text-slate-400">Private Publisher Session</p>
            </div>
            <div class="bg-slate-950 px-5 py-3 rounded-xl border border-slate-800 text-right w-full md:w-auto">
                <span class="text-xs text-slate-500 block">AVAILABLE BALANCE</span>
                <span class="text-2xl font-black text-emerald-400">${{ "%.2f"|format(user.balance) }}</span>
            </div>
        </div>

        <!-- Shorten Link Form -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-cyan-500/30 shadow-xl">
            <h2 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                <i class="fa-solid fa-link text-cyan-400"></i> Create Short Link
            </h2>
            <form action="/shorten" method="POST" class="space-y-4">
                <input type="url" name="url" placeholder="Paste Destination Long URL here..." required 
                    class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400 break-all">
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <input type="text" name="custom_alias" placeholder="Custom Alias (Optional, e.g. my-file)" 
                        class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-cyan-300 focus:outline-none">
                    <input type="password" name="password" placeholder="Protection Password (Optional)" 
                        class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-fuchsia-300 focus:outline-none">
                </div>
                
                <button type="submit" class="w-full py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black rounded-xl hover:scale-101 transition shadow-[0_0_15px_rgba(6,182,212,0.4)]">
                    SHORTEN LINK ⚡
                </button>
            </form>
        </div>

        <!-- Withdrawal Section -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 class="text-lg font-bold text-emerald-400"><i class="fa-solid fa-wallet mr-2"></i>Withdraw Earnings</h2>
            <form action="/withdraw" method="POST" class="flex flex-col md:flex-row gap-3">
                <input type="number" step="0.1" name="amount" placeholder="Amount ($)" required class="p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white">
                <select name="method" class="p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-cyan-400">
                    <option value="bKash">bKash</option>
                    <option value="Nagad">Nagad</option>
                    <option value="Binance/Crypto">Binance (USDT)</option>
                </select>
                <input type="text" name="account" placeholder="Account No / Wallet Address" required class="flex-grow p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white">
                <button type="submit" class="px-6 py-3 bg-emerald-500 text-slate-950 font-bold rounded-xl hover:bg-emerald-400">WITHDRAW</button>
            </form>
        </div>

        <!-- Private User Links Table (FIXED OVERFLOW & 1-CLICK COPY) -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h2 class="text-lg font-bold text-slate-200"><i class="fa-solid fa-lock text-cyan-400 mr-2"></i>Your Private Short Links</h2>
                <span class="text-xs text-slate-500">{{ links|length }} Items</span>
            </div>

            {% if links %}
            <div class="space-y-3">
                {% for item in links %}
                <div class="p-4 bg-slate-950 rounded-xl border border-slate-800/80 flex flex-col md:flex-row justify-between items-start md:items-center gap-3 overflow-hidden">
                    
                    <!-- Link Details (Overflow Protected) -->
                    <div class="space-y-1 min-w-0 w-full md:w-3/4">
                        <p class="text-xs text-slate-500 truncate w-full" title="{{ item.url }}">Original: {{ item.url }}</p>
                        <p class="font-mono text-cyan-400 font-bold text-sm truncate w-full select-all">https://{{ host }}/go/{{ item.code }}</p>
                    </div>

                    <!-- Actions & Clicks -->
                    <div class="flex items-center gap-3 w-full md:w-auto justify-between border-t md:border-t-0 border-slate-800 pt-2 md:pt-0 shrink-0">
                        <span class="text-xs bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800 text-emerald-400 font-bold">
                            <i class="fa-solid fa-eye mr-1"></i> {{ item.clicks }}
                        </span>
                        
                        <!-- 1-CLICK COPY BUTTON -->
                        <button onclick="copyToClipboard('https://{{ host }}/go/{{ item.code }}', this)" 
                            class="px-4 py-2 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs rounded-lg transition duration-200 flex items-center gap-1">
                            <i class="fa-solid fa-copy"></i> <span>Copy</span>
                        </button>
                    </div>

                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-8 text-slate-500 text-xs">You have not created any short links yet. Shorten a link above!</div>
            {% endif %}
        </div>

    </div>

    <!-- 1-CLICK COPY SCRIPT -->
    <script>
        function copyToClipboard(text, btnElement) {
            navigator.clipboard.writeText(text).then(() => {
                const span = btnElement.querySelector('span');
                const originalText = span.innerText;
                span.innerText = "Copied! ✅";
                btnElement.classList.replace('bg-cyan-500', 'bg-emerald-400');
                
                setTimeout(() => {
                    span.innerText = originalText;
                    btnElement.classList.replace('bg-emerald-400', 'bg-cyan-500');
                }, 2000);
            }).catch(err => {
                alert("Failed to copy. Please copy manually.");
            });
        }
    </script>
</body>
</html>
"""

PHASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Protection Portal - Step {{ current_phase }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {{ settings.popunderCode | safe }}
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col justify-between items-center p-4 font-sans">
    
    <div>{{ settings.bannerTop | safe }}</div>

    <div class="max-w-xl w-full bg-slate-900 p-6 rounded-3xl border border-cyan-500/30 text-center space-y-4 shadow-2xl">
        <h2 class="text-cyan-400 font-bold text-lg"><i class="fa-solid fa-shield-halved mr-2"></i>Security Check (Step {{ current_phase }} of {{ total_phases }})</h2>
        
        <div class="text-left text-xs bg-slate-950 p-4 rounded-xl border border-slate-800 text-slate-400 space-y-2">
            <p class="font-bold text-slate-200">Cloudflare Edge Verification</p>
            <p>Scanning files for malware and verifying SSL connection. Please wait while your edge node is prepared...</p>
        </div>

        <div>{{ settings.nativeAd | safe }}</div>

        <div id="timer" class="text-4xl font-mono text-cyan-400 font-bold animate-pulse">{{ settings.timerSeconds }}</div>
        
        <button id="btn" disabled onclick="goNext()" class="w-full py-4 bg-slate-800 text-slate-500 font-bold rounded-2xl">Verifying Security...</button>
    </div>

    <div>{{ settings.bannerBottom | safe }}</div>

    <script>
        let time = {{ settings.timerSeconds }};
        let interval = setInterval(() => {
            time--;
            document.getElementById('timer').innerText = time;
            if(time <= 0){
                clearInterval(interval);
                let btn = document.getElementById('btn');
                btn.disabled = false;
                btn.innerText = "CONTINUE TO NEXT STEP 🚀";
                btn.className = "w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black rounded-2xl cursor-pointer";
            }
        }, 1000);

        function goNext() {
            {% if settings.directLinkUrl %} window.open('{{ settings.directLinkUrl }}', '_blank'); {% endif %}
            {% if current_phase < total_phases %}
                window.location.href = '/go/{{ code }}/phase/{{ current_phase + 1 }}';
            {% else %}
                window.location.href = '/final/{{ code }}';
            {% endif %}
        }
    </script>
</body>
</html>
"""


# ==========================================
# 🌐 FLASK WEB ROUTES
# ==========================================
@app.route('/')
def home():
    if 'user_id' not in session:
        session['user_id'] = f"usr_{uuid.uuid4().hex[:8]}"

    user_id = session['user_id']
    user = users_col.find_one({"username": user_id})
    if not user:
        users_col.insert_one({"username": user_id, "balance": 0.0})
        user = users_col.find_one({"username": user_id})
    
    # Fetch ONLY THIS USER'S LINKS
    links = list(urls_col.find({"owner": user_id}).sort('_id', -1))
    return render_template_string(USER_DASHBOARD, user=user, links=links, host=request.host)

@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user_id' not in session:
        session['user_id'] = f"usr_{uuid.uuid4().hex[:8]}"

    long_url = request.form.get('url')
    custom_alias = request.form.get('custom_alias')
    password = request.form.get('password')
    
    code = custom_alias.strip() if custom_alias and custom_alias.strip() else generate_code()
    
    urls_col.insert_one({
        "code": code,
        "url": long_url,
        "password": password,
        "owner": session['user_id'],
        "clicks": 0
    })
    return redirect('/')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user_id' not in session: return redirect('/')

    amount = float(request.form.get('amount', 0))
    method = request.form.get('method')
    account = request.form.get('account')
    
    user_id = session['user_id']
    user = users_col.find_one({"username": user_id})
    if user and user.get('balance', 0) >= amount and amount > 0:
        users_col.update_one({"username": user_id}, {"$inc": {"balance": -amount}})
        withdrawals_col.insert_one({
            "username": user_id,
            "amount": amount,
            "method": method,
            "account": account,
            "status": "Pending"
        })
    return redirect('/')

@app.route('/go/<code>')
def start_phase(code):
    return redirect(f'/go/{code}/phase/1')

@app.route('/go/<code>/phase/<int:phase_num>')
def handle_phase(code, phase_num):
    url_data = urls_col.find_one({"code": code})
    if not url_data: return "Link Expired", 404

    # Password Protection Check
    if url_data.get('password') and not request.args.get('pass_auth'):
        return f'''<form action="/go/{code}/phase/1" method="GET" style="background:#090d16;color:white;padding:50px;text-align:center;font-family:sans-serif;">
                    <h2>🔐 Password Protected Link</h2>
                    <input type="password" name="pass_auth" placeholder="Enter Password" style="padding:10px;border-radius:5px;border:none;">
                    <button type="submit" style="padding:10px 20px;background:#06b6d4;border:none;border-radius:5px;cursor:pointer;font-weight:bold;">Unlock</button>
                   </form>'''

    settings = get_settings()

    # Geo CPM Rule (US/UK gets 3 phases, others get 2)
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    total_phases = 3 if "1.1.1." in ip else 2 

    # Credit publisher earnings on Phase 1
    if phase_num == 1:
        owner = url_data.get('owner', 'demo_publisher')
        cpm_rate = settings['cpmRates'].get('DEFAULT', 2.0)
        earning_per_click = cpm_rate / 1000.0
        users_col.update_one({"username": owner}, {"$inc": {"balance": earning_per_click}})

    return render_template_string(PHASE_HTML, code=code, settings=settings, current_phase=phase_num, total_phases=total_phases)

@app.route('/final/<code>')
def final_redirect(code):
    url_data = urls_col.find_one({"code": code})
    if url_data:
        urls_col.update_one({"code": code}, {"$inc": {"clicks": 1}})
        return redirect(url_data['url'])
    return "Link Expired", 404

if __name__ == '__main__':
    app.run(debug=True)
