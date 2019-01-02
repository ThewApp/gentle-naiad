from rasa.store import scheduler_store
from rq_scheduler.scheduler import Scheduler
from rq_scheduler.utils import setup_loghandlers

setup_loghandlers('DEBUG')

if __name__ == '__main__':
    scheduler = Scheduler(
        connection=scheduler_store,
        interval=5
    )
    scheduler.run()