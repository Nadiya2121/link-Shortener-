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
# 🤖 TELEGRAM BOT ENGINE (AUTOMATED THREAD)
# ==========================================
def start_telegram_bot():
    if TELEGRAM_BOT_TOKEN and TELEGRAM_BOT_TOKEN != "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        try:
            bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

            try:
                bot.remove_webhook(drop_pending_updates=True)
            except Exception:
                pass

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
            bot.infinity_polling(none_stop=True, skip_pending=True)
        except Exception as e:
            print(f"❌ Telegram Bot Thread Handled: {e}")

threading.Thread(target=start_telegram_bot, daemon=True).start()


# ==========================================
# 🌐 AUTH & DASHBOARD HTML TEMPLATES
# ==========================================
LOGIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publisher Login - CloudLink Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4 font-sans">
    <div class="bg-slate-900 p-8 rounded-3xl border border-cyan-500/30 max-w-md w-full space-y-6 shadow-2xl">
        <div class="text-center space-y-2">
            <h2 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-400">CloudLink Pro</h2>
            <p class="text-xs text-slate-400">Publisher Login Portal</p>
        </div>
        
        {% if error %}
        <div class="bg-rose-500/10 border border-rose-500/30 p-3 rounded-xl text-xs text-rose-400 text-center font-bold">
            {{ error }}
        </div>
        {% endif %}

        <form action="/login" method="POST" class="space-y-4">
            <div>
                <label class="text-xs font-bold text-slate-400 block mb-1">Username</label>
                <input type="text" name="username" placeholder="Enter Username" required class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400">
            </div>
            <div>
                <label class="text-xs font-bold text-slate-400 block mb-1">Password</label>
                <input type="password" name="password" placeholder="Enter Password" required class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400">
            </div>
            <button type="submit" class="w-full py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black rounded-xl hover:scale-101 transition shadow-[0_0_15px_rgba(6,182,212,0.4)]">
                LOGIN TO DASHBOARD 🚀
            </button>
        </form>

        <div class="pt-2 border-t border-slate-800/80 text-center space-y-2">
            <p class="text-xs text-slate-500">Don't have an account? <a href="/register" class="text-cyan-400 font-bold hover:underline">Register Here</a></p>
            <p class="text-xs text-slate-500">Forgot Password? <a href="{{ settings.supportUrl if settings and settings.supportUrl else 'https://t.me/MovieLinkbd' }}" target="_blank" class="text-fuchsia-400 font-bold hover:underline"><i class="fa-brands fa-telegram mr-1"></i>Contact Admin Support</a></p>
        </div>
    </div>
</body>
</html>
"""

REGISTER_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Publisher Registration - CloudLink Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center p-4 font-sans">
    <div class="bg-slate-900 p-8 rounded-3xl border border-cyan-500/30 max-w-md w-full space-y-6 shadow-2xl">
        <div class="text-center space-y-2">
            <h2 class="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-400">CloudLink Pro</h2>
            <p class="text-xs text-slate-400">Create Publisher Account</p>
        </div>
        
        {% if error %}
        <div class="bg-rose-500/10 border border-rose-500/30 p-3 rounded-xl text-xs text-rose-400 text-center font-bold">
            {{ error }}
        </div>
        {% endif %}

        <form action="/register" method="POST" class="space-y-4">
            <div>
                <label class="text-xs font-bold text-slate-400 block mb-1">Username</label>
                <input type="text" name="username" placeholder="Choose Username" required class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400">
            </div>
            <div>
                <label class="text-xs font-bold text-slate-400 block mb-1">Email Address</label>
                <input type="email" name="email" placeholder="Enter Email" required class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400">
            </div>
            <div>
                <label class="text-xs font-bold text-slate-400 block mb-1">Password</label>
                <input type="password" name="password" placeholder="Choose Password" required class="w-full p-3.5 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-cyan-400">
            </div>
            <button type="submit" class="w-full py-3.5 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black rounded-xl hover:scale-101 transition shadow-[0_0_15px_rgba(6,182,212,0.4)]">
                CREATE ACCOUNT ✨
            </button>
        </form>

        <p class="text-xs text-center text-slate-500">Already have an account? <a href="/login" class="text-cyan-400 font-bold hover:underline">Login Here</a></p>
    </div>
</body>
</html>
"""

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
                    <i class="fa-solid fa-user-circle"></i> {{ user.username }}
                </h1>
                <p class="text-xs text-slate-400">Publisher Rate: <span class="text-emerald-400 font-bold">${{ settings.cpmRate }} / 1,000 Views</span></p>
            </div>
            <div class="flex items-center gap-4 w-full md:w-auto justify-between md:justify-end">
                <div class="bg-slate-950 px-5 py-3 rounded-xl border border-slate-800 text-right">
                    <span class="text-xs text-slate-500 block">AVAILABLE BALANCE</span>
                    <span class="text-2xl font-black text-emerald-400">${{ "%.3f"|format(user.balance) }}</span>
                </div>
                <a href="/logout" class="bg-rose-500/10 text-rose-400 p-3.5 rounded-xl hover:bg-rose-500/20 transition" title="Logout">
                    <i class="fa-solid fa-right-from-bracket text-lg"></i>
                </a>
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

        <!-- Withdrawal Section (bKash / Nagad / Rocket) -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 class="text-lg font-bold text-emerald-400 flex items-center gap-2">
                <i class="fa-solid fa-wallet"></i> Withdraw Earnings (Min Limit: ${{ settings.minWithdraw }})
            </h2>
            
            <form action="/withdraw" method="POST" class="flex flex-col md:flex-row gap-3">
                <input type="number" step="0.1" name="amount" placeholder="Amount ($)" required class="p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white">
                <select name="method" class="p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-cyan-400 font-bold">
                    <option value="bKash">bKash (Personal)</option>
                    <option value="Nagad">Nagad (Personal)</option>
                    <option value="Rocket">Rocket (Personal)</option>
                </select>
                <input type="text" name="account" placeholder="Enter Mobile Number (017...)" required class="flex-grow p-3 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white">
                <button type="submit" class="px-6 py-3 bg-emerald-500 text-slate-950 font-bold text-xs rounded-xl hover:bg-emerald-400 transition">WITHDRAW</button>
            </form>

            <!-- User Withdrawal History -->
            <div class="pt-4 border-t border-slate-800 space-y-2">
                <h3 class="text-xs font-bold text-slate-400 mb-2">Withdrawal History</h3>
                {% for w in user_withdrawals %}
                <div class="p-3 bg-slate-950 rounded-xl flex justify-between items-center text-xs border border-slate-800/80">
                    <div>
                        <span class="font-bold text-white">${{ w.amount }}</span> via <span class="text-cyan-400 font-bold">{{ w.method }}</span> ({{ w.account }})
                    </div>
                    <span class="px-2.5 py-1 rounded font-bold {% if w.status=='Approved' %}bg-emerald-500/10 text-emerald-400 border border-emerald-500/30{% elif w.status=='Rejected' %}bg-rose-500/10 text-rose-400 border border-rose-500/30{% else %}bg-yellow-500/10 text-yellow-400 border border-yellow-500/30{% endif %}">
                        {{ w.status }}
                    </span>
                </div>
                {% else %}
                <p class="text-xs text-slate-600">No withdrawal requests submitted yet.</p>
                {% endfor %}
            </div>
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
                    
                    <div class="space-y-1 min-w-0 w-full md:w-3/4">
                        <p class="text-xs text-slate-500 truncate w-full" title="{{ item.url }}">Original: {{ item.url }}</p>
                        <p class="font-mono text-cyan-400 font-bold text-sm truncate w-full select-all">https://{{ host }}/go/{{ item.code }}</p>
                    </div>

                    <div class="flex items-center gap-3 w-full md:w-auto justify-between border-t md:border-t-0 border-slate-800 pt-2 md:pt-0 shrink-0">
                        <span class="text-xs bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800 text-emerald-400 font-bold">
                            <i class="fa-solid fa-eye mr-1"></i> {{ item.clicks }}
                        </span>
                        
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
# 🌐 FLASK WEB ROUTES & AUTH
# ==========================================
@app.route('/')
def home():
    if 'user' not in session:
        return redirect('/login')

    user = users_col.find_one({"username": session['user']})
    if not user or user.get('is_blocked'):
        session.pop('user', None)
        return redirect('/login')

    links = list(urls_col.find({"owner": session['user']}).sort('_id', -1))
    user_withdrawals = list(withdrawals_col.find({"username": session['user']}).sort('_id', -1))
    settings = get_settings()

    return render_template_string(USER_DASHBOARD, user=user, links=links, user_withdrawals=user_withdrawals, settings=settings, host=request.host)

@app.route('/login', methods=['GET', 'POST'])
def login():
    settings = get_settings()
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = users_col.find_one({"username": username, "password": password})
        if user:
            if user.get('is_blocked'):
                return render_template_string(LOGIN_HTML, error="Your account has been blocked by Admin!", settings=settings)
            session['user'] = username
            return redirect('/')
        return render_template_string(LOGIN_HTML, error="Invalid Username or Password!", settings=settings)
    return render_template_string(LOGIN_HTML, settings=settings)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        if users_col.find_one({"username": username}):
            return render_template_string(REGISTER_HTML, error="Username already exists!")

        users_col.insert_one({"username": username, "email": email, "password": password, "balance": 0.0, "is_blocked": False})
        session['user'] = username
        return redirect('/')
    return render_template_string(REGISTER_HTML)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/shorten', methods=['POST'])
def shorten():
    if 'user' not in session: return redirect('/login')

    long_url = request.form.get('url')
    custom_alias = request.form.get('custom_alias')
    password = request.form.get('password')

    code = custom_alias.strip() if custom_alias and custom_alias.strip() else generate_code()
    urls_col.insert_one({"code": code, "url": long_url, "password": password, "owner": session['user'], "clicks": 0})
    return redirect('/')

@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'user' not in session: return redirect('/login')

    amount = float(request.form.get('amount', 0))
    method = request.form.get('method')
    account = request.form.get('account')
    settings = get_settings()

    user = users_col.find_one({"username": session['user']})
    if amount < settings.get('minWithdraw', 2.0):
        return redirect('/')

    if user and user.get('balance', 0) >= amount and amount > 0:
        users_col.update_one({"username": session['user']}, {"$inc": {"balance": -amount}})
        withdrawals_col.insert_one({
            "username": session['user'],
            "amount": amount,
            "method": method,
            "account": account,
            "status": "Pending",
            "timestamp": datetime.datetime.now()
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
    total_phases = settings.get('phaseCount', 2)

    # Dynamic CPM Earnings ($1 CPM = $0.001 per view)
    if phase_num == 1:
        owner = url_data.get('owner')
        if owner:
            cpm_rate = settings.get('cpmRate', 1.0)
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
