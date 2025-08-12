# ShelfScanApp API設計書(GAS)

## 1. エンドポイント
   Google Apps Script WebApp URL（例）：
   https://script.google.com/macros/s/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx/exec


## 2. 共通仕様
### 2.1 HTTPメソッド：GET / POST（用途に応じて選択）
### 2.2 Content-Type
- GET：application/x-www-form-urlencoded
- POST：application/json
### 2.3 共通パラメータ：
- action（string）：実行する処理種別
- その他のパラメータは action に応じて送信


## 3. アクション別仕様
### 3.1 一覧取得
- action：list
- メソッド：GET
- パラメータ：
- status（string, 任意）："pending" のみ取得する場合に指定
- 処理内容：Google Spreadsheet から購入予定品一覧を取得し、JSON配列として返却
- レスポンス例：
```json
    [
      { "id": "1", "name": "商品A", "price": 1200, "deadline": "2025-08-23", "status": "pending" },
      { "id": "2", "name": "商品B", "price": 500, "deadline": "2025-08-15", "status": "done" }
    ]
```
   ### 3.2 新規登録
- action：add
- メソッド：POST
- リクエストボディ：
```json
    {
      "name": "商品A",
      "price": 1200,
      "deadline": "2025-08-23"
    }
```
- 処理内容：Spreadsheet に新規行を追加（IDは自動採番）
- レスポンス例：
```json
    { "result": "success", "id": "3" }
```

### 3.3 ステータス更新
- action：update
- メソッド：POST
- リクエストボディ：
```json
    {
      "id": "3",
      "status": "done"
    }
```
- 処理内容：該当 ID の行を検索し、status を更新
- レスポンス例：
```json
    { "result": "success" }
```

### 3.4 削除
- action：delete
- メソッド：POST
- リクエストボディ：
```json
    {
      "id": "3"
    }
```
- 処理内容：該当 ID の行を削除
- レスポンス例：
```json
    { "result": "success" }
```


## 4. エラーレスポンス例
```json
   { "result": "error", "message": "Item not found" }
```


## 5. 備考
### 5.1 Spreadsheet 構造例
| ID | 品名   | 価格  | 期限         | ステータス
| -- | ------ | ----- | ------------ | ----------
| 1  | 商品A  | 1200  | 2025-08-23   | pending
| 2  | 商品B  | 500   | 2025-08-15   | done
