import os

redis_url = os.getenv('REDIS_URL', None)

if redis_url:
    from urllib.parse import urlparse
    from rasa_core.tracker_store import RedisTrackerStore
    from redis import Redis

    class PickableRedisTrackerStore(RedisTrackerStore):
        def __init__(self, domain, host='localhost',
                     port=6379, db=0, password=None, event_broker=None,
                     record_exp=None):
            self.connection = {
                "host": host,
                "port": port,
                "db": db,
                "password": password
            }

            super().__init__(domain, host,
                             port, db, password,
                             event_broker, record_exp)

        def __getstate__(self):
            # Copy the object's state from self.__dict__ which contains
            # all our instance attributes. Always use the dict.copy()
            # method to avoid modifying the original state.
            state = self.__dict__.copy()
            # Remove the unpicklable entries.
            del state['red']
            return state

        def __setstate__(self, state):
            # Restore instance attributes.
            self.__dict__.update(state)
            # Restore the previously opened file's state. To do so, we need to
            # reopen it and read from it until the line count is restored.
            import redis
            self.red = redis.StrictRedis(host=self.connection["host"], port=self.connection["port"], db=self.connection["db"],
                                         password=self.connection["password"])

    parse_result = urlparse(redis_url)

    hostname = parse_result.hostname
    port = parse_result.port
    password = parse_result.password

    tracker_store = PickableRedisTrackerStore(
        None, host=hostname, port=port, db=0, password=password
    )

    scheduler_store = Redis(
        host=hostname,
        port=port,
        db=1,
        password=password
    )
else:
    tracker_store = None
    scheduler_store = None
