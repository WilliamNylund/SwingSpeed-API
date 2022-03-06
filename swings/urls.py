from django.urls import path, include
from swings import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('swings/', views.SwingList.as_view()),
    path('swings/<int:pk>/', views.SwingDetail.as_view()),
    path('swings/upload/', views.SwingMeasurment.as_view()),
    path('swings/progress/', include('celery_progress.urls')),
]
urlpatterns = format_suffix_patterns(urlpatterns)

