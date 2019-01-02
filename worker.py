from rq_scheduler.scheduler import Scheduler
from rasa.store import scheduler_store

if __name__ == '__main__':
    scheduler = Scheduler(connection=scheduler_store)
    scheduler.run()