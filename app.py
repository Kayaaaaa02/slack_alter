"""
Slack Alter-Ego Bot
===================
skill.md에 정의된 업무 프로필을 기반으로
Slack에서 나를 대신하여 응답하는 봇.

실행 방법:
    1. .env 파일 설정 (.env.example 참고)
    2. pip install -r requirements.txt
    3. python app.py
"""

import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from handlers.mention import handle_mention
from handlers.message import handle_message
from handlers.dm import handle_dm

# 환경변수 로딩
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Slack App 초기화 (Socket Mode 사용)
app = App(token=os.environ["SLACK_BOT_TOKEN"])


# === 이벤트 핸들러 등록 ===

@app.event("app_mention")
def on_mention(event, say):
    """봇이 @멘션되었을 때"""
    handle_mention(event, say)


@app.event("message")
def on_message(event, say):
    """채널/DM 메시지 수신 시"""
    # DM 채널 여부 판별 (channel_type: "im")
    channel_type = event.get("channel_type", "")

    if channel_type == "im":
        handle_dm(event, say)
    else:
        handle_message(event, say)


# === 앱 시작 ===

if __name__ == "__main__":
    logger.info("Slack Alter-Ego Bot 시작...")
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
