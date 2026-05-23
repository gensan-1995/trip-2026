import os

stops = [
    {"num": 1,  "name": "①東京（出国）",               "lat": 35.6762,  "lon": 139.6503, "days": "-",  "note": "成田発 Thai VietJet VZ831",                      "area": "日本"},
    {"num": 2,  "name": "②バンコク",                   "lat": 13.7563,  "lon": 100.5018, "days": "11", "note": "ワクチン一括接種・バンコク観光",                   "area": "アジア"},
    {"num": 3,  "name": "③ムンバイ",                   "lat": 19.0760,  "lon": 72.8777,  "days": "5",  "note": "ゲートウェイオブインディア・エレファンタ島",        "area": "アジア"},
    {"num": 4,  "name": "④ナイロビ・マサイマラ",        "lat": -1.2921,  "lon": 36.8219,  "days": "14", "note": "マサイマラサファリ（グレートマイグレーション）",    "area": "東アフリカ"},
    {"num": 5,  "name": "⑤カンパラ・ブウィンディ",      "lat": 0.3476,   "lon": 32.5825,  "days": "8",  "note": "ゴリラトレッキング・チンパンジートレッキング",      "area": "東アフリカ"},
    {"num": 6,  "name": "⑥キガリ",                     "lat": -1.9441,  "lon": 30.0619,  "days": "4",  "note": "虐殺記念館・現代アフリカの街並み",                 "area": "東アフリカ"},
    {"num": 7,  "name": "⑦ダルエスサラーム・ザンジバル・キリマンジャロ", "lat": -6.7924, "lon": 39.2083, "days": "24", "note": "ザンジバル島（10日）・キリマンジャロ登山（8日マチャメルート）", "area": "東アフリカ"},
    {"num": 8,  "name": "⑧ビクトリアフォールズ",        "lat": -17.9243, "lon": 25.8572,  "days": "4",  "note": "世界三大瀑布・バンジージャンプ・ラフティング",     "area": "南部アフリカ"},
    {"num": 9,  "name": "⑨ウィントフック・ナミブ砂漠",  "lat": -22.5597, "lon": 17.0832,  "days": "10", "note": "ナミブ砂漠・デッドフレイ・ソーサスフレイ",         "area": "南部アフリカ"},
    {"num": 10, "name": "⑩ケープタウン",                "lat": -33.9249, "lon": 18.4241,  "days": "14", "note": "テーブルマウンテン・喜望峰・ワインランド",         "area": "南部アフリカ"},
    {"num": 11, "name": "⑪サンパウロ・リオ・イグアス",  "lat": -23.5505, "lon": -46.6333, "days": "14", "note": "コルコバード・コパカバーナ・イグアスの滝（ブラジル側）", "area": "南米"},
    {"num": 12, "name": "⑫ブエノスアイレス",            "lat": -34.6037, "lon": -58.3816, "days": "10", "note": "イグアスの滝（アルゼンチン側）・タンゴショー",     "area": "南米"},
    {"num": 13, "name": "⑬サンティアゴ・アタカマ",      "lat": -33.4489, "lon": -70.6693, "days": "8",  "note": "アタカマ砂漠・月の谷・タティオ間欠泉・星空観測",   "area": "南米"},
    {"num": 14, "name": "⑭ウユニ・ラパス",              "lat": -19.5832, "lon": -65.7533, "days": "8",  "note": "ウユニ塩湖・星空ツアー・死の道路・ティワナク遺跡", "area": "南米"},
    {"num": 15, "name": "⑮クスコ・マチュピチュ・リマ",  "lat": -13.5319, "lon": -71.9675, "days": "14", "note": "マチュピチュ・クスコ旧市街・レインボーマウンテン",  "area": "南米"},
    {"num": 16, "name": "⑯カルタヘナ・メデジン・ボゴタ","lat": 4.7110,   "lon": -74.0721, "days": "12", "note": "カルタヘナ旧市街・メデジン・コーヒー農園",         "area": "南米"},
    {"num": 17, "name": "⑰アンティグア・アティトラン",   "lat": 14.5586,  "lon": -90.7295, "days": "10", "note": "アンティグア旧市街・アティトラン湖・マヤ遺跡・火山", "area": "中米"},
    {"num": 18, "name": "⑱メキシコシティ",              "lat": 19.4326,  "lon": -99.1332, "days": "14", "note": "テオティワカン・オアハカ・チチェンイッツァ・年越し","area": "中米"},
    {"num": 19, "name": "⑲東京（帰国）",                "lat": 35.6762,  "lon": 139.6503, "days": "-",  "note": "メキシコシティ→成田 帰国",                        "area": "日本"},
]

# エリア別アイコン色
area_style = {
    "日本":         ("ff0000ff", "http://maps.google.com/mapfiles/kml/paddle/red-circle.png"),
    "アジア":       ("ff00aaff", "http://maps.google.com/mapfiles/kml/paddle/ylw-circle.png"),
    "東アフリカ":   ("ff00cc44", "http://maps.google.com/mapfiles/kml/paddle/grn-circle.png"),
    "南部アフリカ": ("ff009933", "http://maps.google.com/mapfiles/kml/paddle/grn-circle.png"),
    "南米":         ("ffff6600", "http://maps.google.com/mapfiles/kml/paddle/blu-circle.png"),
    "中米":         ("ffcc44ff", "http://maps.google.com/mapfiles/kml/paddle/purple-circle.png"),
}

# 飛行機区間
air_pairs = {(1,2),(2,3),(3,4),(10,11),(15,16),(16,17),(18,19)}

kml = '''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>半年間バックパッカー旅程 2026/7/6〜2027/1/6</name>
  <description>17カ国・184日の世界一周ルート</description>

  <Style id="flight">
    <LineStyle><color>ff0000dd</color><width>3</width></LineStyle>
  </Style>
  <Style id="land">
    <LineStyle><color>ffdd6600</color><width>3</width></LineStyle>
  </Style>
'''

# エリア別スタイル
for area, (color, icon) in area_style.items():
    kml += f'''
  <Style id="pin_{area}">
    <IconStyle>
      <color>{color}</color>
      <scale>1.1</scale>
      <Icon><href>{icon}</href></Icon>
    </IconStyle>
    <BalloonStyle>
      <text><![CDATA[<b>$[name]</b><br/>$[description]]]></text>
    </BalloonStyle>
  </Style>'''

# ピン（各ストップ）
kml += '\n\n  <Folder><name>📍 ストップ一覧</name>\n'
for s in stops:
    area = s["area"]
    desc = f"滞在日数: {s['days']}日&#10;{s['note']}"
    kml += f'''
    <Placemark>
      <name>{s["name"]}</name>
      <description>{desc}</description>
      <styleUrl>#pin_{area}</styleUrl>
      <Point><coordinates>{s["lon"]},{s["lat"]},0</coordinates></Point>
    </Placemark>'''
kml += '\n  </Folder>\n'

# ルートライン
kml += '\n  <Folder><name>🗺️ ルート</name>\n'
for i in range(len(stops) - 1):
    a, b = stops[i], stops[i+1]
    pair = (a["num"], b["num"])
    is_air = pair in air_pairs
    style = "flight" if is_air else "land"
    label = "✈️ 飛行機" if is_air else "🚌 陸路"
    kml += f'''
    <Placemark>
      <name>{label}: {a["name"]}→{b["name"]}</name>
      <styleUrl>#{style}</styleUrl>
      <LineString>
        <tessellate>1</tessellate>
        <coordinates>{a["lon"]},{a["lat"]},0 {b["lon"]},{b["lat"]},0</coordinates>
      </LineString>
    </Placemark>'''
kml += '\n  </Folder>\n'

kml += '</Document>\n</kml>'

output = os.path.join(os.path.expanduser("~"), "Desktop", "trip_route.kml")
with open(output, "w", encoding="utf-8") as f:
    f.write(kml)
print(f"KML作成完了: {output}")
