from flask import Blueprint, request, render_template_string, redirect
from config import settings_col, analytics_col, urls_col, get_settings

admin_bp = Blueprint('admin', __name__)

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Enterprise Admin Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans">
    
    <div class="max-w-7xl mx-auto p-4 md:p-8 space-y-6">
        
        <!-- Top Nav -->
        <div class="flex flex-col md:flex-row justify-between items-center bg-slate-900/80 p-6 rounded-2xl border border-cyan-500/30 backdrop-blur-md gap-4">
            <div>
                <h1 class="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-500">
                    <i class="fa-solid fa-shield-halved mr-2"></i>MASTER CONTROL PANEL
                </h1>
                <p class="text-xs text-slate-400">Manage AdSterra Ads, Phases & Global Traffic Analytics</p>
            </div>
            <div class="flex gap-4">
                <div class="bg-slate-950 px-4 py-2 border border-slate-800 rounded-xl text-center">
                    <span class="text-xs text-slate-500 block">TOTAL CLICKS</span>
                    <span class="text-xl font-bold text-cyan-400">{{ total_clicks }}</span>
                </div>
            </div>
        </div>

        <!-- System Controls & Ad Manager -->
        <form action="/admin/save" method="POST" class="space-y-6">
            
            <!-- Phase Settings -->
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
                <h2 class="text-lg font-bold text-fuchsia-400 mb-4"><i class="fa-solid fa-layer-group mr-2"></i>Multi-Phase Settings</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Redirection Phase Count (1, 2, or 3)</label>
                        <select name="phaseCount" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-400 font-bold focus:outline-none focus:border-cyan-500">
                            <option value="1" {% if settings.phaseCount == 1 %}selected{% endif %}>1 Phase (Fast Redirect)</option>
                            <option value="2" {% if settings.phaseCount == 2 %}selected{% endif %}>2 Phase (Standard - High Revenue)</option>
                            <option value="3" {% if settings.phaseCount == 3 %}selected{% endif %}>3 Phase (Maximum Revenue)</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Timer Countdown (Seconds)</label>
                        <input type="number" name="timerSeconds" value="{{ settings.timerSeconds }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-400 font-bold focus:outline-none focus:border-cyan-500">
                    </div>
                </div>
            </div>

            <!-- Ad Codes -->
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
                <h2 class="text-lg font-bold text-cyan-400 mb-4"><i class="fa-solid fa-rectangle-ad mr-2"></i>AdSterra Placement Manager</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs text-slate-400 block mb-1">Popunder Script</label>
                        <textarea name="popunderCode" rows="3" class="w-full bg-slate-950 border border-slate-800 p-2 rounded-xl text-xs font-mono text-cyan-300"><%= settings.popunderCode %></textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 block mb-1">Direct Link URL</label>
                        <input type="text" name="directLinkUrl" value="{{ settings.directLinkUrl }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 block mb-1">Header Banner (728x90 / 300x250)</label>
                        <textarea name="bannerTop" rows="3" class="w-full bg-slate-950 border border-slate-800 p-2 rounded-xl text-xs font-mono text-cyan-300">{{ settings.bannerTop }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 block mb-1">Footer Banner</label>
                        <textarea name="bannerBottom" rows="3" class="w-full bg-slate-950 border border-slate-800 p-2 rounded-xl text-xs font-mono text-cyan-300">{{ settings.bannerBottom }}</textarea>
                    </div>
                    <div class="md:col-span-2">
                        <label class="text-xs text-slate-400 block mb-1">Native Ad Code</label>
                        <textarea name="nativeAd" rows="3" class="w-full bg-slate-950 border border-slate-800 p-2 rounded-xl text-xs font-mono text-cyan-300">{{ settings.nativeAd }}</textarea>
                    </div>
                </div>
                <button type="submit" class="mt-4 px-8 py-3 bg-gradient-to-r from-cyan-500 to-blue-600 font-bold text-slate-950 rounded-xl shadow-[0_0_20px_rgba(6,182,212,0.4)] hover:scale-105 transition">
                    SAVE CHANGES 💾
                </button>
            </div>
        </form>

        <!-- Live Analytics -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl">
            <h2 class="text-lg font-bold text-emerald-400 mb-4"><i class="fa-solid fa-chart-line mr-2"></i>Real-time Traffic Analytics</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-400">
                    <thead class="bg-slate-950 text-slate-200 border-b border-slate-800">
                        <tr>
                            <th class="p-3">SHORT CODE</th>
                            <th class="p-3">DEVICE</th>
                            <th class="p-3">REFERRER</th>
                            <th class="p-3">TIME</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {% for item in analytics %}
                        <tr class="hover:bg-slate-950/50">
                            <td class="p-3 font-mono text-cyan-400 font-bold">{{ item.shortCode }}</td>
                            <td class="p-3"><span class="px-2 py-1 bg-slate-800 rounded-md">{{ item.device }}</span></td>
                            <td class="p-3 text-slate-500">{{ item.referrer }}</td>
                            <td class="p-3">{{ item.time }}</td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

    </div>
</body>
</html>
"""

@admin_bp.route('/admin')
def admin_page():
    settings = get_settings()
    analytics = list(analytics_col.find().sort('_id', -1).limit(30))
    
    # Calculate Total Clicks
    total_clicks = 0
    for u in urls_col.find():
        total_clicks += u.get('clicks', 0)
        
    return render_template_string(ADMIN_HTML, settings=settings, analytics=analytics, total_clicks=total_clicks)

@admin_bp.route('/admin/save', methods=['POST'])
def save_settings():
    settings_col.update_one(
        {"_id": "global_settings"},
        {"$set": {
            "phaseCount": int(request.form.get('phaseCount', 2)),
            "popunderCode": request.form.get('popunderCode'),
            "directLinkUrl": request.form.get('directLinkUrl'),
            "bannerTop": request.form.get('bannerTop'),
            "bannerBottom": request.form.get('bannerBottom'),
            "nativeAd": request.form.get('nativeAd'),
            "timerSeconds": int(request.form.get('timerSeconds', 8))
        }}
    )
    return redirect('/admin')
