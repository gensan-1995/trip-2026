# 旅アプリ 2026-2027（trip-2026）

## プロジェクト概要
半年間バックパッカー世界一周（2026年7月〜2027年1月）の旅程管理Webアプリ。
GitHub Pages でホスティングし、mainブランチにpushすると自動デプロイされる。

## デプロイ
- **本番URL:** GitHub Pages（`gensan-1995/trip-2026` リポジトリのmainブランチ）
- **デプロイ方法:** `git push` → GitHub Actions が自動でデプロイ（`.github/workflows/deploy.yml`）

## ファイル構成

### GitHub管理（pushで反映）
| ファイル | 役割 |
|---|---|
| `index.html` | メインアプリ（地図・旅程・予算・持ち物リスト） |
| `location-update.html` | 現在地をFirebaseに更新するページ |
| `trip-scripts/` | Pythonスクリプト（Googleシート連携・KML生成等） |
| `.github/workflows/deploy.yml` | GitHub Actions デプロイ設定 |

### ローカルのみ（GitHubには上げない）
| ファイル | 役割 |
|---|---|
| `trip-2026-spec.md` | 旅行仕様書・計画メモ |
| `trip-files/` | KMLファイル・地図データ等 |
| `trip-scripts/credentials.json` | Google API認証情報（機密） |
| `*.csv` | スプレッドシートエクスポート |

## 技術スタック
- **フロントエンド:** HTML/CSS/JavaScript（バニラ）
- **地図:** Leaflet.js + OpenStreetMap
- **現在地共有:** Firebase Realtime Database
- **データ:** JavaScriptのデータ配列（stops）に旅程を直書き

## 注意事項
- `index.html` がメイン。`trip-website/` 内は古い複製なので編集しない
- Firebase の設定（apiKey等）は `index.html` 内に直書きされている（公開リポジトリのため問題ない設計）
- `credentials.json` は絶対にコミットしないこと
