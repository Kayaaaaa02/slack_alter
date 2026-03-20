import anthropic
from ai.prompt import build_system_prompt


# 시스템 프롬프트를 한 번만 로딩 (모듈 레벨 캐시)
_system_prompt: str | None = None


def get_system_prompt() -> str:
    global _system_prompt
    if _system_prompt is None:
        _system_prompt = build_system_prompt()
    return _system_prompt


def reload_skill():
    """skill.md가 변경되었을 때 시스템 프롬프트를 다시 로딩"""
    global _system_prompt
    _system_prompt = None


def generate_response(
    message: str,
    channel_context: str = "",
    thread_messages: list[dict] | None = None,
) -> str:
    """Claude API를 호출하여 응답 생성

    Args:
        message: 사용자의 메시지
        channel_context: 채널 정보 (예: "#general")
        thread_messages: 스레드의 이전 메시지들 (대화 맥락 유지용)

    Returns:
        생성된 응답 텍스트
    """
    client = anthropic.Anthropic()

    # 대화 히스토리 구성
    messages = []

    # 스레드 컨텍스트가 있으면 이전 대화를 포함
    if thread_messages:
        for msg in thread_messages:
            role = "assistant" if msg.get("is_bot") else "user"
            messages.append({"role": role, "content": msg["text"]})

    # 현재 메시지 추가
    user_content = message
    if channel_context:
        user_content = f"[채널: {channel_context}]\n{message}"

    messages.append({"role": "user", "content": user_content})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=get_system_prompt(),
        messages=messages,
    )

    return response.content[0].text
