import openai
import os
from dotenv import load_dotenv

print("hello")
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_game_rule(game_name: str) -> str:
    """
    주어진 보드게임 이름에 대한 간단한 룰 설명을 GPT에게 요청하고 반환한다.
    """
    prompt = (
        f"보드게임 '{game_name}'의 핵심 규칙을 초보자도 이해할 수 있게 간단히 5줄 이내로 요약해줘. "
        "너무 어렵게 설명하지 말고, 핵심적인 행동 위주로 말해줘."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ 룰을 가져오는 중 오류가 발생했습니다: {e}"

if __name__ == "__main__":
    game_name = input("룰을 알고 싶은 보드게임 이름을 입력하세요: ").strip()
    game_name = game_name.encode("utf-8", "ignore").decode("utf-8")
    rule = get_game_rule(game_name)
    print(f"'{game_name}'의 룰: {rule}")