import gspread, sys, json
sys.stdout.reconfigure(encoding='utf-8')
gc = gspread.oauth(credentials_filename='C:/Users/posit/Desktop/credentials.json')
sh = gc.open_by_key('14Ry_9IsfaYg492icihQf9FYD6r3dmwDSL88EPbpbDrk')

for w in sh.worksheets():
    if '持ち物' in w.title:
        data = w.get_all_values()
        for row in data:
            print(row)
        break
