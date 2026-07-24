from flask import Blueprint, request, render_template_string, redirect
from bson.objectid import ObjectId
from config import settings_col, analytics_col, urls_col, withdrawals_col, users_col, get_settings

admin_bp = Blueprint('admin', __name__)

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Admin Panel - CloudLink Pro</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen font-sans p-4 md:p-8">
    
    <div class="max-w-7xl mx-auto space-y-8">
        
        <!-- Header Bar -->
        <div class="flex flex-col md:flex-row justify-between items-center bg-slate-900/90 p-6 rounded-2xl border border-cyan-500/40 shadow-[0_0_30px_rgba(6,182,212,0.2)] gap-4">
            <div>
                <h1 class="text-2xl md:text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-fuchsia-500">
                    <i class="fa-solid fa-crown mr-2"></i>MASTER SYSTEM CONTROL
                </h1>
                <p class="text-xs text-slate-400">Complete Control over Users, Ads, Timers, Phases & Withdrawals</p>
            </div>
            <div class="flex items-center gap-4">
                <div class="bg-slate-950 px-4 py-2 border border-slate-800 rounded-xl text-center">
                    <span class="text-xs text-slate-500 block">TOTAL CLICKS</span>
                    <span class="text-xl font-bold text-cyan-400">{{ total_clicks }}</span>
                </div>
                <a href="/" class="bg-slate-800 hover:bg-slate-700 px-4 py-3 rounded-xl text-xs font-bold text-slate-300">
                    <i class="fa-solid fa-globe mr-1"></i> User Site
                </a>
            </div>
        </div>

        <!-- 👥 REGISTERED USERS MANAGEMENT & PASSWORD RESET -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
            <h2 class="text-lg font-bold text-cyan-400 flex items-center gap-2">
                <i class="fa-solid fa-users-gear"></i> Registered Users & Password Reset
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-400">
                    <thead class="bg-slate-950 text-slate-200 border-b border-slate-800">
                        <tr>
                            <th class="p-3">Username</th>
                            <th class="p-3">Email</th>
                            <th class="p-3">Balance</th>
                            <th class="p-3">Status</th>
                            <th class="p-3">Reset Password</th>
                            <th class="p-3">Account Control</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {% for u in users %}
                        <tr class="hover:bg-slate-950/50">
                            <td class="p-3 text-white font-bold">{{ u.username }}</td>
                            <td class="p-3 text-slate-400">{{ u.email }}</td>
                            <td class="p-3 text-emerald-400 font-bold">${{ "%.2f"|format(u.balance) }}</td>
                            <td class="p-3">
                                <span class="px-2 py-1 rounded font-bold {% if u.is_blocked %}bg-rose-500/10 text-rose-400 border border-rose-500/30{% else %}bg-emerald-500/10 text-emerald-400 border border-emerald-500/30{% endif %}">
                                    {% if u.is_blocked %}BLOCKED{% else %}ACTIVE{% endif %}
                                </span>
                            </td>
                            <td class="p-3">
                                <form action="/admin/reset_user_password" method="POST" class="flex gap-1">
                                    <input type="hidden" name="username" value="{{ u.username }}">
                                    <input type="text" name="new_password" placeholder="New Password" required class="p-1.5 bg-slate-950 border border-slate-800 rounded text-cyan-300 w-28 text-xs focus:outline-none">
                                    <button type="submit" class="px-3 py-1.5 bg-cyan-500 text-slate-950 font-bold rounded hover:bg-cyan-400 transition">Reset</button>
                                </form>
                            </td>
                            <td class="p-3">
                                <a href="/admin/toggle_block_user/{{ u.username }}" class="px-3 py-1.5 {% if u.is_blocked %}bg-emerald-500 text-slate-950{% else %}bg-rose-500 text-white{% endif %} font-bold rounded transition">
                                    {% if u.is_blocked %}Unblock{% else %}Block User{% endif %}
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Master Settings Form -->
        <form action="/admin/save" method="POST" class="space-y-6">
            
            <!-- ⚙️ SYSTEM & PHASE SETTINGS -->
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
                <h2 class="text-lg font-bold text-fuchsia-400 flex items-center gap-2">
                    <i class="fa-solid fa-sliders"></i> System & Redirection Step Controls
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Redirection Phase Count (Steps)</label>
                        <select name="phaseCount" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-400 font-bold focus:outline-none focus:border-cyan-500">
                            <option value="1" {% if settings.phaseCount == 1 %}selected{% endif %}>1 Phase (Fast Redirect)</option>
                            <option value="2" {% if settings.phaseCount == 2 %}selected{% endif %}>2 Phase (Standard High Revenue)</option>
                            <option value="3" {% if settings.phaseCount == 3 %}selected{% endif %}>3 Phase (Maximum Revenue)</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Timer Duration (In Seconds)</label>
                        <input type="number" name="timerSeconds" value="{{ settings.timerSeconds }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-400 font-bold focus:outline-none focus:border-cyan-500">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Global CPM Rate ($ per 1000 views)</label>
                        <input type="number" step="0.1" name="cpmRate" value="{{ settings.cpmRate }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-emerald-400 font-bold focus:outline-none focus:border-emerald-500">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Minimum Withdrawal ($ Limit)</label>
                        <input type="number" step="0.1" name="minWithdraw" value="{{ settings.minWithdraw }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-400 font-bold focus:outline-none focus:border-cyan-500">
                    </div>
                </div>
            </div>

            <!-- 🌐 DOMAIN ROTATOR & TELEGRAM SUPPORT SETTINGS -->
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
                <h2 class="text-lg font-bold text-cyan-400 flex items-center gap-2">
                    <i class="fa-solid fa-network-wired"></i> Domain & Contact Support Config
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Primary Domain Name</label>
                        <input type="text" name="primaryDomain" value="{{ settings.primaryDomain }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-300 font-mono text-xs">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Backup Domain Rotator URL</label>
                        <input type="text" name="backupDomain" value="{{ settings.backupDomain }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-cyan-300 font-mono text-xs">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1 text-fuchsia-400"><i class="fa-brands fa-telegram mr-1"></i> Telegram Support URL (Forgot Pass)</label>
                        <input type="text" name="supportUrl" value="{{ settings.supportUrl if settings.supportUrl else 'https://t.me/ProBotDeveloperBot' }}" placeholder="https://t.me/MovieLinkbd" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-fuchsia-300 font-mono text-xs focus:outline-none focus:border-fuchsia-400">
                    </div>
                </div>
            </div>

            <!-- 🎛️ ADSTERRA & ADS CONTROLS -->
            <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
                <h2 class="text-lg font-bold text-yellow-400 flex items-center gap-2">
                    <i class="fa-solid fa-rectangle-ad"></i> AdSterra Advertisement Placements
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Popunder Script Code</label>
                        <textarea name="popunderCode" rows="3" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300 focus:outline-none">{{ settings.popunderCode }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Direct Link URL (Triggers on button click)</label>
                        <input type="text" name="directLinkUrl" value="{{ settings.directLinkUrl }}" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300">
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Header/Top Banner Code</label>
                        <textarea name="bannerTop" rows="3" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300 focus:outline-none">{{ settings.bannerTop }}</textarea>
                    </div>
                    <div>
                        <label class="text-xs text-slate-400 font-bold block mb-1">Footer/Bottom Banner Code</label>
                        <textarea name="bannerBottom" rows="3" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300 focus:outline-none">{{ settings.bannerBottom }}</textarea>
                    </div>
                    <div class="md:col-span-2">
                        <label class="text-xs text-slate-400 font-bold block mb-1">Native Banner Ad Code</label>
                        <textarea name="nativeAd" rows="3" class="w-full bg-slate-950 border border-slate-800 p-3 rounded-xl text-xs font-mono text-cyan-300 focus:outline-none">{{ settings.nativeAd }}</textarea>
                    </div>
                </div>

                <button type="submit" class="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 font-black text-slate-950 rounded-xl shadow-[0_0_20px_rgba(6,182,212,0.5)] hover:scale-102 transition">
                    SAVE ALL MASTER SETTINGS 💾
                </button>
            </div>
        </form>

        <!-- 💸 PENDING WITHDRAWALS SECTION -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
            <h2 class="text-lg font-bold text-emerald-400 flex items-center gap-2">
                <i class="fa-solid fa-money-bill-transfer"></i> Pending User Withdrawals
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-400">
                    <thead class="bg-slate-950 text-slate-200 border-b border-slate-800">
                        <tr>
                            <th class="p-3">User</th>
                            <th class="p-3">Amount</th>
                            <th class="p-3">Method</th>
                            <th class="p-3">Account Info</th>
                            <th class="p-3">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-slate-800">
                        {% for w in withdrawals %}
                        <tr class="hover:bg-slate-950/50">
                            <td class="p-3 text-white font-bold">{{ w.username }}</td>
                            <td class="p-3 text-emerald-400 font-bold">${{ w.amount }}</td>
                            <td class="p-3"><span class="px-2 py-1 bg-slate-800 text-cyan-300 rounded font-bold">{{ w.method }}</span></td>
                            <td class="p-3 font-mono text-cyan-300 font-bold">{{ w.account }}</td>
                            <td class="p-3 space-x-2">
                                <a href="/admin/approve_withdrawal/{{ w._id }}" class="px-3 py-1.5 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg transition">Approve & Paid</a>
                                <a href="/admin/reject_withdrawal/{{ w._id }}" class="px-3 py-1.5 bg-rose-500 hover:bg-rose-400 text-white font-bold rounded-lg transition">Reject & Refund</a>
                            </td>
                        </tr>
                        {% else %}
                        <tr><td colspan="5" class="p-4 text-center text-slate-500">No pending withdrawal requests.</td></tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- 📊 TRAFFIC ANALYTICS TABLE -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
            <h2 class="text-lg font-bold text-cyan-400 flex items-center gap-2">
                <i class="fa-solid fa-chart-line"></i> Real-Time Traffic Analytics
            </h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs text-slate-400">
                    <thead class="bg-slate-950 text-slate-200 border-b border-slate-800">
                        <tr>
                            <th class="p-3">Short Code</th>
                            <th class="p-3">Device</th>
                            <th class="p-3">Referrer</th>
                            <th class="p-3">Time</th>
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
    withdrawals = list(withdrawals_col.find({"status": "Pending"}))
    analytics = list(analytics_col.find().sort('_id', -1).limit(30))
    users = list(users_col.find().sort('_id', -1))
    
    total_clicks = 0
    for u in urls_col.find():
        total_clicks += u.get('clicks', 0)
        
    return render_template_string(
        ADMIN_HTML, 
        settings=settings, 
        withdrawals=withdrawals, 
        analytics=analytics, 
        users=users,
        total_clicks=total_clicks
    )

@admin_bp.route('/admin/reset_user_password', methods=['POST'])
def reset_user_password():
    username = request.form.get('username')
    new_password = request.form.get('new_password')
    if username and new_password:
        users_col.update_one({"username": username}, {"$set": {"password": new_password}})
    return redirect('/admin')

@admin_bp.route('/admin/toggle_block_user/<username>')
def toggle_block_user(username):
    u = users_col.find_one({"username": username})
    if u:
        new_status = not u.get('is_blocked', False)
        users_col.update_one({"username": username}, {"$set": {"is_blocked": new_status}})
    return redirect('/admin')

@admin_bp.route('/admin/approve_withdrawal/<id>')
def approve_withdrawal(id):
    withdrawals_col.update_one({"_id": ObjectId(id)}, {"$set": {"status": "Approved"}})
    return redirect('/admin')

@admin_bp.route('/admin/reject_withdrawal/<id>')
def reject_withdrawal(id):
    w = withdrawals_col.find_one({"_id": ObjectId(id)})
    if w:
        users_col.update_one({"username": w['username']}, {"$inc": {"balance": w['amount']}})
        withdrawals_col.update_one({"_id": ObjectId(id)}, {"$set": {"status": "Rejected"}})
    return redirect('/admin')

@admin_bp.route('/admin/save', methods=['POST'])
def save_settings():
    cpm = float(request.form.get('cpmRate', 1.0))
    min_w = float(request.form.get('minWithdraw', 2.0))
    
    settings_col.update_one(
        {"_id": "global_settings"},
        {"$set": {
            "phaseCount": int(request.form.get('phaseCount', 2)),
            "timerSeconds": int(request.form.get('timerSeconds', 8)),
            "primaryDomain": request.form.get('primaryDomain'),
            "backupDomain": request.form.get('backupDomain'),
            "supportUrl": request.form.get('supportUrl', 'https://t.me/MovieLinkbd'), # সাপোর্ট টেলিগ্রাম লিংক
            "popunderCode": request.form.get('popunderCode'),
            "directLinkUrl": request.form.get('directLinkUrl'),
            "bannerTop": request.form.get('bannerTop'),
            "bannerBottom": request.form.get('bannerBottom'),
            "nativeAd": request.form.get('nativeAd'),
            "cpmRate": cpm,
            "minWithdraw": min_w,
            "cpmRates.DEFAULT": cpm
        }}
    )
    return redirect('/admin')
