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
    #temp fix for paths
    splits = swing.recording.path.split('app/')
    path2 = splits[-1]
    actual_path = 'https://velofore.herokuapp.com/' + path2
    print(actual_path)
    analyze(self, actual_path)
    #delete video
    swing.recording.delete()
    speed = round(random.uniform(30, 90), 2)
    swing.speed = speed
    swing.save()
    return f"Created swing for {swing.user} with speed {speed}"