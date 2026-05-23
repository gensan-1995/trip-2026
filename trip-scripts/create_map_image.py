import gspread, sys, json, requests, os
from staticmap import StaticMap, Line, CircleMarker
sys.stdout.reconfigure(encoding='utf-8')

stops = [
    {"num": 1,  "lat": 35.6762,  "lon": 139.6503, "name": "①東京"},
    {"num": 2,  "lat": 13.7563,  "lon": 100.5018, "name": "②バンコク"},
    {"num": 3,  "lat": 19.0760,  "lon": 72.8777,  "name": "③ムンバイ"},
    {"num": 4,  "lat": -1.2921,  "lon": 36.8219,  "name": "④ナイロビ"},
    {"num": 5,  "lat": 0.3476,   "lon": 32.5825,  "name": "⑤カンパラ"},
    {"num": 6,  "lat": -1.9441,  "lon": 30.0619,  "name": "⑥キガリ"},
    {"num": 7,  "lat": -6.7924,  "lon": 39.2083,  "name": "⑦タンザニア"},
    {"num": 8,  "lat": -17.9243, "lon": 25.8572,  "name": "⑧ビクトリアフォールズ"},
    {"num": 9,  "lat": -22.5597, "lon": 17.0832,  "name": "⑨ナミビア"},
    {"num": 10, "lat": -33.9249, "lon": 18.4241,  "name": "⑩ケープタウン"},
    {"num": 11, "lat": -23.5505, "lon": -46.6333, "name": "⑪サンパウロ"},
    {"num": 12, "lat": -34.6037, "lon": -58.3816, "name": "⑫ブエノスアイレス"},
    {"num": 13, "lat": -33.4489, "lon": -70.6693, "name": "⑬サンティアゴ"},
    {"num": 14, "lat": -19.5832, "lon": -65.7533, "name": "⑭ウユニ"},
    {"num": 15, "lat": -13.5319, "lon": -71.9675, "name": "⑮マチュピチュ"},
    {"num": 16, "lat": 4.7110,   "lon": -74.0721, "name": "⑯ボゴタ"},
    {"num": 17, "lat": 14.5586,  "lon": -90.7295, "name": "⑰グアテマラ"},
    {"num": 18, "lat": 19.4326,  "lon": -99.1332, "name": "⑱メキシコシティ"},
    {"num": 19, "lat": 35.6762,  "lon": 139.6503, "name": "⑲東京"},
]

air_pairs = {(1,2),(2,3),(3,4),(10,11),(15,16),(16,17),(18,19)}

m = StaticMap(1400, 700, url_template='https://tile.openstreetmap.org/{z}/{x}/{y}.png')

# ルートライン描画
for i in range(len(stops)-1):
    a, b = stops[i], stops[i+1]
    pair = (a["num"], b["num"])
    color = "#E74C3C" if pair in air_pairs else "#3498DB"
    width = 3
    coords = [(a["lon"], a["lat"]), (b["lon"], b["lat"])]
    m.add_line(Line(coords, color, width))

# ストップのピン
for s in stops:
    is_endpoint = s["num"] in (1, 19)
    outer_color = "#C0392B" if is_endpoint else "#2980B9"
    m.add_marker(CircleMarker((s["lon"], s["lat"]), outer_color, 14))
    m.add_marker(CircleMarker((s["lon"], s["lat"]), "white", 7))

image = m.render()
output = os.path.join(os.path.expanduser("~"), "Desktop", "trip_map.png")
image.save(output)
print(f"PNG生成完了: {output}")

# Google Driveにアップロード
gc = gspread.oauth(credentials_filename='credentials.json')

with open(output, 'rb') as f:
    img_data = f.read()

metadata = {'name': 'trip_map.png', 'mimeType': 'image/png'}
boundary = 'boundary456'
body = (
    f'--{boundary}\r\nContent-Type: application/json\r\n\r\n'.encode() +
    json.dumps(metadata).encode() +
    f'\r\n--{boundary}\r\nContent-Type: image/png\r\n\r\n'.encode() +
    img_data +
    f'\r\n--{boundary}--'.encode()
)

resp = gc.http_client.request(
    'post',
    f'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart&fields=id,name',
    data=body,
    headers={'Content-Type': f'multipart/related; boundary={boundary}'}
)
file_id = json.loads(resp.text)['id']

# 公開設定
gc.http_client.request(
    'post',
    f'https://www.googleapis.com/drive/v3/files/{file_id}/permissions',
    json={'type': 'anyone', 'role': 'reader'}
)

img_url = f'https://drive.google.com/uc?export=view&id={file_id}'
print(f"Drive URL: {img_url}")

# スプシのルートマップシートに =IMAGE() で埋め込み
sh = gc.open_by_key('14Ry_9IsfaYg492icihQf9FYD6r3dmwDSL88EPbpbDrk')
for w in sh.worksheets():
    if w.title == 'ルートマップ':
        ws = w
        break

ws.update(
    values=[[f'=IMAGE("{img_url}", 1)']],
    range_name='A49',
    value_input_option='USER_ENTERED'
)

# 行の高さを拡大して地図を見やすく
sh.batch_update({
    "requests": [{
        "updateDimensionProperties": {
            "range": {
                "sheetId": ws.id,
                "dimension": "ROWS",
                "startIndex": 48,
                "endIndex": 49
            },
            "properties": {"pixelSize": 400},
            "fields": "pixelSize"
        }
    }, {
        "updateDimensionProperties": {
            "range": {
                "sheetId": ws.id,
                "dimension": "COLUMNS",
                "startIndex": 0,
                "endIndex": 7
            },
            "properties": {"pixelSize": 180},
            "fields": "pixelSize"
        }
    }]
})

ws.format('A48', {'textFormat': {'bold': True, 'fontSize': 12}})
ws.update(values=[['🗺️ ルートマップ（画像）']], range_name='A48', value_input_option='USER_ENTERED')

print("スプシへの埋め込み完了！")
