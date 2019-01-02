import os

redis_url = os.getenv('REDIS_URL', None)

if redis_url:
    from urllib.parse import urlparse
    from rasa_core.tracker_store import RedisTrackerStore
    from redis import Redis

    parse_result = urlparse(redis_url)

    hostname = parse_result.hostname
    port = parse_result.port
    password = parse_result.password

    tracker_store = RedisTrackerStore(
        None, host=hostname, port=port, db=0, password=password
    )

    scheduler_store = Redis(
        host=hostname,
        port=port,
        db=5,
        password=password
    )
else:
    tracker_store = None
    scheduler_store = None