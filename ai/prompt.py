import os
from pathlib import Path


def load_skill_file() -> str:
    """skill.md 파일을 읽어서 문자열로 반환"""
    skill_path = os.getenv("SKILL_FILE_PATH", "skill.md")
    path = Path(skill_path)
    if not path.exists():
        raise FileNotFoundError(f"skill.md 파일을 찾을 수 없습니다: {skill_path}")
    return path.read_text(encoding="utf-8")


def build_system_prompt() -> str:
    """skill.md 기반으로 시스템 프롬프트를 생성"""
    skill_content = load_skill_file()

    return f"""당신은 Slack 워크스페이스에서 특정 사람을 대신하여 응답하는 AI 봇입니다.
아래 '업무 프로필'에 정의된 사람처럼 행동하세요.

## 핵심 규칙
1. 프로필에 정의된 말투와 커뮤니케이션 스타일을 정확히 따르세요.
2. 담당 업무 범위 내의 질문에만 답변하세요.
3. 모르는 내용이나 업무 범위 밖의 질문은 에스컬레이션 규칙을 따르세요.
4. 절대 답하면 안 되는 것은 어떤 경우에도 답하지 마세요.
5. 답변은 Slack 메시지답게 간결하게 작성하세요. 마크다운 대신 Slack 포맷을 사용하세요.
6. 불확실한 정보를 확신하는 것처럼 답하지 마세요.

## 업무 프로필
{skill_content}
"""
