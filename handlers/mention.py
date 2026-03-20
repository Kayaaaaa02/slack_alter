import logging
import re
from ai.responder import generate_response
from utils.slack_client import get_thread_messages, send_message, get_channel_name

logger = logging.getLogger(__name__)


def handle_mention(event: dict, say):
    """봇이 @멘션되었을 때 처리"""
    text = event.get("text", "")
    channel = event.get("channel", "")
    thread_ts = event.get("thread_ts") or event.get("ts")
    user = event.get("user", "")

    # 봇 멘션 태그 제거 (예: <@U12345>)
    clean_text = re.sub(r"<@[A-Z0-9]+>\s*", "", text).strip()

    if not clean_text:
        say(text="네, 말씀하세요!", thread_ts=thread_ts)
        return

    logger.info(f"멘션 수신 - 채널: {channel}, 유저: {user}, 메시지: {clean_text[:50]}")

    # 스레드 컨텍스트 가져오기
    thread_messages = []
    if event.get("thread_ts"):
        thread_messages = get_thread_messages(channel, event["thread_ts"])

    channel_name = get_channel_name(channel)

    try:
        response = generate_response(
            message=clean_text,
            channel_context=channel_name,
            thread_messages=thread_messages,
        )
        say(text=response, thread_ts=thread_ts)
    except Exception:
        logger.exception("응답 생성 실패")
        say(text="잠시 오류가 발생했어요. 다시 시도해주세요!", thread_ts=thread_ts)
