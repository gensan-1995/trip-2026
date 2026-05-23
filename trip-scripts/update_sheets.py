"""
Google スプレッドシート 編集スクリプト
初回実行時: ブラウザが開いてGoogleアカウント認証が必要
2回目以降: 自動認証
"""

import gspread

SPREADSHEET_ID = "14Ry_9IsfaYg492icihQf9FYD6r3dmwDSL88EPbpbDrk"
SHEET_GID = 1333808764


def get_worksheet():
    gc = gspread.oauth(
        credentials_filename="C:/Users/posit/Desktop/credentials.json"
    )
    sh = gc.open_by_url(f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit")
    # gidでシートを取得
    for ws in sh.worksheets():
        if ws.id == SHEET_GID:
            return ws
    raise ValueError(f"gid={SHEET_GID} のシートが見つかりません")


def read_sheet():
    ws = get_worksheet()
    data = ws.get_all_values()
    print(f"シート名: {ws.title}")
    print(f"行数: {len(data)}")
    for i, row in enumerate(data[:10], 1):  # 先頭10行表示
        print(f"  行{i}: {row}")
    return data


def write_cell(row, col, value):
    """
    セルに値を書き込む
    row, col: 1始まりの行・列番号
    例: write_cell(1, 1, "テスト") → A1に書き込み
    """
    ws = get_worksheet()
    ws.update_cell(row, col, value)
    print(f"書き込み完了: ({row}, {col}) = {value}")


def write_range(start_cell, values):
    """
    範囲に値を書き込む
    start_cell: "A1" などのセル名
    values: 2次元リスト [[行1], [行2], ...]
    例: write_range("A1", [["名前", "値"], ["田中", 10]])
    """
    ws = get_worksheet()
    ws.update(start_cell, values)
    print(f"書き込み完了: {start_cell} から {len(values)}行")


if __name__ == "__main__":
    # まず現在のデータを読み取り表示
    read_sheet()

