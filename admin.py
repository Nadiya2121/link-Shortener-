from flask import Blueprint, request, render_template_string, redirect
from config import settings_col, analytics_col, urls_col, get_settings

admin_bp = Blueprint('admin', __name__)

ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Neon Admin Panel</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-slate-950 text-slate-200 p-6">
    <div class="max-w-5xl mx-auto space-y-6">
        <h1 class="text-3xl font-bold text-cyan-400">MASTER ADMIN PANEL ⚡</h1>
        
        <!-- AdSterra Settings -->
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 class="text-xl font-bold text-fuchsia-400 mb-4">AdSterra & Link Control</h2>
            <form action="/admin/save" method="POST" class="space-y-4">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs text-slate-400">Popunder Code</label>
                        <textarea name="popunderCode" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">{{ settings.popunderCode }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400">Direct Link URL</label>
                        <input type="text" name="directLinkUrl" value="{{ settings.directLinkUrl }}" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400">Banner Top</label>
                        <textarea name="bannerTop" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">{{ settings.bannerTop }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400">Banner Bottom</label>
                        <textarea name="bannerBottom" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">{{ settings.bannerBottom }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400">Native Ad Code</label>
                        <textarea name="nativeAd" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">{{ settings.nativeAd }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400">Timer (Seconds)</label>
                        <input type="number" name="timerSeconds" value="{{ settings.timerSeconds }}" class="w-full bg-slate-950 p-2 text-xs border border-slate-800 text-cyan-300 font-mono">
                    </div>
                </div>
                <button type="submit" class="bg-cyan-500 text-slate-950 px-6 py-2 font-bold rounded">SAVE SETTINGS 💾</button>
            </form>
        </div>

        <!-- Traffic Analytics -->
        <div class="bg-slate-900 p-6 rounded-xl border border-slate-800">
            <h2 class="text-xl font-bold text-cyan-400 mb-4">Live Traffic Reports</h2>
            <table class="w-full text-xs text-left text-slate-400">
                <thead class="bg-slate-950 text-slate-200">
                    <tr><th class="p-2">Code</th><th class="p-2">Device</th><th class="p-2">Time</th></tr>
                </thead>
                <tbody>
                    {% for item in analytics %}
                    <tr class="border-b border-slate-800">
                        <td class="p-2 text-cyan-400">{{ item.shortCode }}</td>
                        <td class="p-2">{{ item.device }}</td>
                        <td class="p-2">{{ item.time }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

@admin_bp.route('/admin')
def admin_page():
    settings = get_settings()
    analytics = list(analytics_col.find().sort('_id', -1).limit(20))
    return render_template_string(ADMIN_HTML, settings=settings, analytics=analytics)

@admin_bp.route('/admin/save', methods=['POST'])
def save_settings():
    settings_col.update_one(
        {"_id": "global_settings"},
        {"$set": {
            "popunderCode": request.form.get('popunderCode'),
            "directLinkUrl": request.form.get('directLinkUrl'),
            "bannerTop": request.form.get('bannerTop'),
            "bannerBottom": request.form.get('bannerBottom'),
            "nativeAd": request.form.get('nativeAd'),
            "timerSeconds": int(request.form.get('timerSeconds', 10))
        }}
    )
    return redirect('/admin')
