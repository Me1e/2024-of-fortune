import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

# FastAPI 애플리케이션을 생성합니다.
app = FastAPI()

# 스토리 요청을 위한 데이터 모델을 정의합니다.
class Data(BaseModel):
    name: Optional[str] = None

# "/api/story" 경로에 POST 요청을 받아 스토리를 생성하는 API 엔드포인트입니다.
@app.post("/api/story")
async def api_story(data: Data):
    # 요청된 스토리 토픽이 없으면 None을 반환합니다.
    if not data.name:
        return None

    # 스트리밍 응답으로 OpenAI를 이용해 스토리를 생성하고 반환합니다.
    return StreamingResponse(openai_stream(data.name), media_type="text/html")

# OpenAI를 이용해 스트리밍 방식으로 스토리를 생성하는 함수입니다.
async def openai_stream(name: str):
    # OpenAI 클라이언트를 초기화합니다.
    client = OpenAI(api_key="sk-your-key-here")

    # GPT-4 모델을 사용하여 스토리를 생성하는 요청을 보냅니다.
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You're a world-class fortune teller. You're reading someone else's 2024 fortunes. Try to be as positive as possible."},
            {"role": "user", "content": f"My job is a developer. My name is {name}. Look at my 2024 fortunes. In Korean."},
        ],
        stream=True
    )

    # 생성된 스토리를 청크 단위로 반환합니다.
    for chunk in completion:
        word = chunk.choices[0].delta.content
        if word is None:
            break
        yield word

# 경로 우선순위 조정을 위해 맨 마지막에 정적 파일 경로를 등록합니다.
app.mount("/", StaticFiles(directory="static", html=True))

# 메인 함수: 서버를 8080 포트에서 실행합니다.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))