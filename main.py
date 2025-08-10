from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import openai

app = FastAPI()

# CORS: フロントエンドをホストするドメインを許可してください
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 環境変数で設定
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# 献立
GAS_WEBHOOK_MENU_PLAN = "https://script.google.com/macros/s/AKfycbyJb93GqckOEK-6Iw99XI7qpXjIgx_SclN1fGV0__nI4JqQR_uLMR0hIPCNjKOzRY-v/exec"

# 底値
GAS_WEBHOOK_LOWEST_PRICE = "https://script.google.com/macros/s/AKfycbwn8X6CY1gKDMI3FjONKw3NB9Msz8XSfP1j770y85FPjMJfbIx9Xl7PbrbC0DXYHiRQ/exec"

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

@app.post('/search')
async def search(req: Request):
    body = await req.json()
    mode = body.get('mode')
    keywords = body.get('keywords', {})
    ingredients_list = [
        i.strip() for i in keywords.get("ingredients", "").replace("、", ",").split(",") if i.strip()
    ]

    if mode == 'ai':
        if not OPENAI_API_KEY:
            raise HTTPException(status_code=500, detail='OpenAI API key not configured')
        # シンプルなプロンプト例。必要に応じて調整してください。
        prompt = (
            f"あなたは献立提案アシスタントです。\n"
            f"所要時間: {keywords.get('time','')}, 材料: {keywords.get('ingredients','')}, ジャンル: {keywords.get('category','')}\n"
            f"上記の条件で3件のメニュー（料理名、所要時間、主な材料、調理手順の簡単な説明）をJSONで返してください。"
        )

        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'user','content':prompt}],
            temperature=0.7,
            max_tokens=800
        )
        # 応答テキストをそのまま返す
        text = resp['choices'][0]['message']['content']
        return {'source':'ai','text':text}

    elif mode == 'history':
        if not GAS_WEBHOOK_MENU_PLAN:
            raise HTTPException(status_code=500, detail='GAS webhook not configured')
        # GAS にフォワード
        try:
            r = requests.post(GAS_WEBHOOK_MENU_PLAN, json={
                "mode": "history",
                "keywords": {
                    "time": keywords.get("time"),
                    "ingredients": ingredients_list,
                    "category": keywords.get("category")
                }
            }
            , timeout=10)
            r.raise_for_status()
            return {'source':'history','result': r.json()}
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f'GAS Error: {str(e)}')

    else:
        raise HTTPException(status_code=400, detail='mode must be "ai" or "history"')

@app.get("/items")
def get_items():
    try:
        resp = requests.get(GAS_WEBHOOK_LOWEST_PRICE, params={"mode": "list"})
        resp.raise_for_status()
        return resp.json()

    except Exception as e:
        return {"error": str(e)}

@app.post("/update")
async def update_item(request: Request):
    try:
        data = await request.json()
        mode = "new" if data.get("newItemMode") else "search"
        payload = {
            "mode": mode,
            "item": data.get("item"),
            "price": data.get("price"),
            "quantity": data.get("quantity"),
        }
        resp = requests.post(GAS_WEBHOOK_LOWEST_PRICE, json=payload)
        resp.raise_for_status()
        return resp.json()

    except Exception as e:
        return {"error": str(e)}

@app.get("/item_detail")
def get_item_detail(item: str = Query(..., description="品目名")):
    """指定品目の詳細情報を取得"""
    try:
        resp = requests.get(
            GAS_WEBHOOK_LOWEST_PRICE,
            params={"mode": "detail", "item": item}
        )
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}
