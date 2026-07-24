from flask import Blueprint, request, render_template_string, redirect, session
from config import settings_col, analytics_col, urls_col, withdrawals_col, users_col, get_settings

admin_bp = Blueprint('admin', __name__)

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"><title>Master Admin - SaaS Control</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 p-6">
    <div class="max-w-7xl mx-auto space-y-6">
        <div class="flex justify-between items-center bg-slate-900 p-6 rounded-2xl border border-cyan-500/30">
            <h1 class="text-2xl font-bold text-cyan-400"><i class="fa-solid fa-crown mr-2"></i>SAAS MASTER PANEL</h1>
            <a href="/" class="bg-slate-800 px-4 py-2 rounded-xl text-xs font-bold text-slate-300">User Dashboard</a>
        </div>

        <!-- Withdrawals Approval Table -->
        <div class="bg-slate-900 p-6 rounded-2xl border border-slate-800">
            <h2 class="text-lg font-bold text-emerald-400 mb-4"><i class="fa-solid fa-money-bill-transfer mr-2"></i>Pending Withdrawals</h2>
            <table class="w-full text-left text-xs text-slate-400">
                <thead class="bg-slate-950">
                    <tr><th class="p-3">User</th><th class="p-3">Amount</th><th class="p-3">Method</th><th class="p-3">Account</th><th class="p-3">Action</th></tr>
                </thead>
                <tbody>
                    {% for w in withdrawals %}
                    <tr class="border-b border-slate-800">
                        <td class="p-3 text-white font-bold">{{ w.username }}</td>
                        <td class="p-3 text-emerald-400 font-bold">${{ w.amount }}</td>
                        <td class="p-3">{{ w.method }}</td>
                        <td class="p-3 font-mono text-cyan-300">{{ w.account }}</td>
                        <td class="p-3">
                            <a href="/admin/approve_withdrawal/{{ w._id }}" class="px-3 py-1 bg-emerald-500 text-slate-950 font-bold rounded">Approve</a>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- Settings Form -->
        <form action="/admin/save" method="POST" class="bg-slate-900 p-6 rounded-2xl border border-slate-800 space-y-4">
            <h2 class="text-lg font-bold text-fuchsia-400"><i class="fa-solid fa-gear mr-2"></i>Domain Rotator & AdSterra Settings</h2>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="text-xs text-slate-400">Primary Domain</label>
                    <input type="text" name="primaryDomain" value="{{ settings.primaryDomain }}" class="w-full bg-slate-950 p-3 rounded-xl border border-slate-800 text-cyan-400 text-xs">
                </div>
                <div>
                    <label class="text-xs text-slate-400">Backup Domain Rotator</label>
                    <input type="text" name="backupDomain" value="{{ settings.backupDomain }}" class="w-full bg-slate-950 p-3 rounded-xl border border-slate-800 text-cyan-400 text-xs">
                </div>
                <div>
                    <label class="text-xs text-slate-400">Popunder Code</label>
                    <textarea name="popunderCode" class="w-full bg-slate-950 p-2 border border-slate-800 text-xs text-cyan-300">{{ settings.popunderCode }}</textarea>
                </div>
                <div>
                    <label class="text-xs text-slate-400">Direct Link URL</label>
                    <input type="text" name="directLinkUrl" value="{{ settings.directLinkUrl }}" class="w-full bg-slate-950 p-3 rounded-xl border border-slate-800 text-cyan-300 text-xs">
                </div>
                <div>
                    <label class="text-xs text-slate-400">Banner Top</label>
                    <textarea name="bannerTop" class="w-full bg-slate-950 p-2 border border-slate-800 text-xs text-cyan-300">{{ settings.bannerTop }}</textarea>
                </div>
                <div>
                    <label class="text-xs text-slate-400">Native Ad Code</label>
                    <textarea name="nativeAd" class="w-full bg-slate-950 p-2 border border-slate-800 text-xs text-cyan-300">{{ settings.nativeAd }}</textarea>
                </div>
            </div>
            <button type="submit" class="px-6 py-3 bg-cyan-500 text-slate-950 font-bold rounded-xl">SAVE ALL CONFIGURATIONS</button>
        </form>
    </div>
</body>
</html>
"""

@admin_bp.route('/admin')
def admin_page():
    settings = get_settings()
    withdrawals = list(withdrawals_col.find({"status": "Pending"}))
    return render_template_string(ADMIN_HTML, settings=settings, withdrawals=withdrawals)

@admin_bp.route('/admin/approve_withdrawal/<id>')
def approve_withdrawal(id):
    from bson.objectid import ObjectId
    withdrawals_col.update_one({"_id": ObjectId(id)}, {"$set": {"status": "Approved"}})
    return redirect('/admin')

@admin_bp.route('/admin/save', methods=['POST'])
def save_settings():
    settings_col.update_one(
        {"_id": "global_settings"},
        {"$set": {
            "primaryDomain": request.form.get('primaryDomain'),
            "backupDomain": request.form.get('backupDomain'),
            "popunderCode": request.form.get('popunderCode'),
            "directLinkUrl": request.form.get('directLinkUrl'),
            "bannerTop": request.form.get('bannerTop'),
            "nativeAd": request.form.get('nativeAd')
        }}
    )
    return redirect('/admin')
