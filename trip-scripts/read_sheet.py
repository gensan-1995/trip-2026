import gspread, sys
sys.stdout.reconfigure(encoding='utf-8')
gc = gspread.oauth(credentials_filename='C:/Users/posit/Desktop/trip-scripts/credentials.json')
sh = gc.open_by_key('14Ry_9IsfaYg492icihQf9FYD6r3dmwDSL88EPbpbDrk')

print("=== シート一覧 ===")
for w in sh.worksheets():
    print(f"  {w.title} (gid={w.id})")

print("\n=== gid=1731212045 のシート内容 ===")
for w in sh.worksheets():
    if w.id == 1731212045:
        print(f"シート名: {w.title}")
        for row in w.get_all_values():
            print(row)
        break
