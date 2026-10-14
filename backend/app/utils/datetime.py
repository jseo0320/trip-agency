from datetime import datetime
from zoneinfo import ZoneInfo

def now_korea() -> datetime:
    return datetime.now(ZoneInfo("Asia/Seoul"))
