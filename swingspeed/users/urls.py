from django.urls import path, include
from users import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    #path('users/<int:pk>/profile-pictures/', views.UserProfilePicture.as_view()),
    path('users/profile-picture/', views.UserProfilePicture.as_view()),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken')),
]
#urlpatterns = format_suffix_patterns(urlpatterns)

