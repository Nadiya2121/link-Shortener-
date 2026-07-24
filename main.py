import random, string, datetime
from flask import Flask, request, redirect, render_template_string
from user_agents import parse
from config import urls_col, analytics_col, get_settings
from admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)

def generate_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# --- PRO USER DASHBOARD HTML ---
USER_DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CloudLink Pro - High Speed Link Shortener</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col font-sans">
    
    <!-- Navbar -->
    <nav class="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
        <div class="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-2">
                <div class="w-9 h-9 bg-gradient-to-tr from-cyan-500 to-fuchsia-500 rounded-xl flex items-center justify-center font-black text-slate-950 shadow-[0_0_15px_rgba(6,182,212,0.5)]">CL</div>
                <span class="text-xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-400">CloudLink Pro</span>
            </div>
            <div class="text-xs bg-slate-800/80 px-3 py-1.5 rounded-full border border-slate-700 text-slate-300">
                <i class="fa-solid fa-bolt text-yellow-400 mr-1"></i> Global CDN Active
            </div>
        </div>
    </nav>

    <!-- Main Body -->
    <main class="flex-grow max-w-4xl w-full mx-auto p-4 my-6 space-y-8">
        
        <!-- Shortener Box -->
        <div class="bg-slate-900 p-6 md:p-8 rounded-3xl border border-cyan-500/30 shadow-[0_0_40px_rgba(6,182,212,0.15)] text-center relative overflow-hidden">
            <div class="absolute -top-10 -right-10 w-32 h-32 bg-cyan-500/10 rounded-full blur-2xl"></div>
            
            <h1 class="text-2xl md:text-4xl font-extrabold mb-2">Shorten & Protect Your Links</h1>
            <p class="text-slate-400 text-xs md:text-sm mb-6">Encrypted cloud redirection with maximum monetization throughput.</p>

            <form action="/shorten" method="POST" class="flex flex-col sm:flex-row gap-3">
                <input type="url" name="url" placeholder="Paste your long URL here..." required 
                    class="flex-grow px-5 py-4 bg-slate-950 border border-slate-700 rounded-2xl focus:outline-none focus:border-cyan-400 text-white placeholder-slate-500 shadow-inner">
                <button type="submit" 
                    class="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 rounded-2xl font-bold text-slate-950 hover:scale-105 transition duration-200 shadow-[0_0_20px_rgba(6,182,212,0.4)]">
                    SHORTEN <i class="fa-solid fa-arrow-right ml-1"></i>
                </button>
            </form>
        </div>

        <!-- User Links Dashboard List -->
        <div class="bg-slate-900 p-6 rounded-3xl border border-slate-800 shadow-xl space-y-4">
            <div class="flex justify-between items-center border-b border-slate-800 pb-3">
                <h3 class="font-bold text-slate-200 flex items-center gap-2">
                    <i class="fa-solid fa-list-check text-cyan-400"></i> Recent Shortened Links
                </h3>
                <span class="text-xs text-slate-500">{{ links|length }} Items</span>
            </div>

            {% if links %}
            <div class="space-y-3">
                {% for item in links %}
                <div class="p-4 bg-slate-950/80 rounded-2xl border border-slate-800 flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                    <div class="space-y-1 overflow-hidden w-full">
                        <p class="text-xs text-slate-500 truncate">{{ item.url }}</p>
                        <p class="text-sm font-mono text-cyan-400 font-bold select-all">https://{{ host }}/go/{{ item.code }}</p>
                    </div>
                    <div class="flex items-center gap-3 w-full md:w-auto justify-between border-t md:border-t-0 border-slate-800 pt-2 md:pt-0">
                        <span class="text-xs bg-slate-800 text-slate-300 px-3 py-1 rounded-lg">
                            <i class="fa-solid fa-eye text-cyan-400 mr-1"></i> {{ item.clicks }} clicks
                        </span>
                        <button onclick="navigator.clipboard.writeText('https://{{ host }}/go/{{ item.code }}'); alert('Link Copied!');" 
                            class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-xs font-bold rounded-xl transition text-slate-200">
                            <i class="fa-solid fa-copy mr-1"></i> Copy
                        </button>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div class="text-center py-8 text-slate-500 text-sm">No links shortened yet. Paste a link above!</div>
            {% endif %}
        </div>

    </main>
</body>
</html>
"""

# --- ENTERPRISE PHASE REDIRECTION HTML ---
PHASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Secure Cloud Portal - Verification Step {{ current_phase }}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    {{ settings.popunderCode | safe }}
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col justify-between items-center p-3 md:p-6 font-sans">
    
    <!-- Top Header Banner Space -->
    <div class="w-full max-w-3xl text-center my-2 overflow-hidden">{{ settings.bannerTop | safe }}</div>

    <!-- Main Verification Box -->
    <div class="max-w-xl w-full bg-slate-900/90 p-6 md:p-8 rounded-3xl border border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.2)] backdrop-blur-md space-y-6">
        
        <!-- Security Header -->
        <div class="flex items-center justify-between border-b border-slate-800 pb-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-cyan-500/10 border border-cyan-500/30 rounded-xl flex items-center justify-center text-cyan-400">
                    <i class="fa-solid fa-shield-virus text-lg"></i>
                </div>
                <div>
                    <h2 class="font-bold text-sm md:text-base text-slate-100">Secure File Protection</h2>
                    <p class="text-xs text-slate-400">Cloud Mirror Verification Step {{ current_phase }} of {{ total_phases }}</p>
                </div>
            </div>
            <span class="text-xs px-2.5 py-1 bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-semibold rounded-full">
                SSL Secured
            </span>
        </div>

        <!-- Fake Tech Article / Content for User Retention -->
        <div class="text-xs text-slate-400 leading-relaxed bg-slate-950 p-4 rounded-xl border border-slate-800/80 space-y-2">
            <p class="font-bold text-slate-300"><i class="fa-solid fa-server mr-1 text-cyan-400"></i> Cloud File Status: Ready</p>
            <p>Your requested link is being decrypted through our high-speed edge network. Please complete the security countdown below to proceed to the destination server.</p>
        </div>

        <!-- Native Ad Space -->
        <div class="my-4 text-center overflow-hidden">{{ settings.nativeAd | safe }}</div>

        <!-- Timer & Progress Bar -->
        <div class="text-center space-y-3">
            <div id="timer" class="text-4xl md:text-5xl font-mono font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-400">
                {{ settings.timerSeconds }}
            </div>
            <div class="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
                <div id="progressBar" class="bg-gradient-to-r from-cyan-500 to-fuchsia-500 h-full w-0 transition-all duration-1000"></div>
            </div>
        </div>

        <!-- Action Button -->
        <button id="nextBtn" disabled onclick="goNext()" 
            class="w-full py-4 bg-slate-800 text-slate-500 font-bold text-sm md:text-base rounded-2xl cursor-not-allowed transition duration-300 shadow-inner">
            <i class="fa-solid fa-spinner fa-spin mr-2"></i> Verifying Security...
        </button>
    </div>

    <!-- Bottom Banner Space -->
    <div class="w-full max-w-3xl text-center my-2 overflow-hidden">{{ settings.bannerBottom | safe }}</div>

    <!-- Script for Dynamic Multi-Phase Logic -->
    <script>
        let totalTime = {{ settings.timerSeconds }};
        let timeLeft = totalTime;
        const timerElem = document.getElementById('timer');
        const nextBtn = document.getElementById('nextBtn');
        const progressBar = document.getElementById('progressBar');

        const countdown = setInterval(() => {
            timeLeft--;
            timerElem.innerText = timeLeft;
            let percentage = ((totalTime - timeLeft) / totalTime) * 100;
            progressBar.style.width = percentage + '%';

            if (timeLeft <= 0) {
                clearInterval(countdown);
                timerElem.innerText = "VERIFIED!";
                nextBtn.disabled = false;
                nextBtn.innerHTML = 'CONTINUE TO NEXT STEP <i class="fa-solid fa-arrow-right ml-2"></i>';
                nextBtn.className = "w-full py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-slate-950 font-black text-sm md:text-base rounded-2xl shadow-[0_0_25px_rgba(6,182,212,0.5)] cursor-pointer hover:scale-102 transition";
            }
        }, 1000);

        function goNext() {
            {% if settings.directLinkUrl %}
                window.open('{{ settings.directLinkUrl }}', '_blank');
            {% endif %}
            
            // Redirect based on current phase vs total phase
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

# --- ROUTES ---
@app.route('/')
def home():
    links = list(urls_col.find().sort('_id', -1).limit(10))
    return render_template_string(USER_DASHBOARD_HTML, links=links, host=request.host)

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('url')
    code = generate_code()
    urls_col.insert_one({"code": code, "url": long_url, "clicks": 0})
    return redirect('/')

@app.route('/go/<code>')
def phase_start(code):
    return redirect(f'/go/{code}/phase/1')

@app.route('/go/<code>/phase/<int:phase_num>')
def phase_step(code, phase_num):
    url_data = urls_col.find_one({"code": code})
    if not url_data: return "Link Expired/Not Found", 404

    settings = get_settings()
    total_phases = settings.get('phaseCount', 2)

    # Track analytics on Phase 1
    if phase_num == 1:
        ua = parse(request.headers.get('User-Agent', ''))
        device = "Mobile" if ua.is_mobile else "Desktop"
        analytics_col.insert_one({
            "shortCode": code,
            "device": device,
            "referrer": request.headers.get('Referrer', 'Direct'),
            "time": datetime.datetime.now().strftime("%I:%M %p - %d %b")
        })

    return render_template_string(
        PHASE_HTML, 
        code=code, 
        settings=settings, 
        current_phase=phase_num, 
        total_phases=total_phases
    )

@app.route('/final/<code>')
def final_redirect(code):
    url_data = urls_col.find_one({"code": code})
    if url_data:
        urls_col.update_one({"code": code}, {"$inc": {"clicks": 1}})
        return redirect(url_data['url'])
    return "Link Expired", 404

if __name__ == '__main__':
    app.run(debug=True)
