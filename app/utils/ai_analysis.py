import httpx
import json
from app.core.config import settings

async def get_health_analysis_result(records: list, user_name: str) -> str:
    """
    Solar API를 호출하여 건강 기록을 분석합니다.
    :param records: DB에서 가져온 health_records 리스트 (JSON)
    :param user_name: 사용자 이름 (프롬프트 개인화용)
    :return: AI가 생성한 분석 보고서 (Markdown Text)
    """

    # 1. 시스템 프롬프트 구성
    system_prompt = f"""
    당신은 '할매피디아' 서비스의 **AI 건강 분석 전문가**입니다. 
    사용자({user_name} 어르신)의 지난 1년간 건강 기록을 분석하여 보고서를 작성하세요.

    # 역할 및 지침
    1. 데이터의 `content`에 포함된 거친 표현(비속어 등)은 통증의 강도로 이해하되, 결과물에는 순화된 표현을 사용하세요.
    2. `category` 빈도수를 분석하여 Top 3 증상을 추출하세요.
    3. 계절(`created_at`)과 증상의 연관성을 파악하세요.
    4. 말투는 손주처럼 다정하고 예의 바르게("할머니, 이때는 많이 편찮으셨네요") 작성하세요.

    # 출력 형식 (Markdown)
    ## 👵 {user_name}님의 건강 요약
    ### 1. 자주 말씀하신 증상
    * 1위: [증상명] (N회)
    ...
    ### 2. AI 손주의 분석
    ...
    ### 3. 한마디
    ...
    """

    # 2. 사용자 데이터(Context) 준비
    # DB 데이터를 문자열로 예쁘게 변환
    user_data_str = json.dumps(records, ensure_ascii=False, default=str)

    # 3. Solar API 요청 준비 (OpenAI Chat Completion 호환 방식)
    headers = {
        "Authorization": f"Bearer {settings.SOLAR_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "solar-pro",  # 혹은 사용 가능한 모델명 (solar-1-mini-chat 등)
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"다음은 {user_name}님의 건강 기록 데이터입니다. 분석해 주세요:\n{user_data_str}"}
        ],
        "temperature": 0.7
    }

    # 4. API 호출
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.SOLAR_BASE_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30.0  # 분석이 길어질 수 있으므로 타임아웃 넉넉히
            )

            if response.status_code != 200:
                print(f"Solar API Error: {response.text}")
                return "죄송해요, 할머니. 지금은 건강 기록을 읽어오는데 문제가 생겼어요. 잠시 후에 다시 시도해 주세요."

            result = response.json()
            return result["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"AI Analysis Error: {str(e)}")
        return "죄송해요, 분석 중에 오류가 발생했어요."