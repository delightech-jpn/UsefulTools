# 献立AIアプリ 設計書

---

## 1. 概要

- ユーザーが所要時間・材料・カテゴリを指定して献立検索できるWebアプリ  
- モードは2種類  
  - AIモード（OpenAI APIでメニュー生成）  
  - 履歴モード（Google スプレッドシートに保存された過去メニュー検索）  
- フロントエンドはレスポンシブHTML（スマホ対応）  
- バックエンドはFastAPIでRender.comにデプロイ  
- Google Apps Script（GAS）でスプレッドシート連携を実装  

---

## 2. システム構成

| コンポーネント           | 技術 / サービス            | 役割                                  |
|------------------------|--------------------------|-------------------------------------|
| フロントエンド           | HTML/CSS/JavaScript      | 入力フォーム表示、API呼び出し、結果表示         |
| バックエンドAPI          | Python FastAPI           | リクエスト受け取り、OpenAI・GAS連携処理         |
| OpenAI API             | OpenAI                  | AI献立提案の生成                      |
| Google Apps Script(GAS) | Google Apps Script       | スプレッドシートアクセス、履歴検索・登録処理        |
| スプレッドシート         | Google Sheets            | 過去の献立データの保存・管理                |
| ホスティング             | Render.com, GitHub Pages | FastAPIのホスティング(Render)、静的HTML配信(GitHub Pages) |

---

## 3. 詳細設計

### 3-1. フロントエンド

- 入力項目  
  - モード（`ai` or `history`）: select  
  - 所要時間（分）: number入力  
  - 材料: カンマ区切りテキスト  
  - カテゴリ: select（和食、中華、洋食、その他）  

- ボタン押下で `/search` エンドポイントへPOST  
- 結果はテーブル形式で表示  
- スマホ対応（レスポンシブデザイン）  

---

### 3-2. バックエンド（FastAPI）

- `/search` (POST)  
  - リクエストJSON例  
    ```json
    {
      "mode": "ai",
      "keywords": {
        "time": "30",
        "ingredients": "豚肉, にんじん",
        "category": "洋食"
      }
    }
    ```
  - `mode == "ai"` の場合  
    - OpenAI APIにプロンプト送信し、献立提案結果を取得  
    - JSONテキストでフロントへ返却  
  - `mode == "history"` の場合  
    - GASのWebhook URLへ検索キーワードを送信  
    - スプレッドシートから該当メニューを取得・登録し結果返却  
- CORS設定あり（フロントのオリジン許可）  

---

### 3-3. Google Apps Script (GAS)

- doPost(e)  
  - POSTデータをパースし、検索キーワードを取得  
  - スプレッドシートのデータ範囲を走査し条件に合うメニューを抽出  
  - 結果をJSONで返す  
  - 該当なしの場合はキーワードを新規行に保存  
- スプレッドシート列構成例  
  - timestamp, time, ingredients, category, found, menu_json  

---

## 4. API仕様

| エンドポイント | メソッド | 入力例 (JSON)                             | 出力例 (JSON)                                  | 備考                      |
|---------------|---------|-----------------------------------------|----------------------------------------------|-------------------------|
| `/search`     | POST    | See 上記の3-2リクエスト例                 | AI or スプレッドシート結果のJSON                  | モードによって処理を分ける       |

---

## 5. デプロイ・環境設定

| 項目                   | 内容                                  |
|----------------------|-------------------------------------|
| FastAPIホスティング        | Render.com                           |
| 環境変数                | OPENAI_API_KEY（OpenAIキー）          |
|                      | GAS_WEBHOOK（GASのウェブアプリURL）     |
| 静的HTMLホスティング        | GitHub Pages（index.htmlを配置）          |
| Google スプレッドシートID   | GASコード内の`SPREADSHEET_ID`に設定       |

---

## 6. 今後の拡張案

- AIのレスポンスをJSON解析してUIで構造化表示  
- 材料やカテゴリの自動補完やタグ入力UI  
- 履歴検索の絞り込み強化（部分一致、複数条件）  
- ユーザー認証・アクセス制限強化（GASの認証やAPIキー管理）  
- スマホUIの改善（調理手順の折りたたみ表示など）  

---

