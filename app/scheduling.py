import logging
import os
import sys
from threading import Thread
import urllib

from rq.compat import as_text, text_type
from rq.job import Job, _job_stack
from rq.worker import SimpleWorker, green, blue, yellow
from rq.connections import push_connection, pop_connection
from rq.registry import StartedJobRegistry
from rq.timeouts import JobTimeoutException
from rq.utils import utcnow

logger = logging.getLogger(__name__)

line_webhook = os.getenv("LINE_WEBHOOK_CHECK")

def reminder_job(e, dispatcher, agent, *args, **kwargs):
    if line_webhook:
        # Ping web
        Thread(target=urllib.request.urlopen, args=(line_webhook, )).start()
    agent.handle_reminder(e, dispatcher)

def rich_menu_update_things(userId, state, rich_menu, *args, **kwargs):
    if state == True:
        rich_menu.link_things(userId)
    elif state == False:
        rich_menu.unlink_things(userId)

class ReminderJob(Job):
    # Job execution
    def perform(self, workerKwargs):  # noqa
        """Invokes the job function with the job arguments."""
        self.connection.persist(self.key)
        _job_stack.push(self)
        try:
            self._kwargs.update(workerKwargs)
            self._result = self._execute()
        finally:
            assert self is _job_stack.pop()
        return self._result


class ReminderWorker(SimpleWorker):
    def work(self, *args, **kwargs):
        self.workerKwargs = kwargs.pop("workerKwargs", None)
        super().work(*args, **kwargs)

    def perform_job(self, job, queue, heartbeat_ttl=None):
        """Performs the actual work of a job.  Will/should only be called
        inside the work horse's process.
        """
        self.prepare_job_execution(job, heartbeat_ttl)

        push_connection(self.connection)

        started_job_registry = StartedJobRegistry(job.origin,
                                                  self.connection,
                                                  job_class=self.job_class)

        try:
            job.started_at = utcnow()
            timeout = job.timeout or self.queue_class.DEFAULT_TIMEOUT
            with self.death_penalty_class(timeout, JobTimeoutException, job_id=job.id):
                rv = job.perform(self.workerKwargs)

            job.ended_at = utcnow()

            # Pickle the result in the same try-except block since we need
            # to use the same exc handling when pickling fails
            job._result = rv

            self.handle_job_success(job=job,
                                    queue=queue,
                                    started_job_registry=started_job_registry)
        except:
            job.ended_at = utcnow()
            self.handle_job_failure(job=job,
                                    started_job_registry=started_job_registry)
            self.handle_exception(job, *sys.exc_info())
            return False

        finally:
            pop_connection()

        self.log.info('{0}: {1} ({2})'.format(
            green(job.origin), blue('Job OK'), job.id))
        if rv is not None:
            log_result = "{0!r}".format(as_text(text_type(rv)))
            self.log.debug('Result: %s', yellow(log_result))

        if self.log_result_lifespan:
            result_ttl = job.get_result_ttl(self.default_result_ttl)
            if result_ttl == 0:
                self.log.info('Result discarded immediately')
            elif result_ttl > 0:
                self.log.info(
                    'Result is kept for {0} seconds'.format(result_ttl))
            else:
                self.log.warning(
                    'Result will never expire, clean up result key manually')

        return True
