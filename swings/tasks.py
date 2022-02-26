from celery import shared_task
from time import sleep
from celery_progress.backend import ProgressRecorder

@shared_task(bind=True)
def test_task(self, duration):
    print("start task")
    progress_recorder = ProgressRecorder(self)
    for i in range(100):
        sleep(0.1)
        progress_recorder.set_progress(i, 100, 'iteration: ' + str(i))
    print("task completed")
    return "done sleeping"