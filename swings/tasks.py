from re import I
from time import sleep
from celery import shared_task
from celery_progress.backend import ProgressRecorder
import random
from .models import Swing
# Now do your import
from .tracker.main import analyze
#from .videoanalysis import analyze
import base64

@shared_task(bind=True)
def test_task(self, swing_id):
    print("start task")
    swing = Swing.objects.get(pk=swing_id)
    progress_recorder = ProgressRecorder(self)
    for i in range(15):
        #simulate video analysis
        sleep(1)
        progress_recorder.set_progress(i, 15, description="Loading")

    swing.recording.delete()
    speed = round(random.uniform(30, 90), 2)
    swing.speed = speed
    swing.save()
    return {
        "message": f"Created swing for {swing.user} with speed {speed}",
        "swing": swing.pk
    }