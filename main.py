import random, string, datetime
from flask import Flask, request, redirect, render_template_string
from user_agents import parse
from config import urls_col, analytics_col, get_settings
from admin import admin_bp

app = Flask(__name__)
app.register_blueprint(admin_bp)

def generate_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

# --- HTML TEMPLATES ---
INDEX_HTML = """
<!DOCTYPE html>
<html>
<head><title>Neon Shortener</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center">
    <div class="bg-slate-900 p-8 rounded-2xl border border-cyan-500/30 max-w-md w-full text-center">
        <h1 class="text-3xl font-bold text-cyan-400 mb-4">NEON LINK ⚡</h1>
        <form action="/shorten" method="POST" class="space-y-4">
            <input type="url" name="url" placeholder="Paste link here..." required class="w-full p-3 bg-slate-950 border border-slate-700 rounded-xl text-white">
            <button type="submit" class="w-full p-3 bg-cyan-500 text-slate-950 font-bold rounded-xl">SHORTEN</button>
        </form>
        {% if short_url %}
            <div class="mt-4 p-3 bg-slate-950 border border-cyan-500 text-cyan-400 font-mono rounded-xl">{{ short_url }}</div>
        {% endif %}
    </div>
</body>
</html>
"""

PHASE1_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Step 1</title>
    <script src="https://cdn.tailwindcss.com"></script>
    {{ settings.popunderCode | safe }}
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-between p-4">
    <div>{{ settings.bannerTop | safe }}</div>
    <div class="bg-slate-900 p-6 rounded-xl border border-fuchsia-500/30 text-center max-w-md w-full">
        <h2 class="text-fuchsia-400 font-bold">Phase 1: Verification</h2>
        <div>{{ settings.nativeAd | safe }}</div>
        <div id="timer" class="text-4xl font-mono text-cyan-400 my-4">{{ settings.timerSeconds }}</div>
        <button id="btn" disabled onclick="goNext()" class="w-full py-3 bg-slate-800 text-slate-500 rounded-xl font-bold">Please Wait...</button>
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
                btn.innerText = "CONTINUE TO PHASE 2 🚀";
                btn.className = "w-full py-3 bg-cyan-500 text-slate-950 font-bold rounded-xl";
            }
        }, 1000);
        function goNext() {
            {% if settings.directLinkUrl %} window.open('{{ settings.directLinkUrl }}', '_blank'); {% endif %}
            window.location.href = '/go/{{ code }}/phase2';
        }
    </script>
</body>
</html>
"""

PHASE2_HTML = """
<!DOCTYPE html>
<html>
<head><title>Step 2</title><script src="https://cdn.tailwindcss.com"></script></head>
<body class="bg-slate-950 text-white min-h-screen flex items-center justify-center">
    <div class="bg-slate-900 p-8 rounded-xl border border-cyan-500 text-center max-w-md w-full">
        <h2 class="text-cyan-400 text-xl font-bold mb-4">Final Step</h2>
        <div>{{ settings.nativeAd | safe }}</div>
        <a href="/final/{{ code }}" class="block w-full py-3 bg-green-500 text-slate-950 font-bold rounded-xl mt-4">GET LINK 🔓</a>
    </div>
</body>
</html>
"""

# --- ROUTES ---
@app.route('/')
def home():
    return render_template_string(INDEX_HTML)

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('url')
    code = generate_code()
    urls_col.insert_one({"code": code, "url": long_url, "clicks": 0})
    short_url = f"https://{request.host}/go/{code}"
    return render_template_string(INDEX_HTML, short_url=short_url)

@app.route('/go/<code>')
def phase1(code):
    url_data = urls_col.find_one({"code": code})
    if not url_data: return "Link Not Found", 404
    
    # Analytics
    ua = parse(request.headers.get('User-Agent', ''))
    device = "Mobile" if ua.is_mobile else "Desktop"
    analytics_col.insert_one({"shortCode": code, "device": device, "time": datetime.datetime.now().strftime("%I:%M %p")})

    return render_template_string(PHASE1_HTML, code=code, settings=get_settings())

@app.route('/go/<code>/phase2')
def phase2(code):
    return render_template_string(PHASE2_HTML, code=code, settings=get_settings())

@app.route('/final/<code>')
def final_redirect(code):
    url_data = urls_col.find_one({"code": code})
    if url_data:
        urls_col.update_one({"code": code}, {"$inc": {"clicks": 1}})
        return redirect(url_data['url'])
    return "Expired", 404

if __name__ == '__main__':
    app.run(debug=True)
