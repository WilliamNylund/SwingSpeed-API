from celery import shared_task
from celery_progress.backend import ProgressRecorder
import random
from .models import Swing
# Now do your import
#from .tracker.main import analyze
from .videoanalysis import analyze
import base64

@shared_task(bind=True)
def test_task(self, swing_id):
    print("start task")
    swing = Swing.objects.get(pk=swing_id)
    analyze(self, swing.recording.path)
    #delete video
    swing.recording.delete()
    speed = round(random.uniform(30, 90), 2)
    swing.speed = speed
    swing.save()
    return f"Created swing for {swing.user} with speed {speed}"