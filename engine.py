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
        "실제로 있는 보드게임인지 3번 더 확인해."
        "보드게임에 대한 질문이 아닌 경우에는 아무 답변도 하지마."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"룰을 가져오는 중 오류가 발생했습니다: {e}"

def get_game_rule_detailed(game_name: str, text: str) -> str:
    """
    주어진 보드게임에 대한 사용자의 질문에 대해 GPT에게 답변을 요청하고 반환한다.
    """
    prompt = (
        f"보드게임 '{game_name}'에 대해 다음 질문에 답변해줘: {text}. "
        "너무 어렵게 설명하지 말고, 핵심적인 행동 위주로 말해줘."
        "실제로 있는 보드게임인지 3번 더 확인해."
        "보드게임에 대한 질문이 아닌 경우에는 아무 답변도 하지마."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"질문에 대한 답변을 가져오는 중 오류가 발생했습니다: {e}"


def reset_chat() -> str:
    """
    GPT와의 대화를 초기화할 때 사용되는 메소드.
    """
    prompt = "대화를 초기화할게. 앞선 대화들은 모두 잊어줘."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"대화 초기화 중 오류가 발생했습니다: {e}"

"""
if __name__ == "__main__":
    game_name = input("룰을 알고 싶은 보드게임 이름을 입력하세요: ").strip()
    game_name = game_name.encode("utf-8", "ignore").decode("utf-8")
    rule = get_game_rule(game_name)
    print(f"'{game_name}'의 룰: {rule}")
    question = input("자세한 룰에 대해 질문이 있으면 입력하세요 (없으면 Enter): ").strip()
    if question:
        detailed_rule = get_game_rule_detailed(game_name, question)
        print(f"'{game_name}'에 대한 질문 '{question}'의 답변: {detailed_rule}")
    else:
        print("추가 질문이 없습니다. 프로그램을 종료합니다.")
"""