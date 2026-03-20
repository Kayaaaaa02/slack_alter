import logging
from ai.responder import generate_response
from utils.slack_client import get_thread_messages

logger = logging.getLogger(__name__)


def handle_dm(event: dict, say):
    """DM 메시지 처리"""
    text = event.get("text", "")
    channel = event.get("channel", "")
    thread_ts = event.get("thread_ts") or event.get("ts")
    user = event.get("user", "")

    if not text.strip():
        return

    logger.info(f"DM 수신 - 유저: {user}, 메시지: {text[:50]}")

    # 스레드 컨텍스트 가져오기
    thread_messages = []
    if event.get("thread_ts"):
        thread_messages = get_thread_messages(channel, event["thread_ts"])

    try:
        response = generate_response(
            message=text,
            channel_context="DM",
            thread_messages=thread_messages,
        )
        say(text=response, thread_ts=thread_ts)
    except Exception:
        logger.exception("DM 응답 생성 실패")
        say(text="잠시 오류가 발생했어요. 다시 시도해주세요!", thread_ts=thread_ts)
