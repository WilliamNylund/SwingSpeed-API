from django.urls import path
from swings import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('swings/', views.SwingList.as_view()),
    path('swings/<int:pk>/', views.SwingDetail.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)

