import folium
import os

# 旅程の順番通りにストップを定義
stops = [
    {"num": 1,  "name": "東京（出国）",              "lat": 35.6762,  "lon": 139.6503, "country": "🇯🇵 日本",       "days": "-",  "note": "出国"},
    {"num": 2,  "name": "バンコク",                  "lat": 13.7563,  "lon": 100.5018, "country": "🇹🇭 タイ",       "days": "11", "note": "ワクチン接種・観光"},
    {"num": 3,  "name": "ムンバイ",                  "lat": 19.0760,  "lon": 72.8777,  "country": "🇮🇳 インド",     "days": "5",  "note": "ゲートウェイ・エレファンタ島"},
    {"num": 4,  "name": "ナイロビ・マサイマラ",       "lat": -1.2921,  "lon": 36.8219,  "country": "🇰🇪 ケニア",     "days": "14", "note": "マサイマラサファリ（グレートマイグレーション）"},
    {"num": 5,  "name": "カンパラ・ブウィンディ",     "lat": 0.3476,   "lon": 32.5825,  "country": "🇺🇬 ウガンダ",   "days": "8",  "note": "ゴリラトレッキング・チンパンジー"},
    {"num": 6,  "name": "キガリ",                    "lat": -1.9441,  "lon": 30.0619,  "country": "🇷🇼 ルワンダ",   "days": "4",  "note": "虐殺記念館・現代アフリカ"},
    {"num": 7,  "name": "ダルエスサラーム・ザンジバル","lat": -6.7924,  "lon": 39.2083,  "country": "🇹🇿 タンザニア", "days": "24", "note": "ザンジバル10日・キリマンジャロ登山8日"},
    {"num": 8,  "name": "ビクトリアフォールズ",       "lat": -17.9243, "lon": 25.8572,  "country": "🇿🇼 ジンバブエ", "days": "4",  "note": "世界三大瀑布・バンジージャンプ"},
    {"num": 9,  "name": "ウィントフック・ナミブ砂漠", "lat": -22.5597, "lon": 17.0832,  "country": "🇳🇦 ナミビア",   "days": "10", "note": "ナミブ砂漠・デッドフレイ"},
    {"num": 10, "name": "ケープタウン",               "lat": -33.9249, "lon": 18.4241,  "country": "🇿🇦 南アフリカ", "days": "14", "note": "テーブルマウンテン・喜望峰"},
    {"num": 11, "name": "サンパウロ・リオ・イグアス", "lat": -23.5505, "lon": -46.6333, "country": "🇧🇷 ブラジル",   "days": "14", "note": "イグアスの滝・コルコバード"},
    {"num": 12, "name": "ブエノスアイレス",           "lat": -34.6037, "lon": -58.3816, "country": "🇦🇷 アルゼンチン","days": "10", "note": "タンゴ・イグアス（アルゼンチン側）"},
    {"num": 13, "name": "サンティアゴ・アタカマ",     "lat": -33.4489, "lon": -70.6693, "country": "🇨🇱 チリ",       "days": "8",  "note": "アタカマ砂漠・星空観測"},
    {"num": 14, "name": "ウユニ・ラパス",             "lat": -19.5832, "lon": -65.7533, "country": "🇧🇴 ボリビア",   "days": "8",  "note": "ウユニ塩湖・死の道路"},
    {"num": 15, "name": "クスコ・マチュピチュ・リマ", "lat": -13.5319, "lon": -71.9675, "country": "🇵🇪 ペルー",     "days": "14", "note": "マチュピチュ・レインボーマウンテン"},
    {"num": 16, "name": "カルタヘナ・メデジン・ボゴタ","lat": 4.7110,   "lon": -74.0721, "country": "🇨🇴 コロンビア", "days": "12", "note": "カルタヘナ旧市街・コーヒー農園"},
    {"num": 17, "name": "アンティグア・アティトラン",  "lat": 14.5586,  "lon": -90.7295, "country": "🇬🇹 グアテマラ", "days": "10", "note": "マヤ遺跡・火山トレッキング"},
    {"num": 18, "name": "メキシコシティ",             "lat": 19.4326,  "lon": -99.1332, "country": "🇲🇽 メキシコ",   "days": "14", "note": "テオティワカン・チチェンイッツァ・年越し"},
    {"num": 19, "name": "東京（帰国）",               "lat": 35.6762,  "lon": 139.6503, "country": "🇯🇵 日本",       "days": "-",  "note": "帰国"},
]

# マップ作成（世界地図中心）
m = folium.Map(location=[20, 20], zoom_start=2, tiles="CartoDB positron")

# ルートを線で描画（飛行機区間は点線、陸路は実線）
air_segments = {(2,3), (3,4), (10,11), (15,16), (16,17), (18,19), (1,2)}
coords = [(s["lat"], s["lon"]) for s in stops]

for i in range(len(stops) - 1):
    pair = (stops[i]["num"], stops[i+1]["num"])
    is_air = pair in air_segments
    folium.PolyLine(
        locations=[coords[i], coords[i+1]],
        color="#E74C3C" if is_air else "#3498DB",
        weight=2.5,
        opacity=0.8,
        dash_array="8 4" if is_air else None,
        tooltip=f"{'✈️ 飛行機' if is_air else '🚌 陸路'}: {stops[i]['name']} → {stops[i+1]['name']}"
    ).add_to(m)

# 各ストップにマーカー追加
for s in stops:
    is_start_end = s["num"] in (1, 19)
    color = "red" if is_start_end else "blue"
    icon = "home" if is_start_end else "info-sign"

    popup_html = f"""
    <div style="font-family:sans-serif; min-width:180px;">
        <b style="font-size:14px;">#{s['num']} {s['name']}</b><br>
        <span style="color:#666;">{s['country']}</span><br>
        <hr style="margin:4px 0;">
        📅 滞在日数: <b>{s['days']}日</b><br>
        📌 {s['note']}
    </div>
    """

    folium.Marker(
        location=[s["lat"], s["lon"]],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=f"#{s['num']} {s['country']} {s['name']}",
        icon=folium.Icon(color=color, icon=icon, prefix="glyphicon")
    ).add_to(m)

    # ナンバーラベル
    folium.Marker(
        location=[s["lat"] + 1.5, s["lon"]],
        icon=folium.DivIcon(
            html=f'<div style="font-size:10px;font-weight:bold;color:#2C3E50;background:white;border-radius:50%;width:18px;height:18px;text-align:center;line-height:18px;border:1px solid #aaa;">{s["num"]}</div>',
            icon_size=(18, 18),
            icon_anchor=(9, 9)
        )
    ).add_to(m)

# 凡例
legend_html = """
<div style="position:fixed;bottom:30px;left:30px;z-index:1000;background:white;padding:12px;border-radius:8px;border:1px solid #ccc;font-family:sans-serif;font-size:12px;">
    <b>🌏 半年間バックパッカー旅程</b><br>
    <b>2026/7/6 〜 2027/1/6（184日・17カ国）</b><br><br>
    <span style="color:#E74C3C;">━ ━ ━</span> ✈️ 飛行機<br>
    <span style="color:#3498DB;">━━━</span> 🚌 陸路バス・電車<br>
    <span style="background:#E74C3C;color:white;padding:1px 5px;border-radius:3px;">●</span> 出発・帰国<br>
    <span style="background:#3498DB;color:white;padding:1px 5px;border-radius:3px;">●</span> 各ストップ
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# 保存
output = os.path.join(os.path.expanduser("~"), "Desktop", "trip_map.html")
m.save(output)
print(f"マップ作成完了: {output}")
