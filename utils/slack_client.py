import os
import logging
from slack_sdk import WebClient

logger = logging.getLogger(__name__)

_client: WebClient | None = None


def get_client() -> WebClient:
    """Slack WebClient 싱글턴 반환"""
    global _client
    if _client is None:
        token = os.environ["SLACK_BOT_TOKEN"]
        _client = WebClient(token=token)
    return _client


def get_thread_messages(channel: str, thread_ts: str) -> list[dict]:
    """스레드의 메시지들을 가져와서 대화 맥락 구성

    Returns:
        [{"text": "...", "is_bot": True/False}, ...]
    """
    bot_user_id = os.getenv("BOT_USER_ID", "")
    client = get_client()

    result = client.conversations_replies(channel=channel, ts=thread_ts, limit=20)
    messages = []

    for msg in result.get("messages", [])[:-1]:  # 마지막 메시지(현재)는 제외
        messages.append({
            "text": msg.get("text", ""),
            "is_bot": msg.get("user") == bot_user_id,
        })

    return messages


def send_message(channel: str, text: str, thread_ts: str | None = None):
    """Slack에 메시지 전송"""
    client = get_client()
    client.chat_postMessage(channel=channel, text=text, thread_ts=thread_ts)


def get_channel_name(channel_id: str) -> str:
    """채널 ID로부터 채널 이름 조회"""
    try:
        client = get_client()
        result = client.conversations_info(channel=channel_id)
        return f"#{result['channel']['name']}"
    except Exception:
        logger.warning(f"채널 이름 조회 실패: {channel_id}")
        return channel_id
