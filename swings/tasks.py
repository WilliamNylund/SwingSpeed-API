from celery import shared_task
from time import sleep
from celery_progress.backend import ProgressRecorder
from django.core.files.storage import default_storage
import random
from .models import Swing
from .models import User

@shared_task(bind=True)
def test_task(self, path, user_id):
    print("start task")
    progress_recorder = ProgressRecorder(self)
    for i in range(100):
        sleep(0.1)
        progress_recorder.set_progress(i, 100, description="Loading")
    try:
        # Delete video if it was stored in default storage
        default_storage.delete(path)
    except:
        print("path was not in default_storage")
    speed = round(random.uniform(30, 90), 2)
    user = User.objects.get(pk=user_id)
    Swing(speed=speed, user=user).save()
    return f"Created swing for {user} with speed {speed}"