from fastapi import FastAPI, Request, HTTPException
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
GAS_WEBHOOK = "https://script.google.com/macros/s/AKfycbxEMoykB7CFuKLL-BTbqj3bUJX2iTkSj_fAg7jLbvkkijzpMCZK0K97y-I2GsbKFEg/exec"

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


@app.post('/search')
async def search(req: Request):
    body = await req.json()
    mode = body.get('mode')
    keywords = body.get('keywords', {})

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
        if not GAS_WEBHOOK:
            raise HTTPException(status_code=500, detail='GAS webhook not configured')
        # GAS にフォワード
        try:
            r = requests.post(GAS_WEBHOOK, json={'keywords': keywords}, timeout=10)
            r.raise_for_status()
            return {'source':'history','result': r.json()}
        except requests.RequestException as e:
            raise HTTPException(status_code=500, detail=f'GAS Error: {str(e)}')

    else:
        raise HTTPException(status_code=400, detail='mode must be "ai" or "history"')
