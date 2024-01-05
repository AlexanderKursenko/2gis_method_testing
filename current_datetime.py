from datetime import datetime

current_datetime = datetime.utcnow().replace(second=0, microsecond=0).isoformat()[:-3]
