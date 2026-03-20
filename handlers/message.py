import os
import logging
import re
from ai.responder import generate_response, reload_skill
from utils.slack_client import get_thread_messages, send_message, get_channel_name

logger = logging.getLogger(__name__)


def handle_message(event: dict, say):
    """채널 메시지 처리 (멘션이 아닌 일반 메시지)

    봇이 직접 멘션되지 않은 채널 메시지를 처리합니다.
    기본적으로 모든 메시지에 반응하지 않고,
    특정 키워드가 포함된 경우에만 반응합니다.
    """
    # 봇 자신의 메시지는 무시
    bot_user_id = os.getenv("BOT_USER_ID", "")
    if event.get("user") == bot_user_id:
        return

    # bot_message 서브타입 무시
    if event.get("subtype") == "bot_message":
        return

    text = event.get("text", "")
    channel = event.get("channel", "")
    thread_ts = event.get("thread_ts") or event.get("ts")

    # 이미 멘션 핸들러에서 처리되는 메시지는 스킵
    if re.search(rf"<@{bot_user_id}>", text):
        return

    # === 관리 명령어 ===
    my_user_id = os.getenv("MY_REAL_USER_ID", "")

    # 본인만 사용 가능한 명령어: skill 리로드
    if event.get("user") == my_user_id and text.strip().lower() == "!reload":
        reload_skill()
        say(text="skill.md를 다시 로딩했습니다.", thread_ts=thread_ts)
        return

    # === 키워드 기반 자동 응답 (선택사항) ===
    # 필요하면 아래 주석을 해제하고 키워드를 설정하세요.
    # 기본값은 비활성화 — 멘션(@봇)이나 DM으로만 반응합니다.
    #
    # TRIGGER_KEYWORDS = ["배포", "장애", "API"]
    # if not any(kw in text for kw in TRIGGER_KEYWORDS):
    #     return
    #
    # channel_name = get_channel_name(channel)
    # thread_messages = []
    # if event.get("thread_ts"):
    #     thread_messages = get_thread_messages(channel, event["thread_ts"])
    #
    # try:
    #     response = generate_response(
    #         message=text,
    #         channel_context=channel_name,
    #         thread_messages=thread_messages,
    #     )
    #     say(text=response, thread_ts=thread_ts)
    # except Exception:
    #     logger.exception("응답 생성 실패")
