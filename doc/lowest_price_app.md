# 底値管理アプリ 設計書

## 1. システム概要
品目ごとの「底値（最安値）」を管理し、入力された価格・数量から計算した単価が過去の記録より安ければ更新するアプリ。  
**フロントエンド（HTML）** → **FastAPI（Render.com）** → **Google Apps Script (GAS)** → **Google Spreadsheet** の流れでデータを取得・更新する。

---

## 2. システム構成図

```mermaid
flowchart TB
    A[ブラウザ\n(HTML + JavaScript)] -->|HTTP GET/POST| B[FastAPI\n(Render.com)]
    B -->|GET/POST (mode指定)| C[GAS Web App]
    C -->|Spreadsheet API| D[Google Spreadsheet]
    D -->|品目・価格データ| C
    C -->|JSONレスポンス| B
    B -->|JSONレスポンス| A
```

---

## 3. 機能一覧

### (1) フロントエンド（HTML）
- **品目選択/入力**
  - `<input list="items">` により、DB（Spreadsheet）から取得した品目候補を表示。
  - 候補にない場合は手入力可能（新規登録モード）。
- **参照領域**
  - 選択した品目の底値情報（価格・数量・単価）を表示。
  - 取得中は「読み込み中...」を表示。
- **入力領域**
  - 新しい価格・数量を入力し、「登録」ボタンで更新。
  - 単価は自動計算して参照専用フィールドに表示。
- **新規登録モード**
  - 品目名がDBに存在しない場合、自動的に新規登録モードで処理。
- **UI構造**
  - 「参照領域」と「入力領域」を上下に並べ、それぞれ枠線で囲む。
- **底値更新中表示**  
  - 「登録」ボタン押下後、更新処理が完了するまで「更新中...」を参照領域に表示。
- **更新後の参照情報自動更新**  
  - 更新処理完了後、最新の底値情報を取得し、参照領域を最新化する。

---

### (2) FastAPI（Render.com）
環境変数 `GAS_WEBHOOK_URL` で GAS の URL を設定。

- **GET `/items`**
  - mode=`list` でGASに品目一覧取得を依頼し、JSON返却。

- **GET `/item_detail?item=XXX`**
  - mode=`all_data` でGASから全データ取得後、該当品目を検索して返却。

- **POST `/update`**
  - newItemMode=True → mode=`new` でGASへ新規登録依頼。
  - newItemMode=False → mode=`search` で底値更新処理依頼。
  - 更新完了後に `/item_detail` を呼び出し、最新情報を返却。

- **GET `/`**
  - API稼働確認用ステータス返却。

---

### (3) Google Apps Script（GAS）
- **doGet**
  - `mode=list` → Spreadsheetの品目一覧を返す。
  - `mode=detail` → 選択品目の詳細データを返す。
- **doPost**
  - `mode=search` → 該当品目の底値比較・更新。
  - `mode=new` → 新規品目登録。
- **返却データ形式**
  - JSON形式（例：`{ "item": "りんご", "price": 100, "quantity": 3, "unit_price": 33.33 }`）

---

### (4) Google Spreadsheet 構成
1行目にヘッダー、2行目以降データ。

| 品目 (item) | 価格 (price) | 数量 (quantity) | 単価 (unit_price) | 更新日 (updated_at) |
|-------------|-------------|-----------------|-------------------|---------------------|
| りんご      | 100         | 3               | 33.33             | 2025/08/10          |
| バナナ      | 150         | 5               | 30.00             | 2025/08/09          |

---

## 4. データフロー

### 更新時
1. ユーザがHTMLで品目を選択/入力 → 価格・数量を入力。
2. 「底値更新」ボタン押下 → 「更新中...」表示開始。
3. FastAPIに `/update` POST。
4. FastAPIが mode（`new` or `search`）を判定しGASへ送信。
5. GASがSpreadsheetを更新。
6. 更新結果をFastAPIに返却。
7. FastAPIが `/item_detail` を呼び出して最新情報取得。
8. HTMLの参照領域を最新化し、「更新中...」表示を解除。

---

## 5. 補足仕様
- 単価は `価格 ÷ 数量` で小数第2位まで計算。
- 品目詳細取得時・更新処理中はローディング表示。
- 新規登録と既存更新は同じフォームから処理可能。
- CORS設定済み（フロントエンドから直接API呼び出し可）。
