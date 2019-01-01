from rasa_core.tracker_store import RedisTrackerStore

import os
from urllib.parse import urlparse

redis_url = os.getenv('REDIS_URL', None)

if redis_url:
    parse_result = urlparse(redis_url)

    hostname = parse_result.hostname
    port = parse_result.port
    password = parse_result.password

    tracker_store = RedisTrackerStore(
        None, host=hostname, port=port, password=password
    )
else:
    tracker_store = None
