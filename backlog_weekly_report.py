"""
Backlog 課題作成者 集計レポート
使い方:
  python backlog_weekly_report.py          # 週次（直近7日）
  python backlog_weekly_report.py --monthly # 月次（前月1日〜末日）
"""

import os
import sys
import argparse
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import csv
from dotenv import load_dotenv

load_dotenv()

# ========== 設定 ==========
API_KEY      = os.environ["BACKLOG_API_KEY"]
SPACE_ID     = os.environ["BACKLOG_SPACE_ID"]
DOMAIN       = os.environ["BACKLOG_DOMAIN"]
PROJECT_KEY  = os.environ["BACKLOG_PROJECT_KEY"]

NOTION_TOKEN     = os.environ["NOTION_TOKEN"]
NOTION_PARENT_ID = os.environ["NOTION_PARENT_ID"]
# ==========================

BASE_URL = f"https://{SPACE_ID}.{DOMAIN}/api/v2"


def get_date_range(monthly=False):
    today = datetime.now()
    if monthly:
        first_of_this_month = today.replace(day=1)
        last_of_prev = first_of_this_month - timedelta(days=1)
        since = last_of_prev.replace(day=1).strftime("%Y-%m-%d")
        until = last_of_prev.strftime("%Y-%m-%d")
    else:
        since = (today - timedelta(days=7)).strftime("%Y-%m-%d")
        until = today.strftime("%Y-%m-%d")
    return since, until


def get_issues_for_week(monthly=False):
    """課題を全件取得（週次 or 月次）"""
    since, until = get_date_range(monthly)

    all_issues = []
    offset = 0
    count = 100  # 1回あたりの取得件数（最大100）

    project_id = get_project_id()
    issue_type_id = get_issue_type_id()
    print(f"取得期間: {since} 〜 {until}")
    print("課題を取得中...")

    while True:
        params = {
            "apiKey": API_KEY,
            "projectId[]": project_id,
            "issueTypeId[]": issue_type_id,
            "statusId[]": 1,  # 1=未対応（新規）
            "createdSince": since,
            "createdUntil": until,
            "count": count,
            "offset": offset,
        }
        resp = requests.get(f"{BASE_URL}/issues", params=params)
        resp.raise_for_status()
        issues = resp.json()

        if not issues:
            break

        all_issues.extend(issues)
        offset += len(issues)

        if len(issues) < count:
            break

    print(f"取得件数: {len(all_issues)} 件\n")
    return all_issues


def get_project_id():
    """プロジェクトキーからプロジェクトIDを取得"""
    resp = requests.get(
        f"{BASE_URL}/projects/{PROJECT_KEY}",
        params={"apiKey": API_KEY}
    )
    resp.raise_for_status()
    return resp.json()["id"]


def get_issue_type_id():
    """「課題」タイプのIDを取得"""
    resp = requests.get(
        f"{BASE_URL}/projects/{PROJECT_KEY}/issueTypes",
        params={"apiKey": API_KEY}
    )
    resp.raise_for_status()
    for t in resp.json():
        if t["name"] == "課題":
            return t["id"]
    raise ValueError("「課題」タイプが見つかりませんでした。利用可能なタイプ: " +
                     str([t["name"] for t in resp.json()]))


def aggregate_by_creator(issues):
    """作成者ごとに集計（キー・件名リスト付き）"""
    data = defaultdict(list)
    for issue in issues:
        creator = issue["createdUser"]["name"]
        data[creator].append({"key": issue["issueKey"], "summary": issue["summary"]})
    return dict(sorted(data.items(), key=lambda x: len(x[1]), reverse=True))


def print_report(data, since, until):
    """コンソールに表示"""
    print("=" * 60)
    print(f"課題作成者 週間集計レポート")
    print(f"期間: {since} 〜 {until}")
    print(f"プロジェクト: {PROJECT_KEY}")
    print("=" * 60)
    for name, subjects in data.items():
        print(f"\n{name}（{len(subjects)}件）")
        for s in subjects:
            print(f"  ・[{s['key']}] {s['summary']}")
    print("\n" + "-" * 60)
    print(f"合計: {sum(len(v) for v in data.values())} 件")
    print("=" * 60)


def save_csv(data, since, until):
    """CSVファイルに保存"""
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = os.path.join(desktop, f"backlog_report_{since}_{until}.csv")
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["作成者", "Backlogキー", "件名", "期間開始", "期間終了", "プロジェクト"])
        for name, subjects in data.items():
            for s in subjects:
                writer.writerow([name, s["key"], s["summary"], since, until, PROJECT_KEY])
    print(f"\nCSV保存完了: {filename}")
    return filename


def post_to_notion(data, since, until):
    """Notionに週次レポートページを作成"""
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    # ページ本文のブロックを組み立て
    blocks = [
        {
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": f"期間: {since} 〜 {until}　／　プロジェクト: {PROJECT_KEY}"}}],
                "icon": {"emoji": "📅"},
                "color": "gray_background",
            }
        }
    ]

    for name, subjects in data.items():
        # 作成者の見出し
        blocks.append({
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": f"{name}　({len(subjects)}件)"}}]
            }
        })
        # 課題ごとの箇条書き
        for s in subjects:
            blocks.append({
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {"type": "text", "text": {"content": s["key"], "link": {"url": f"https://{SPACE_ID}.{DOMAIN}/view/{s['key']}"}}, "annotations": {"code": True}},
                        {"type": "text", "text": {"content": f"  {s['summary']}"}},
                    ]
                }
            })

    # 合計
    blocks.append({
        "object": "block",
        "type": "divider",
        "divider": {}
    })
    blocks.append({
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [{"type": "text", "text": {"content": f"合計: {sum(len(v) for v in data.values())} 件"},
                           "annotations": {"bold": True}}]
        }
    })

    payload = {
        "parent": {"page_id": NOTION_PARENT_ID},
        "icon": {"emoji": "📊"},
        "properties": {
            "title": {
                "title": [{"text": {"content": f"Backlog週次レポート　{since} 〜 {until}"}}]
            }
        },
        "children": blocks,
    }

    resp = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)
    resp.raise_for_status()
    page_url = resp.json().get("url", "")
    print(f"Notion投稿完了: {page_url}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--monthly", action="store_true", help="月次レポート（前月集計）")
    args = parser.parse_args()

    since, until = get_date_range(args.monthly)

    try:
        issues = get_issues_for_week(args.monthly)
        data = aggregate_by_creator(issues)
        print_report(data, since, until)
        save_csv(data, since, until)
        post_to_notion(data, since, until)
    except requests.HTTPError as e:
        print(f"APIエラー: {e}")
        print(f"レスポンス: {e.response.text}")
        sys.exit(1)


if __name__ == "__main__":
    main()
