from celery import shared_task
from time import sleep
from celery_progress.backend import ProgressRecorder
from django.core.files.storage import default_storage

@shared_task(bind=True)
def test_task(self, path):
    print("start task")
    progress_recorder = ProgressRecorder(self)
    for i in range(100):
        sleep(0.1)
        progress_recorder.set_progress(i, 100, 'iteration: ' + str(i))
    try:
        # Delete video if it was stored in default storage
        default_storage.delete(path)
    except:
        print("path was not in default_storage")
    return "done sleeping"